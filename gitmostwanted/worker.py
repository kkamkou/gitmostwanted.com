# pylint: disable=E1002
from oauth2client.client import SignedJwtAssertionCredentials
from gitmostwanted.bigdata.result import Result
from gitmostwanted.app import app, celery
from apiclient import discovery, errors
from datetime import date
from httplib2 import Http

class ContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

celery.Task = ContextTask


def service_bigquery():
    config = app.config['GOOGLE_BIGQUERY']

    with open(config['private_key_path'], 'rb') as f:
        private_key = f.read()

    http_auth = SignedJwtAssertionCredentials(config['email'], private_key, config['url'])
    return discovery.build(config['service_name'], config['version'], http=http_auth.authorize(Http()))


@celery.task()
def most_starred_today(self):
    query_request = service_bigquery().jobs()
    query_data = {
        'query': """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM [githubarchive:day.events_%s]
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """ % date.today().strftime('%Y%m%d')
    }
    try:
        query_response = query_request.query(
            projectId=app.config['GOOGLE_BIGQUERY']['project_id'], body=query_data
        ).execute()

        result = Result(query_response)
    except errors.HttpError as e:
        raise self.retry(exc=e)

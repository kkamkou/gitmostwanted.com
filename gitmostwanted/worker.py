# pylint: disable=E1002
from oauth2client.client import SignedJwtAssertionCredentials
from gitmostwanted.app import app, celery
from apiclient.discovery import build
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
    return build(config['service_name'], config['version'], http=http_auth.authorize(Http()))

# query_request = service_bigquery().jobs()
# query_data = {'query': 'SELECT * FROM [githubarchive:month.201503] WHERE repo_id = 28922883;'}
# query_response = query_request.query(projectId=app.config['GOOGLE_BIGQUERY']['project_id'],
# body=query_data).execute()


@celery.task()
def mock():
    pass

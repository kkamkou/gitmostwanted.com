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
    private_key = ''
    email = ''
    url = 'https://www.googleapis.com/auth/bigquery.readonly'

    with open(private_key, 'rb') as f:
        private_key = f.read()

    http_auth = SignedJwtAssertionCredentials(email, private_key, url).authorize(Http())

    return build('bigquery', 'v2', http=http_auth)


@celery.task()
def mock():
    print(service_bigquery().datasets().list(projectId='').execute())
    pass

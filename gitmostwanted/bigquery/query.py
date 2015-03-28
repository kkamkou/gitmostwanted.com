from gitmostwanted.bigquery.result import Result
from gitmostwanted.app import app
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery, errors
from httplib2 import Http


def service():
    config = app.config['GOOGLE_BIGQUERY']

    with open(config['private_key_path'], 'rb') as f:
        private_key = f.read()

    auth = SignedJwtAssertionCredentials(config['email'], private_key, config['url'])
    return discovery.build(config['service_name'], config['version'], http=auth.authorize(Http()))


def result(body):
    try:
        pid = app.config['GOOGLE_BIGQUERY']['project_id']
        return Result(service().jobs().query(projectId=pid, body=body).execute())
    except errors.HttpError:
        return False

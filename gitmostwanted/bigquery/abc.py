from apiclient import discovery, errors
from gitmostwanted.bigquery.result import Result
from gitmostwanted.app import app
from httplib2 import Http
from uuid import uuid4
from oauth2client.client import SignedJwtAssertionCredentials


def api():
    config = app.config['GOOGLE_BIGQUERY']

    with open(config['private_key_path'], 'rb') as f:
        private_key = f.read()

    auth = SignedJwtAssertionCredentials(config['email'], private_key, config['url'])
    return discovery.build(config['service_name'], config['version'], http=auth.authorize(Http()))


def fetch(query, batch=False, num_retries=3, interval=10):
    project_id = app.config['GOOGLE_BIGQUERY']['project_id']
    service = api()
    job = query_async(service, project_id, query, batch, num_retries)

    poll_job(service, job['jobReference']['projectId'], job['jobReference']['jobId'], interval, num_retries)

    for page in paging(service, service.jobs().getQueryResults, num_retries=num_retries, **query_job['jobReference']):
        yield Result(page)


def query_async(service, project_id, query, batch=False, num_retries=3):
    body = {
        'jobReference': {
            'projectId': project_id,
            'job_id': str(uuid4())
        },
        'configuration': {
            'query': {
                'query': query,
                'priority': 'BATCH' if batch else 'INTERACTIVE'
            }
        }
    }
    return service.jobs().insert(projectId=project_id, body=body).execute(num_retries=num_retries)


def poll_job(service, projectId, jobId, interval=5.0, num_retries=5):
    """checks the status of a job every *interval* seconds"""

    import time

    job_get = service.jobs().get(projectId=projectId, jobId=jobId)
    job_resource = job_get.execute(num_retries=num_retries)

    while not job_resource['status']['state'] == 'DONE':
        print('Job is {}, waiting {} seconds...'
              .format(job_resource['status']['state'], interval))
        time.sleep(float(interval))
        job_resource = job_get.execute(num_retries=num_retries)

    return job_resource


def paging(service, request_func, num_retries=5, **kwargs):
    """pages though the results of an asynchronous job"""

    has_next = True
    while has_next:
        response = request_func(**kwargs).execute(num_retries=num_retries)
        if 'pageToken' in response:
            kwargs['pageToken'] = response['pageToken']
        else:
            has_next = False
        yield response

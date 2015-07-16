from uuid import uuid4
from gitmostwanted.bigquery.service import ServiceGmw


class Query:
    def __init__(self, service: ServiceGmw, query_str: str, num_retries: int=3):
        self.num_retries = num_retries
        self.service = service
        self.query = query_str

    def async(self, batch=False):
        body = {
            'jobReference': {
                'projectId': self.service.project_id,
                'job_id': str(uuid4())
            },
            'configuration': {
                'query': {
                    'query': self.query,
                    'priority': 'BATCH' if batch else 'INTERACTIVE'
                }
            }
        }
        return self.service.resource.jobs().insert(projectId=self.service.project_id, body=body)\
            .execute(num_retries=self.num_retries)

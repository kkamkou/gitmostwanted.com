from apiclient import discovery
from google.oauth2 import service_account


class Service:
    """
    :type resource: discovery.Resource
    """
    def __init__(
        self, json_key_path: str, service_name: str, version: str,
        scope: str
    ):
        credentials = service_account.Credentials\
            .from_service_account_file(json_key_path, scopes=[scope])
        self.resource = discovery.build(service_name, version, credentials=credentials)

    def jobs(self):  # @todo #58/DEV polish me
        return self.resource.jobs()


class ServiceGmw(Service):
    """
    :type __project_id: str
    """
    def __init__(self, json_key_path: str, project_id: str):
        self.__project_id = project_id
        super().__init__(
            json_key_path, 'bigquery', 'v2', 'https://www.googleapis.com/auth/bigquery'
        )

    @property
    def project_id(self):
        return self.__project_id

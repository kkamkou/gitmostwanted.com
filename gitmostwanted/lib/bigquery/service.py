from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from httplib2 import Http


class Service:
    """
    :type resource: discovery.Resource
    """
    def __init__(
        self, json_key_path: str, service_name: str, version: str,
        scope: str
    ):
        auth = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
        self.resource = discovery.build(service_name, version, http=auth.authorize(Http()))

    def jobs(self):  # @todo! polish me
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

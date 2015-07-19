from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery
from httplib2 import Http


class Service:
    """
    :type resource: discovery.Resource
    """
    def __init__(
        self, account_name: str, private_key: str, service_name: str, version: str,
        scope: str
    ):
        auth = SignedJwtAssertionCredentials(account_name, private_key, scope)
        self.resource = discovery.build(service_name, version, http=auth.authorize(Http()))

    def jobs(self):  # @todo! polish me
        return self.resource.jobs()


class ServiceGmw(Service):
    """
    :type __project_id: str
    """
    def __init__(self, account_name: str, private_key_path: str, project_id: str):
        self.__project_id = project_id

        with open(private_key_path, 'rb') as f:
            private_key = f.read()

        super().__init__(
            account_name, private_key, 'bigquery', 'v2',
            'https://www.googleapis.com/auth/bigquery'
        )

    @property
    def project_id(self):
        return self.__project_id

from unittest import TestCase
from gitmostwanted.models.repo import Repo


class ModelsRepoTestCase(TestCase):
    def test_accept_kwargs_in_constructor(self):
        self.assertEquals(Repo(language='python').language, 'python')

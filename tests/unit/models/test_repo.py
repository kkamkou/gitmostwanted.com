from unittest import TestCase
from gitmostwanted.models.repo import Repo


class ModelsRepoTestCase(TestCase):
    def test_accept_kwargs_in_constructor(self):
        entry = Repo(language='python')

        self.assertIsNone(entry.status_updated_at)
        self.assertEqual(entry.language, 'python')

    def test_update_status_with_timestamp(self):
        entry = Repo()

        entry.html_url = 'http://example.com'
        self.assertIsNone(entry.status_updated_at)

        entry.status = 'unknown'
        status_updated_at = entry.status_updated_at
        self.assertEqual(entry.status, 'unknown')
        self.assertIsNotNone(status_updated_at)

        entry.status = 'unknown'
        self.assertEqual(entry.status_updated_at, status_updated_at)

    def test_update_fields(self):
        entry = Repo()

        entry.homepage = 'example.com'
        self.assertEqual(entry.homepage, 'http://example.com')

        entry.description = ''
        self.assertEqual(entry.description, None)

        entry.description = 'atext' * 60
        self.assertEqual(len(entry.description), 250)

    def test_handle_incorrect_status(self):
        self.assertRaises(ValueError, Repo, status='abc')

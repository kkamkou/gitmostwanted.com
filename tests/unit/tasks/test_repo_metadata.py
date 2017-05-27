from gitmostwanted.app import db
from gitmostwanted.tasks.repo_metadata import is_worth_decreased
from unittest import TestCase


class TasksRepoMetadataTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()

    def test_is_worth_decreased(self):
        self.assertTrue(is_worth_decreased(2, 3))
        self.assertTrue(is_worth_decreased(20, 30))
        self.assertFalse(is_worth_decreased(95, 100))
        self.assertFalse(is_worth_decreased(105, 100))

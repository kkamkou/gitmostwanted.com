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

    def test_topic_diff_comparison(self):
        from gitmostwanted.models.repo import RepoTopics
        existing_topics = [RepoTopics(title='python'), RepoTopics(title='flask')]
        new_topics = {'python', 'flask'}
        diff = new_topics.difference(set(t.title for t in existing_topics))
        self.assertEqual(len(diff), 0)

        new_topics_with_extra = {'python', 'flask', 'sqlalchemy'}
        diff_extra = new_topics_with_extra.difference(set(t.title for t in existing_topics))
        self.assertEqual(diff_extra, {'sqlalchemy'})


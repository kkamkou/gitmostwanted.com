from datetime import date, datetime
from unittest import TestCase

from gitmostwanted.app import db
from gitmostwanted.models.repo import Repo, RepoMean, RepoTopics


class ModelsRepoTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        from gitmostwanted.app import db
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        from gitmostwanted.app import db
        db.drop_all()

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

    def test_repo_mean_default_date(self):
        r = Repo(id=1, full_name='test/repo', html_url='http://example.com', created_at=datetime.now(), name='repo')
        db.session.add(r)
        db.session.commit()

        rm = RepoMean(repo_id=1, value=12.5)
        db.session.add(rm)
        db.session.flush()
        self.assertEqual(rm.created_at, date.today())
        db.session.rollback()

    def test_repo_topics_index(self):
        index_columns = [
            set(col.name for col in idx.columns) for idx in RepoTopics.__table__.indexes
        ]
        self.assertIn({'title'}, index_columns)

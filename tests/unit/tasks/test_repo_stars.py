from datetime import datetime, timedelta
from gitmostwanted.app import db
from gitmostwanted.tasks.repo_stars import query_stars_by_repo
from unittest import TestCase


class TasksRepoStarsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()

    def test_query_stars_by_repo(self):
        yt = datetime.now() - timedelta(days=1)
        now = datetime.now()
        query = query_stars_by_repo(12, now, yt)
        self.assertTrue("'{}'".format(yt.strftime('%Y-%m')) in query)
        self.assertTrue("'{}'".format(now.strftime('%Y-%m')) in query)
        self.assertTrue('repo.id = {}'.format(12) in query)


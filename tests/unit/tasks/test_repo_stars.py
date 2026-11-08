from datetime import datetime, timedelta
from unittest import TestCase

from gitmostwanted.app import db
from gitmostwanted.tasks.repo_stars import query_stars_by_repo


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
        repo_id = 12
        query = query_stars_by_repo(repo_id, now, yt)
        self.assertIn(
            "_TABLE_SUFFIX BETWEEN '{}' AND '{}'".format(
                now.strftime('%Y%m%d')[1:], yt.strftime('%Y%m%d')[1:]
            ),
            query
        )
        self.assertIn('repo.id = {}'.format(repo_id), query)
        self.assertIn("COUNTIF(type = 'ForkEvent') * 3", query)
        self.assertIn("COUNTIF(type IN ('IssuesEvent', 'DiscussionEvent')) * 2", query)
        self.assertIn("COUNTIF(type IN ('WatchEvent', 'IssueCommentEvent')) + 1", query)
        self.assertIn("COUNTIF(type IN ('ReleaseEvent', 'PublicEvent')) * 5", query)
        self.assertIn("'PullRequestEvent', 'PullRequestReviewEvent', 'MemberEvent'", query)
        self.assertIn("COUNTIF(type = 'GollumEvent') * 2", query)
        self.assertIn('SQRT(', query)
        self.assertNotIn('AND type IN', query)
        for event in (
            'PushEvent', 'CreateEvent', 'IssuesEvent', 'PullRequestReviewCommentEvent',
            'ReleaseEvent', 'GollumEvent', 'MemberEvent', 'DiscussionEvent',
            'PullRequestEvent', 'DeleteEvent', 'PullRequestReviewEvent', 'IssueCommentEvent',
            'WatchEvent', 'ForkEvent', 'PublicEvent', 'CommitCommentEvent'
        ):
            self.assertIn(event, query)

from gitmostwanted.tasks.github import repo_starred_star
from unittest import TestCase, mock


class TasksGithubTestCase(TestCase):
    @mock.patch('gitmostwanted.tasks.github.user_starred')
    def test_star_rpository_with_invalid_starred(self, fake):
        fake.return_value = None, 404
        self.assertFalse(repo_starred_star(1, 'token'))
        fake.assert_called_once_with('token')

    @mock.patch('gitmostwanted.tasks.github.user_starred_star')
    @mock.patch('gitmostwanted.tasks.github.user_starred')
    @mock.patch('gitmostwanted.tasks.github.UserAttitude.liked_by_user')
    def test_star_rpository(self, fake_attitude, fake_starred, fake_starred_star):
        fake_starred.return_value = [{'full_name': 'repo1'}, {'full_name': 'repo3'}], 200

        std = mock.Mock()
        std.repo.full_name = 'repo2'
        fake_attitude.return_value = [std]

        res = repo_starred_star(1, 'token')
        fake_starred_star.assert_called_once_with('repo2', 'token')
        self.assertEqual(res, 1)

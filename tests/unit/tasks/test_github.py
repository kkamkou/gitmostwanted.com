from gitmostwanted.tasks.github import repo_starred_star
from unittest import TestCase, mock


class TasksGithubTestCase(TestCase):
    @mock.patch('gitmostwanted.tasks.github.user_starred')
    def test_star_repository_with_invalid_starred(self, fake):
        fake.return_value = None, 404
        self.assertFalse(repo_starred_star(1, 'token'))
        fake.assert_called_once_with('token')

    @mock.patch('gitmostwanted.tasks.github.user_starred_star')
    @mock.patch('gitmostwanted.tasks.github.user_starred')
    @mock.patch('gitmostwanted.tasks.github.UserAttitude.list_liked_by_user')
    @mock.patch('gitmostwanted.tasks.github.repo_like')
    def test_star_repository(self, fk_repo_like, fk_attitude, fk_starred, fk_starred_star):
        std1 = mock.Mock()
        std1.repo.full_name = 'repo2'

        std2 = mock.Mock()
        std2.repo.full_name = 'repo3'

        fk_attitude.return_value = [std1, std2]
        fk_starred.return_value = [{'full_name': 'repo1'}, {'full_name': 'repo3'}], 200

        res = repo_starred_star(1, 'token')
        self.assertEqual(res, (1, 1))

        fk_repo_like.assert_called_once_with('repo1', 1)
        fk_starred_star.assert_called_once_with('repo2', 'token')

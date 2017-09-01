from datetime import datetime
from gitmostwanted.app import db
from gitmostwanted.models.repo import RepoMean
from gitmostwanted.tasks.repo_status import \
    last_known_mean, repo_mean, result_mean, result_normalize, result_split
from itertools import chain
from types import GeneratorType
from unittest import TestCase


class TasksRepoStatusTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()

    def test_normalize_result(self):
        result = result_normalize([[28, 28], [8, 8]], 28)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEqual(lst[0], 8)
        self.assertEqual(lst[1], 0)
        self.assertEqual(lst[20], 28)
        self.assertEqual(len(lst), 28)

    def test_split_result(self):
        result = result_split(list(range(28)), 7)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEqual(len(lst), 4)
        self.assertEqual(len(lst[0]), 7)

    def test_find_last_known_mean(self):
        self.assertEqual(last_known_mean(1, 7), 7.0)
        db.session.add(RepoMean(repo_id=1, created_at=datetime.now(), value=77.0))
        db.session.commit()
        self.assertEqual(last_known_mean(1, 999), 77.0)

    def test_calculate_mean(self):
        def gn_normal():
            yield [10, 20]

        def gn_mixed():
            yield [10, 99999, 10]

        self.assertEqual(result_mean(gn_normal(), 1), 15)
        self.assertEqual(result_mean(gn_mixed(), 1), 1)
        self.assertEqual(result_mean(gn_mixed(), 10), 10)
        self.assertEqual(result_mean(chain(gn_mixed(), gn_normal()), 1), 8)

    def test_calculate_repo_mean(self):
        self.assertEqual(repo_mean([[0, 1], [1, 2], [2, 3], [3, 100]], 8, 2, 1000), 250.375)

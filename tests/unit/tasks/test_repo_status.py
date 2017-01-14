from datetime import datetime
from gitmostwanted.app import db
from gitmostwanted.models.repo import RepoMean
from gitmostwanted.tasks.repo_status import\
    result_normalize, result_split, result_mean, last_known_mean
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
        result = result_normalize([[8, 8], [28, 28]], 28)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEquals(lst[0], 8)
        self.assertEquals(lst[20], 28)
        self.assertEquals(len(lst), 28)

    def test_split_result(self):
        result = result_split(list(range(28)), 7)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEquals(len(lst), 4)
        self.assertEquals(len(lst[0]), 7)

    def test_last_known_mean(self):
        self.assertEqual(last_known_mean(1, 7), 7.0)
        db.session.add(RepoMean(repo_id=1, created_at=datetime.now(), value=77.0))
        db.session.commit()
        self.assertEqual(last_known_mean(1, 999), 77.0)

    def test_calculate_mean(self):
        def gn_normal():
            yield [10, 20]

        def gn_mixed():
            yield [10, 99999, 10]

        self.assertEquals(result_mean(gn_normal(), 1), 15)
        self.assertEquals(result_mean(gn_mixed(), 1), 1)
        self.assertEquals(result_mean(gn_mixed(), 10), 10)
        self.assertEquals(result_mean(chain(gn_mixed(), gn_normal()), 1), 8)

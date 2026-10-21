from datetime import datetime, timedelta
from itertools import chain
from types import GeneratorType
from unittest import TestCase

from gitmostwanted.app import db
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.repo import RepoMean, RepoStars
from gitmostwanted.tasks.repo_status import \
    last_known_mean, repo_mean, result_mean, result_normalize, result_split, status_detect


class TasksRepoStatusTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.create_all()
        db.session.add(
            Repo(
                created_at=datetime.now(), description='test', full_name='test/test',
                html_url='http://py.test', id=1, name='test'
            )
        )
        db.session.commit()

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

    def test_normalize_result_cross_year(self):
        d1 = (datetime(2020, 1, 1) + timedelta(days=364)).toordinal()  # Dec 30
        d2 = (datetime(2020, 1, 1) + timedelta(days=365)).toordinal()  # Dec 31
        d3 = (datetime(2021, 1, 1) + timedelta(days=0)).toordinal()    # Jan 1

        result = list(result_normalize([(d1, 10), (d2, 20), (d3, 30)], 3))
        self.assertEqual(result, [10, 20, 30])

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

        def gn_single():
            yield [42]

        def gn_empty():
            yield []

        def gn_none():
            return
            yield

        self.assertEqual(result_mean(gn_normal(), 1), 15)
        self.assertEqual(result_mean(gn_mixed(), 1), 1)
        self.assertEqual(result_mean(gn_mixed(), 10), 10)
        self.assertEqual(result_mean(chain(gn_mixed(), gn_normal()), 1), 8)
        self.assertEqual(result_mean(gn_single(), 5), 5)
        self.assertEqual(result_mean(gn_empty(), 5), 5)
        self.assertEqual(result_mean(gn_none(), 5), 5)

    def test_calculate_repo_mean(self):
        self.assertEqual(repo_mean([[0, 1], [1, 2], [2, 3], [3, 100]], 8, 2, 1000), 250.375)

    def test_status_detect_cross_year(self):
        db.session.add(
            Repo(
                created_at=datetime.now(), description='test2', full_name='test/test2',
                html_url='http://py.test/2', id=2, name='test2', status='unknown'
            )
        )
        # 14 days in 2020 (Dec 18 - Dec 31)
        for d in range(353, 367):
            db.session.add(RepoStars(repo_id=2, year=2020, day=d, stars=10))
        # 14 days in 2021 (Jan 1 - Jan 14)
        for d in range(1, 15):
            db.session.add(RepoStars(repo_id=2, year=2021, day=d, stars=10))
        db.session.commit()

        status_detect(28, 4)

        repo = db.session.get(Repo, 2)
        self.assertEqual(repo.status, 'promising')

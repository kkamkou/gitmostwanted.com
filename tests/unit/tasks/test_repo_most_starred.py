from unittest import TestCase
from unittest.mock import patch

from gitmostwanted.tasks.repo_most_starred import (
    most_starred_week, most_starred_month, most_starred_quarter, most_starred_year,
    most_starred_by_span
)


class TasksRepoMostStarredTestCase(TestCase):
    @patch('gitmostwanted.tasks.repo_most_starred.most_starred_sync')
    def test_most_starred_by_span(self, mock_sync):
        most_starred_by_span('ReportAllQuarterly', 'quarter')
        mock_sync.assert_called_once()
        args, _ = mock_sync.call_args
        self.assertEqual(args[0], 'ReportAllQuarterly')
        self.assertIn('_TABLE_SUFFIX BETWEEN', args[1])

    @patch('gitmostwanted.tasks.repo_most_starred.most_starred_by_span')
    def test_most_starred_tasks(self, mock_by_span):
        most_starred_week()
        mock_by_span.assert_called_with('ReportAllWeekly', 'week')

        most_starred_month()
        mock_by_span.assert_called_with('ReportAllMonthly', 'month')

        most_starred_quarter()
        mock_by_span.assert_called_with('ReportAllQuarterly', 'quarter')

        most_starred_year()
        mock_by_span.assert_called_with('ReportAllYearly', 'year')

from unittest import TestCase

from gitmostwanted.models.report import ReportAllDaily, ReportAllWeekly, ReportAllMonthly, \
    ReportAllQuarterly, \
    ReportAllYearly


class ModelsReportTestCase(TestCase):
    def test_report_tablename(self):
        self.assertEqual(ReportAllDaily.__tablename__, 'report_all_daily')
        self.assertEqual(ReportAllWeekly.__tablename__, 'report_all_weekly')
        self.assertEqual(ReportAllMonthly.__tablename__, 'report_all_monthly')
        self.assertEqual(ReportAllQuarterly.__tablename__, 'report_all_quarterly')
        self.assertEqual(ReportAllYearly.__tablename__, 'report_all_yearly')

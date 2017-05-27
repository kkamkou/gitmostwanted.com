from gitmostwanted.services.log import instance
from unittest import TestCase, mock


class ServicesLogTestCase(TestCase):
    def test_use_logger_if_needed(self):
        app = mock.MagicMock(debug=False, logger=mock.MagicMock())
        with mock.patch('logging.handlers.TimedRotatingFileHandler'):
            instance(app)
        self.assertEqual(app.logger.addHandler.call_count, 1)

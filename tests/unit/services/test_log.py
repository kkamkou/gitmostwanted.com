from gitmostwanted.services.log import instance
from unittest import TestCase, mock


class ServicesLogTestCase(TestCase):
    def test_use_logger_normally(self):
        app = mock.MagicMock(debug=False, testing=False, logger=mock.MagicMock())
        with mock.patch('logging.handlers.TimedRotatingFileHandler'):
            instance(app)
        self.assertEqual(app.logger.addHandler.call_count, 1)

    def test_logging_handlers_imported(self):
        import logging
        self.assertTrue(hasattr(logging, 'handlers'))
        self.assertTrue(hasattr(logging.handlers, 'TimedRotatingFileHandler'))


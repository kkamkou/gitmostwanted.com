from gitmostwanted.services.celery import instance
from unittest import TestCase, mock
from gitmostwanted.web import app


class ServicesCeleryTestCase(TestCase):
    def test_use_flask_context(self):
        context = mock.MagicMock()

        app.app_context = lambda: context
        app.config['CELERY_ALWAYS_EAGER'] = True
        app.config['CELERY_IGNORE_RESULT'] = True

        class FakeTask(instance(app).Task):
            def run(self): pass

        FakeTask().delay()

        context.__enter__.assert_called_once_with()

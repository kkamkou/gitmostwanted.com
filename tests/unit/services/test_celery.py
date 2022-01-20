from unittest import mock

import pytest

from gitmostwanted.web import app


@pytest.fixture(scope='session')
def celery_parameters():
    return {'task_cls': 'lib.celery.flask_context_task:FlaskContextTask'}


def test_use_flask_context(celery_app, celery_worker):
    context = mock.MagicMock()

    app.app_context = lambda: context

    @celery_app.task
    def test():
        return 1

    celery_worker.reload()

    test.delay().get(timeout=10)

    context.__enter__.assert_called_once_with()

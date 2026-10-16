import os
os.environ['GMW_APP_ENV'] = 'testing'

import pytest
from gitmostwanted.app import app

pytest_plugins = ["celery.contrib.pytest"]


@pytest.fixture(autouse=True, scope='session')
def app_context():
    with app.app_context():
        yield

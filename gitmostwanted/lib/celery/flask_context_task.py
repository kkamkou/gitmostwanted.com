from abc import ABC

from celery import Task

from gitmostwanted.app import app


class FlaskContextTask(Task, ABC):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

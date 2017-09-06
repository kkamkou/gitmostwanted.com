from celery import Celery as TheCelery, Task
from raven import Client
from raven.contrib.celery import register_logger_signal, register_signal


def instance(app):
    """:rtype: Celery"""
    class Celery(TheCelery):
        @staticmethod
        def on_configure():
            if not app.debug and not app.testing:
                client = Client(app.config['SENTRY_IO']['celery']['dsn'])
                register_logger_signal(client)
                register_signal(client)

    inst = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    inst.conf.update(app.config)

    class ContextTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    inst.Task = ContextTask
    return inst

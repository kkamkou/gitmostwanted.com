from celery import Celery


def instance(app):
    """:rtype: Celery"""
    return Celery(
        app.import_name,
        broker=app.config.get('CELERY_URL_BROKER'),
        backend=app.config.get('CELERY_URL_BACKEND'),
        task_cls='gitmostwanted.lib.celery.flask_context_task:FlaskContextTask'
    )

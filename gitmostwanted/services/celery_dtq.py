from celery import Celery


def instance(app):
    """:rtype: Celery"""
    return Celery(
        app.import_name,
        backend=app.config.get('CELERY_URL_BACKEND'),
        broker=app.config.get('CELERY_URL_BROKER'),
        config_source='celeryconfig',
        task_cls='gitmostwanted.lib.celery.flask_context_task:FlaskContextTask'
    )

from celery import Celery


def instance(app):
    inst = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    inst.conf.update(app.config)

    class ContextTask(inst.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    inst.Task = ContextTask
    return inst

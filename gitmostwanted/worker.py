from .app import app, celery


class ContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

celery.Task = ContextTask

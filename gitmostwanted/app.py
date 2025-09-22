from os import environ

from flask import Flask

from gitmostwanted.services import \
    celery_dtq as service_celery, db as service_db, log as service_log, sentry as service_sentry

env = environ.get('GMW_APP_ENV', 'development').capitalize()

app = Flask(__name__)
app.config.from_object('gitmostwanted.config.Config' + env)
app.config.from_envvar('GMW_APP_SETTINGS', silent=True)
app.config.from_prefixed_env(prefix='GMW')

service_sentry.register(app)

celery = service_celery.instance(app)
db = service_db.instance(app)
log = service_log.instance(app)

log.info("Environment used: %s", app.config.get('ENVIRONMENT'))

del environ, Flask, service_celery, service_db, service_log, service_sentry

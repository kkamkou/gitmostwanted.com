from gitmostwanted.services import celery as service_celery, db as service_db
from flask import Flask
from os import environ

env = environ.get('GMW_APP_ENV', 'development').capitalize()

app = Flask(__name__)
app.config.from_object('gitmostwanted.config.Config' + env)
app.config.from_envvar('GMW_APP_SETTINGS', silent=True)

celery = service_celery.instance(app)
db = service_db.instance(app)

if not app.debug:
    from logging import handlers, INFO
    handler = handlers.TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=1)
    handler.setLevel(INFO)
    app.logger.addHandler(handler)

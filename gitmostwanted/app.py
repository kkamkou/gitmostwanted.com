from gitmostwanted.services import oauth, celery, db
from flask import Flask
from os import environ

env = environ.get('GMW_APP_ENV', 'development').capitalize()

app = Flask(__name__)
app.config.from_object('gitmostwanted.config.Config' + env)
app.config.from_envvar('GMW_APP_SETTINGS', silent=True)

celery = celery.instance(app)
oauth = oauth.instance(app)
db = db.instance(app)

if not app.debug:
    from logging import handlers, INFO
    handler = handlers.TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=1)
    handler.setLevel(INFO)
    app.logger.addHandler(handler)

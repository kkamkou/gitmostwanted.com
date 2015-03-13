from os import environ
from flask import Flask

env = environ.get('GMW_APP_ENV', 'development').capitalize()

application = Flask(__name__)
application.config.from_object('gitmostwanted.config.Config' + env)

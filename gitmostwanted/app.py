from os import environ
from flask import Flask
from flask.ext.oauthlib.client import OAuth

env = environ.get('GMW_APP_ENV', 'development').capitalize()

app = Flask(__name__)
app.config.from_object('gitmostwanted.config.Config' + env)

oauth = OAuth()
github = oauth.remote_app('github', app_key='OAUTH_GITHUB')
oauth.init_app(app)

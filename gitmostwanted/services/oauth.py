from flask.ext.oauthlib.client import OAuth


def instance(app):
    oauth = OAuth()
    oauth.remote_app('github', app_key='GITHUB_OAUTH')
    oauth.init_app(app)
    return oauth

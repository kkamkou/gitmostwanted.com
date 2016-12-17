from flask_oauthlib.client import OAuth


def instance(app):
    """:rtype: OAuth"""
    oauth = OAuth()
    oauth.remote_app('github', app_key='GITHUB_OAUTH')
    oauth.init_app(app)
    return oauth

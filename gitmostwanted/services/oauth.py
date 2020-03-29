from authlib.integrations.flask_client import OAuth


def instance(app):
    """:rtype: OAuth"""
    return OAuth(app)

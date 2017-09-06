from raven.contrib.flask import Sentry


def instance(app):
    """:rtype: Sentry"""
    sentry = Sentry()
    if not app.debug and not app.testing:
        sentry.init_app(app, **app.config['SENTRY_IO']['flask'])
    return sentry

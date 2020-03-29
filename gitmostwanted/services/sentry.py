from importlib import import_module
from itertools import groupby

import sentry_sdk
from flask import Flask


def register(app: Flask):
    if 'SENTRY_IO' not in app.config:
        return

    def merged_configuration(conf: dict) -> dict:
        defaults = {
            'environment': app.config['ENVIRONMENT'],
            'debug': app.config['DEBUG']
        }
        return {**defaults, **conf}

    for (k, grp) in groupby(app.config['SENTRY_IO']):
        mdl = 'sentry_sdk.integrations.' + k.lower()
        integrations = map(
            lambda key: getattr(import_module(mdl), key.title() + 'Integration')(), grp
        )
        sentry_sdk.init(
            dsn=app.config['SENTRY_IO'][k]['dsn'],
            integrations=list(integrations),
            **merged_configuration(
                app.config['SENTRY_IO'][k]['configuration']
                if 'configuration' in app.config['SENTRY_IO'][k] else {}
            )
        )

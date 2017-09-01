import logging


def instance(app):
    """:rtype: logging.Logger"""
    if app.testing:
        app.logger.disabled = True
        return app.logger

    if app.debug:
        app.logger.setLevel(logging.DEBUG)
        return app.logger

    handler = logging.handlers\
        .TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=7)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app.logger

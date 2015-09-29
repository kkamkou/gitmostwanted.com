def instance(app):
    """:rtype: logging.Logger"""
    if app.debug:
        return app.logger

    from logging import handlers, INFO

    handler = handlers.TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=1)
    handler.setLevel(INFO)

    app.logger.addHandler(handler)
    return app.logger

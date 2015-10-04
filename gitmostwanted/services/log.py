def instance(app):
    """:rtype: logging.Logger"""
    if app.debug:
        return app.logger

    from logging import handlers, INFO, Formatter
    handler = handlers.TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=1)
    handler.setLevel(INFO)
    handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.setLevel(INFO)
    app.logger.addHandler(handler)
    return app.logger

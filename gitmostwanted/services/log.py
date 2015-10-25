def instance(app):
    """:rtype: logging.Logger"""
    if app.debug:
        return app.logger

    import logging

    handler = logging.handlers\
        .TimedRotatingFileHandler(app.config['DEBUG_FILE'], when='d', backupCount=7)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app.logger

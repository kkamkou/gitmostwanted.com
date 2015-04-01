# pylint: disable=C1001
class Config():
    CELERY_BROKER_URL = ''
    SQLALCHEMY_ECHO = False
    SECRET_KEY = ''
    TESTING = False
    DEBUG = False


class ConfigDevelopment(Config):
    SQLALCHEMY_ECHO = True
    DEBUG = True


class ConfigTesting(Config):
    SECRET_KEY = 'testing'
    TESTING = True


class ConfigProduction(Config):
    pass

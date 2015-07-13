# pylint: disable=C1001
class Config:
    CELERY_BROKER_URL = ''
    SQLALCHEMY_ECHO = False
    SECRET_KEY = ''
    TESTING = False
    DEBUG = True


class ConfigDevelopment(Config):
    SQLALCHEMY_ECHO = True


class ConfigTesting(Config):
    SECRET_KEY = 'testing'  # noqa
    TESTING = True


class ConfigProduction(Config):
    DEBUG = False

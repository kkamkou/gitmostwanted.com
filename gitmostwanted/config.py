# pylint: disable=C1001
class Config:
    # Custom
    DEBUG_FILE = '/tmp/gmw.log'
    ENVIRONMENT = 'development'

    # Application related
    REPOSITORY_WORTH_MINIMUM = 6

    # Flask
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = 1209600  # 14 days
    SECRET_KEY = ''
    TESTING = False

    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    CELERY_TIMEZONE = 'Europe/Berlin'
    CELERY_BROKER_URL = ''

    # Oauth
    GITHUB_AUTH = (None, None)


class ConfigDevelopment(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ConfigTesting(Config):
    ENVIRONMENT = 'testing'
    GITHUB_AUTH = ('Test', '')
    SECRET_KEY = 'testing'  # noqa
    TESTING = True


class ConfigProduction(Config):
    DEBUG = False
    ENVIRONMENT = 'production'

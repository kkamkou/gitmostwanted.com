# pylint: disable=C1001
class Config:
    ENVIRONMENT = 'development'

    # Custom
    DEBUG_FILE = '/tmp/gmw.log'

    # Application related
    REPOSITORY_WORTH_SOLID = 6
    REPOSITORY_WORTH_DEFAULT = 3

    # Flask
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = 1209600  # 14 days
    SECRET_KEY = ''
    TESTING = False

    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Oauth
    GITHUB_AUTH = (None, None)
    GITHUB_OAUTH = {}


class ConfigDevelopment(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ConfigTesting(Config):
    ENVIRONMENT = 'testing'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    GITHUB_AUTH = ('Test', '')
    SECRET_KEY = 'testing'  # noqa
    TESTING = True


class ConfigProduction(Config):
    ENVIRONMENT = 'production'

    DEBUG = False


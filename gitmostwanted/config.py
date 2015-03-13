class Config:
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    DEBUG = False
    TESTING = False


class ConfigDevelopment(Config):
    DEBUG = True


class ConfigProduction(Config):
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    DEBUG = True

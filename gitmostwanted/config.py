class Config:
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = 'secret_key'
    DEBUG = False
    TESTING = False

    OAUTH_GITHUB = dict(
        consumer_key='',
        consumer_secret='',
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
    )


class ConfigDevelopment(Config):
    DEBUG = True


class ConfigProduction(Config):
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    DEBUG = True

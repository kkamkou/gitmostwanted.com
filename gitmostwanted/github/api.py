from gitmostwanted.app import app
from requests import get, exceptions


def fetch(uri):
    try:
        result = get('https://api.github.com/%s' % uri, auth=app.config['GITHUB_AUTH'])
        result.raise_for_status()
        return result.json()
    except exceptions.HTTPError as e:
        app.logger.error('Request exception %d: %s' % (e.errno, e.strerror))


def repo_info(full_name):
    return fetch('repos/%s' % full_name)


def rate_limit():
    return fetch('rate_limit')

from gitmostwanted.app import app
from requests import get, exceptions


def fetch(uri):
    try:
        result = get('https://api.github.com/{0}'.format(uri), auth=app.config['GITHUB_AUTH'])
        result.raise_for_status()
        return result.json()
    except exceptions.HTTPError as e:
        app.logger.warning('Request exception {0}: {1}'.format(e.errno, e.strerror))
        return None


def repo_info(full_name):
    return fetch('repos/{0}'.format(full_name))


def rate_limit():
    return fetch('rate_limit')

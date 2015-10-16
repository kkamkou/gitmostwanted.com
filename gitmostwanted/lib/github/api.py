from gitmostwanted.app import app
from requests import get, exceptions


def fetch(uri):
    """:rtype: (str|None, int)"""
    json = None
    try:
        result = get('https://api.github.com/{0}'.format(uri), auth=app.config['GITHUB_AUTH'])
        result.raise_for_status()
        json = result.json()
    except exceptions.HTTPError as e:
        app.logger.info(
            'Request exception {0}: {1}, code: {2}'.format(e.errno, e.strerror, result.status_code)
        )
    return json, result.status_code


def repo_info(full_name: str):
    return fetch('repos/{0}'.format(full_name))


def rate_limit():
    return fetch('rate_limit')

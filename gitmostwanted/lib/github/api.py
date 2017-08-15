"""
@todo #113:3h GitHub API must be re-factored. The current architecture is too complicated to
 paginate.
"""

from gitmostwanted.app import app
import requests


def fetch(uri: str, method: str = 'get', token: str = None):
    """:rtype: (str|None, int)"""
    uri = 'https://api.github.com/{0}'.format(uri)
    auth = app.config['GITHUB_AUTH']
    headers = {}
    json = None

    if token:
        headers['Authorization'] = 'token {}'.format(token)
        auth = None

    try:
        result = getattr(requests, method.lower())(uri, auth=auth, headers=headers)
        result.raise_for_status()
        json = result.json() if result.status_code != 204 else None
    except requests.HTTPError as e:
        app.logger.info(
            "Request to {} is failed ({}, {}): {}\n{}\n"
            .format(result.url, method, e.strerror, result.status_code, result.text)
        )

    return json, result.status_code


def repo_info(full_name: str):
    return fetch('repos/{}'.format(full_name))


def user_starred(token: str = None):
    return fetch('user/starred?per_page=9999', token=token)


def user_starred_star(full_name: str, token: str):
    return fetch('user/starred/{}'.format(full_name), method='PUT', token=token)


def rate_limit():
    return fetch('rate_limit')

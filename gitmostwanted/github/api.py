from gitmostwanted.app import app
from requests import get


def repo_info(name):
    result = get('https://api.github.com/repos/%s' % name, auth=app.config['GITHUB_AUTH'])
    if result.status_code != 200:
        return None
    return result.json()


def rate_limit():
    return get('https://api.github.com/rate_limit', auth=app.config['GITHUB_AUTH']).json()

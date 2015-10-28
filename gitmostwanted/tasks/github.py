from gitmostwanted.lib.github.api import user_starred, user_starred_star
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.app import celery


@celery.task()
def repo_starred_star(user_id: int, access_token: str):
    starred, code = user_starred(access_token)
    if not starred:
        return False

    attitudes = UserAttitude.query\
        .filter(UserAttitude.user_id == user_id)\
        .filter(UserAttitude.attitude == 'like')

    lst = [user_starred_star(r.repo.full_name, access_token) for r in attitudes
           if not [x for x in starred if x['full_name'] == r.repo.full_name]]

    return len(lst)

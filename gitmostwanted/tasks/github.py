from gitmostwanted.app import celery, db
from gitmostwanted.lib.github.api import user_starred, user_starred_star
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.user import UserAttitude


@celery.task()
def repo_starred_star(user_id: int, access_token: str):
    starred, code = user_starred(access_token)
    if not starred:
        return False

    attitudes = UserAttitude.list_liked_by_user(user_id)

    lst_in = [repo_like(s['full_name'], user_id) for s in starred
              if not [a for a in attitudes if s['full_name'] == a.repo.full_name]]

    lst_out = [user_starred_star(r.repo.full_name, access_token) for r in attitudes
               if not [x for x in starred if x['full_name'] == r.repo.full_name]]

    return len(lst_out), len(list(filter(None, lst_in)))


def repo_like(repo_name: str, uid: int):
    repo = Repo.get_one_by_full_name(repo_name)
    if not repo:
        return None

    db.session.merge(UserAttitude.like(uid, repo.id))
    db.session.commit()
    return repo.id

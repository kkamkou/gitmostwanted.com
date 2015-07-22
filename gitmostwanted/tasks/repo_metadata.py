from gitmostwanted.app import db, celery
from gitmostwanted.models.repo import Repo
from datetime import datetime, timedelta


@celery.task()
def repo_flag_mature(num_months):
    repos = Repo.query\
        .filter(Repo.created_at >= datetime.now() + timedelta(days=num_months * 30 * -1))\
        .filter(Repo.mature.is_(False))
    for repo in repos:
        repo.mature = True
        db.session.commit()
    return repos.count()

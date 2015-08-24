from gitmostwanted.app import db, celery
from gitmostwanted.models.repo import Repo
from gitmostwanted.github import api
from datetime import datetime, timedelta
from time import sleep


@celery.task()
def repo_flag_mature(num_months):
    repos = Repo.query\
        .filter(Repo.created_at <= datetime.now() + timedelta(days=num_months * 30 * -1))\
        .filter(Repo.mature.is_(False))
    for repo in repos:
        repo.mature = True
        db.session.commit()
    return repos.count()


@celery.task()
def repo_details_update(num_days):
    repos = Repo.query\
        .filter(
            Repo.checked_at.is_(None) |
            (Repo.checked_at <= datetime.now() + timedelta(days=num_days * -1))
        )\
        .yield_per(10)\
        .limit(200)  # GitHup allows only 3000 calls per day within a token
    for repo in repos:
        repo.checked_at = datetime.now()

        details = api.repo_info(repo.full_name)
        if not details:
            continue

        for key in ['description', 'language', 'homepage']:
            if getattr(repo, key) != details[key]:
                setattr(repo, key, details[key])

        db.session.commit()
    return repos.count()

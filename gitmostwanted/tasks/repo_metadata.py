from gitmostwanted.app import app, db, celery
from gitmostwanted.models.repo import Repo
from gitmostwanted.github import api
from datetime import datetime, timedelta


@celery.task()
def metadata_maturity(num_months):
    repos = Repo.query\
        .filter(Repo.created_at <= datetime.now() + timedelta(days=num_months * 30 * -1))\
        .filter(Repo.mature.is_(False))
    for repo in repos:
        repo.mature = True
        db.session.commit()
    return repos.count()


@celery.task()
def metadata_refresh(num_days):
    repos = Repo.query\
        .filter(
            Repo.checked_at.is_(None) |
            (Repo.checked_at <= datetime.now() + timedelta(days=num_days * -1))
        )\
        .yield_per(10)\
        .limit(200)  # GitHub allows only 3000 calls per day within a token
    for repo in repos:
        repo.checked_at = datetime.now()

        details, code = api.repo_info(repo.full_name)
        if not details:
            if 400 <= code < 500:
                repo.worth -= 1
                app.logger.info(
                    '{0} is not found, the "worth" has been decreased by 1'.format(repo.full_name)
                )
            continue

        for key in ['description', 'language', 'homepage']:
            if getattr(repo, key) != details[key]:
                setattr(repo, key, details[key])

        db.session.commit()
    return repos.count()


@celery.task()
def metadata_erase():
    query = Repo.query.filter((Repo.status == 'deleted') & (Repo.worth < 0))
    cnt = query.count()
    query.delete()
    return cnt

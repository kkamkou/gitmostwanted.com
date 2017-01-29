from datetime import datetime, timedelta
from gitmostwanted.app import app, db, celery
from gitmostwanted.lib.github import api
from gitmostwanted.models.repo import Repo, RepoMean
from sqlalchemy.sql import func, expression
from statistics import stdev


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
        .yield_per(25)\
        .limit(300)  # GitHub allows only 3000 calls per day within a token
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

        for key in ['description', 'language', 'homepage', 'stargazers_count']:
            if getattr(repo, key) != details[key]:
                setattr(repo, key, details[key])

        db.session.commit()
    return repos.count()


@celery.task()
def metadata_trend(num_days):
    results = db.session.query(
        RepoMean.repo_id, func.substring_index(
            func.group_concat(
                RepoMean.value.op('ORDER BY')(expression.desc(RepoMean.created_at))
            ), ',', 2)
        )\
        .filter(RepoMean.created_at >= datetime.now() + timedelta(days=num_days * -1))\
        .group_by(RepoMean.repo_id)\
        .all()
    for result in filter(lambda x: ',' in x[1], results):
        curr, prev = map(lambda v: float(v), result[1].split(','))
        if curr < prev and stdev([curr, prev]) > 1:
            app.logger.info(
                'Mean value of {0} is {1}, previous was {2}. The "worth" has been decreased by 1'
                .format(result[0], curr, prev)
            )
            db.session.query(Repo)\
                .filter(Repo.id == result[0])\
                .update({Repo.worth: Repo.worth - 1})
            db.session.commit()


@celery.task()
def metadata_erase():
    cnt = Repo.query.filter(Repo.worth < -5).delete()
    db.session.commit()
    return cnt

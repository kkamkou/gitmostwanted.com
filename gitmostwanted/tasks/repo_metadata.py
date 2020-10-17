from datetime import datetime, timedelta

from sqlalchemy.sql import func, expression

from gitmostwanted.app import app, log, db, celery
from gitmostwanted.lib.github import api
from gitmostwanted.models.repo import Repo, RepoMean


@celery.task()
def metadata_maturity(num_months):
    cnt = func.count(RepoMean.repo_id).label('cnt')
    repos = db.session.query(RepoMean.repo_id, cnt).join(Repo)\
        .filter(Repo.mature.is_(False))\
        .group_by(RepoMean.repo_id)\
        .having(cnt >= num_months)
    for (repo_id, cnt) in repos:
        db.session.query(Repo).filter(Repo.id == repo_id).update({Repo.mature: True})
        db.session.commit()
        log.info('{0} is marked as mature ({1})'.format(repo_id, cnt))
    return repos.count()


@celery.task()
def metadata_refresh(num_days):
    repos = Repo.query\
        .filter(
            (Repo.status != 'deleted') & (
                Repo.checked_at.is_(None) |
                (Repo.checked_at <= datetime.now() + timedelta(days=num_days * -1))
            )
        )\
        .yield_per(25)\
        .limit(300)  # GitHub allows only 3000 calls per day within a token
    for repo in repos:
        details, code = api.repo_info(repo.full_name)
        if not details:
            if 400 <= code < 500:
                repo.worth -= 1
                db.session.commit()
                log.info(
                    '{0} is not found (code={1}), the "worth" has been decreased by 1'
                    .format(repo.full_name, code)
                )
            continue

        repo.checked_at = datetime.now()

        for key in [
            'description', 'forks_count', 'homepage', 'language', 'open_issues_count', 'size',
            'stargazers_count', 'subscribers_count'
        ]:
            if getattr(repo, key) != details[key]:
                setattr(repo, key, details[key])

        if 'license' in details:
            license = getattr(details['license'], 'key', 'unlicense')
            if license != repo.license:
                setattr(repo, 'license', license)

        db.session.commit()

        log.info('Repository {0}({1}) has been updated'.format(repo.id, repo.full_name))
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
        if is_worth_decreased(curr, prev):
            log.info(
                'Mean value of {0} is {1}, previous was {2}. The "worth" has been decreased by 1'
                .format(result[0], curr, prev)
            )
            db.session.query(Repo)\
                .filter(Repo.id == result[0])\
                .update({Repo.worth: Repo.worth - 1})
            db.session.commit()


@celery.task()
def metadata_erase():
    cnt = Repo.query\
        .filter((Repo.worth < -5) & (Repo.worth_max <= app.config['REPOSITORY_WORTH_DEFAULT'] * 3))\
        .delete()
    log.info('{0} repositories has been removed (worthless)'.format(cnt))
    db.session.commit()


# defines the logic to determinate if worth is really decreased or just slightly jumped down
def is_worth_decreased(curr, prev):
    if curr < 3:
        return True
    return curr < prev and ((prev - curr) * 100 / prev) >= 10

from gitmostwanted.models.repo import Repo, RepoStars, RepoMean
from gitmostwanted.app import db, celery
from sqlalchemy.sql import expression
from statistics import variance, mean
from datetime import datetime, timedelta
from types import GeneratorType


@celery.task()
def status_detect(num_days, num_segments):
    repos = Repo.query.filter().filter(Repo.status == 'unknown')
    for repo in repos:
        result = db.session.query(RepoStars.day, RepoStars.stars)\
            .filter(RepoStars.repo_id == repo.id)\
            .order_by(expression.asc(RepoStars.day))\
            .all()

        val = 0 if not result else result_mean(
            result_split(list(result_normalize(result, num_days)), num_segments)
        )

        repo.status = 'hopeless' if val < 1 else 'promising'

        db.session.add(RepoMean(repo=repo, value=val))
        db.session.commit()


@celery.task()
def status_refresh(num_days):
    repos = Repo.query\
        .filter(Repo.status.in_(('promising', 'hopeless')))\
        .filter(Repo.status_updated_at <= datetime.now() + timedelta(days=num_days * -1))
    for repo in repos:
        RepoStars.query.filter(RepoStars.repo_id == repo.id).delete()

        repo.worth += 1 if repo.status == 'promising' else -1
        repo.status = 'new' if repo.worth > -1 else 'deleted'

        db.session.commit()


def result_mean(chunks: GeneratorType):
    return mean([1 if variance(chunk) >= 1000 else mean(chunk) for chunk in chunks])


def result_normalize(lst: list, num_days: int):
    fst = lst[0][0]
    lst = dict(lst)
    for i in range(num_days):
        key = fst + i
        yield 0 if key not in lst else lst[key]


def result_split(lst: list, num_rows: int):
    num_segments = len(lst) // num_rows
    for i in range(num_segments):
        yield lst[(i * num_rows):((i + 1) * num_rows)]

from datetime import datetime, timedelta
from gitmostwanted.app import app, db, celery
from gitmostwanted.lib.bigquery.job import Job
from gitmostwanted.models.repo import Repo, RepoStars
from gitmostwanted.services import bigquery
from time import sleep


def results_of(j: Job):
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


@celery.task()
def stars_mature(num_days):
    date_from = (datetime.now() + timedelta(days=num_days * -1)).strftime('%Y-%m-%d')
    date_to = datetime.now()
    service = bigquery.instance(app)

    jobs = []

    repos = Repo.query\
        .filter(Repo.mature.is_(True))\
        .filter(Repo.status == 'new')\
        .limit(40)  # we are at the free plan
    for repo in repos:
        query = query_stars_by_repo(repo_id=repo.id, date_from=date_from, date_to=date_to)

        job = Job(service, query, batch=True)
        job.execute()

        jobs.append((job, repo))

    for job in jobs:
        for row in results_of(job[0]):
            db.session.add(RepoStars(repo_id=job[1].id, stars=row[0], year=row[1], day=row[2]))

        job[1].status = 'unknown'

        db.session.commit()


@celery.task()
def stars_repo_reset(repo_id, date_from, date_to):
    service = bigquery.instance(app)
    query = query_stars_by_repo(repo_id=repo_id, date_from=date_from, date_to=date_to)

    job = Job(service, query)
    job.execute()

    cnt = 0
    lst = {}
    for row in results_of(job):
        key = '{} {}'.format(row[1], row[3])
        lst[key] = lst.get(key, []) + [row[0]]

        db.session.merge(RepoStars(repo_id=repo_id, stars=row[0], year=row[1], day=row[2]))
        cnt += 1

    for val, yj in lst:
        avg = val  # call normalization
        date = datetime.datetime.strptime(yj, '%Y %j')

        # insert to the mean table

    db.session.query(Repo).filter(Repo.id == repo_id).update({Repo.status: 'unknown'})

    db.session.commit()

    return cnt


# @todo #192:1h move BQ queries to a separate place
def query_stars_by_repo(repo_id: int, date_from: datetime, date_to: datetime):
    query = """
        SELECT
            COUNT(1) AS stars, YEAR(created_at) AS y, DAYOFYEAR(created_at) AS doy,
            MONTH(created_at) as mon
        FROM
            TABLE_DATE_RANGE([githubarchive:day.], TIMESTAMP('{date_from}'), TIMESTAMP('{date_to}'))
        WHERE
            repo.id = {id} AND type IN ('WatchEvent', 'ForkEvent')
        GROUP BY y, doy
    """
    return query.format(
        id=repo_id, date_from=date_from.strftime('%Y-%m-%d'), date_to=date_to.strftime('%Y-%m-%d')
    )

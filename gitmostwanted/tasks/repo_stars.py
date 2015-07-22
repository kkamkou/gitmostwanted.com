from gitmostwanted.models.repo import Repo, RepoStars
from gitmostwanted.app import app, db, celery
from gitmostwanted.services import bigquery
from gitmostwanted.bigquery.job import Job
from datetime import datetime, timedelta
from time import sleep


def job_results(j: Job):
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


@celery.task()
def repos_stars(days_from, days_to):
    service = bigquery.new_instance(app)

    date_from = (datetime.now() + timedelta(days=days_from)).strftime('%Y-%m-%d')
    date_to = (datetime.now() + timedelta(days=days_to)).strftime('%Y-%m-%d')
    query = """
        SELECT
            COUNT(1) AS stars, YEAR(created_at) AS y, DAYOFYEAR(created_at) AS doy
        FROM
            TABLE_DATE_RANGE(
                githubarchive:day.events_,
                TIMESTAMP('{date_from}'),
                TIMESTAMP('{date_to}')
            )
        WHERE repo.id = {id} AND type = 'WatchEvent'
        GROUP BY y, doy
    """

    repos = Repo.query.with_entities(Repo.id)\
        .filter(Repo.created_at >= date_from)\
        .filter(Repo.created_at <= date_to)
    for repo in repos:
        job = Job(service, query.format(id=repo.id, date_from=date_from, date_to=date_to))
        for row in job_results(job):
            db.session.merge(RepoStars(repo_id=repo.id, stars=row[0], year=row[1], day=row[2]))
        db.session.commit()

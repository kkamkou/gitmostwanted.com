from gitmostwanted.models.repo import Repo, RepoStars
from gitmostwanted.app import app, db, celery
from gitmostwanted.services import bigquery
from gitmostwanted.lib.bigquery.job import Job
from datetime import datetime, timedelta
from time import sleep


def results_of(j: Job):
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


@celery.task()
def stars_mature(num_days):
    date_from = (datetime.now() + timedelta(days=num_days * -1)).strftime('%Y-%m-%d')
    service = bigquery.instance(app)
    query = """
        SELECT
            COUNT(1) AS stars, YEAR(created_at) AS y, DAYOFYEAR(created_at) AS doy
        FROM
            TABLE_DATE_RANGE(
                githubarchive:day.events_, TIMESTAMP('{date_from}'), CURRENT_TIMESTAMP()
            )
        WHERE repo.id = {id} AND type IN ('WatchEvent', 'ForkEvent')
        GROUP BY y, doy
    """
    jobs = []

    repos = Repo.query.filter(Repo.mature.is_(True)).filter(Repo.status == 'new')
    for repo in repos:
        job = Job(service, query.format(id=repo.id, date_from=date_from), batch=True)
        job.execute()
        jobs.append((job, repo))

    for job in jobs:
        for row in results_of(job[0]):
            db.session.add(RepoStars(repo_id=job[1].id, stars=row[0], year=row[1], day=row[2]))

        job[1].status = 'unknown'

        db.session.commit()

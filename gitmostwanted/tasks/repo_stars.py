from datetime import datetime, timedelta
from time import sleep

from gitmostwanted.app import app, db, celery
from gitmostwanted.lib.bigquery.job import Job
from gitmostwanted.models.repo import Repo, RepoStars
from gitmostwanted.services import bigquery


def results_of(j: Job):  # @todo #0:15m copy-paste code in multiple tasks
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


@celery.task()
def stars_mature(num_days):
    service = bigquery.instance(app)

    jobs = []

    repos = Repo.query\
        .filter(Repo.mature.is_(True))\
        .filter(Repo.status == 'new')\
        .order_by(Repo.checked_at.asc())\
        .limit(100)  # donations will increase this number
    for repo in repos:
        query = query_stars_by_repo(
            repo_id=repo.id, date_from=datetime.now() + timedelta(days=num_days * -1),
            date_to=datetime.now()
        )

        job = Job(service, query, batch=True)
        job.execute()

        jobs.append((job, repo))

    for job in jobs:
        for row in results_of(job[0]):
            db.session.add(RepoStars(repo_id=job[1].id, stars=row[0], year=row[1], day=row[2]))

        status_old = job[1].status
        job[1].status = 'unknown'

        db.session.commit()

        app.logger.info(
            'Repository {0} got a new status {1} (was: {2})'
            .format(job[1].id, job[1].status, status_old)
        )


# @todo #192:1h move BQ queries to a separate place
def query_stars_by_repo(repo_id: int, date_from: datetime, date_to: datetime):
    query = """
        SELECT
            CAST(
                ROUND(
                    SQRT(
                        (
                            COUNTIF(type = 'ForkEvent') * 3 +
                            COUNTIF(type IN ('IssuesEvent', 'DiscussionEvent')) * 2 +
                            COUNTIF(type = 'WatchEvent') + 1
                        ) * (
                            COUNTIF(type = 'ReleaseEvent') * 5 +
                            COUNTIF(type IN ('PullRequestEvent', 'PullRequestReviewEvent')) * 3 +
                            COUNTIF(type = 'PushEvent') + 1
                        )
                    ) - 1
                ) AS INT64
            ) AS stars,
            EXTRACT(YEAR FROM created_at) AS y,
            EXTRACT(DAYOFYEAR FROM created_at) AS doy,
            EXTRACT(MONTH FROM created_at) AS mon
        FROM `githubarchive.day.2*`
        WHERE
            _TABLE_SUFFIX BETWEEN '{start_suffix}' AND '{end_suffix}'
            AND repo.id = {id}
            AND type IN (
                'WatchEvent', 'ForkEvent', 'ReleaseEvent',
                'PullRequestEvent', 'PullRequestReviewEvent',
                'IssuesEvent', 'DiscussionEvent', 'PushEvent'
            )
        GROUP BY y, mon, doy
    """
    return query.format(
        id=repo_id,
        start_suffix=date_from.strftime('%Y%m%d')[1:],
        end_suffix=date_to.strftime('%Y%m%d')[1:]
    )

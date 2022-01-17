from datetime import date, datetime, timedelta
from time import sleep

import arrow

from gitmostwanted.app import app, db, celery
from gitmostwanted.lib.bigquery.job import Job
from gitmostwanted.lib.github.api import repo_info
from gitmostwanted.models import report
from gitmostwanted.models.repo import Repo
from gitmostwanted.services import bigquery


def results_of(j: Job):
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


@celery.task()
def most_starred_day():
    most_starred_sync(
        'ReportAllDaily',
        """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM [githubarchive:day.{0}]
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """.format((date.today() - timedelta(1)).strftime('%Y%m%d'))
    )


@celery.task()
def most_starred_week():
    rng = arrow.utcnow().shift(days=-1).span('week')
    most_starred_sync(
        'ReportAllWeekly',
        """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM
                TABLE_DATE_RANGE([githubarchive:day.], TIMESTAMP('{0}'), TIMESTAMP('{1}'))
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """.format(rng[0].format('YYYYMMDD'), rng[1].format('YYYYMMDD'))
    )


@celery.task()
def most_starred_month():
    rng = arrow.utcnow().shift(days=-1).span('month')
    most_starred_sync(
        'ReportAllMonthly',
        """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM
                TABLE_DATE_RANGE([githubarchive:day.], TIMESTAMP('{0}'), TIMESTAMP('{1}'))
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """.format(rng[0].format('YYYYMMDD'), rng[1].format('YYYYMMDD'))
    )


def most_starred_sync(model_name: str, query: str):
    app.logger.info('Importing repos of %s (query: %s)', model_name, query)

    model = getattr(report, model_name)
    service = bigquery.instance(app)

    db.session.query(model).delete()

    job = Job(service, query)
    job.execute()

    for row in results_of(job):
        info, code = repo_info(row[1])
        if not info:
            continue

        db.session.merge(
            model(
                id=row[0],
                cnt_watch=row[2],
                repo=Repo(
                    id=info['id'],
                    created_at=datetime.strptime(info['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                    description=info['description'],
                    full_name=info['full_name'],
                    homepage=info['homepage'],
                    html_url=info['html_url'],
                    language=info['language'],
                    name=info['name']
                )
            )
        )

        app.logger.info(
            'Repository {0}({1}) has a new number of watchers {2}'
            .format(row[0], info['full_name'], row[2])
        )

    db.session.commit()

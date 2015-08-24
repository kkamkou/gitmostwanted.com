from gitmostwanted.github.api import repo_info
from gitmostwanted.app import app, db, celery
from gitmostwanted.services import bigquery
from gitmostwanted.bigquery.job import Job
from gitmostwanted.models.repo import Repo
from gitmostwanted.models import report
from datetime import date, datetime
from time import sleep


def job_results(j: Job):
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
            FROM [githubarchive:day.events_{0}]
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """.format(date.today().strftime('%Y%m%d'))
    )


@celery.task()
def most_starred_week():
    most_starred_sync(
        'ReportAllWeekly',
        """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM
                TABLE_DATE_RANGE(
                    githubarchive:day.events_,
                    DATE_ADD(CURRENT_TIMESTAMP(), -7, 'DAY'),
                    CURRENT_TIMESTAMP()
                )
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """
    )


@celery.task()
def most_starred_month():
    most_starred_sync(
        'ReportAllMonthly',
        """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM
                TABLE_DATE_RANGE(
                    githubarchive:day.events_,
                    DATE_ADD(CURRENT_TIMESTAMP(), -30, 'DAY'),
                    CURRENT_TIMESTAMP()
                )
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """
    )


def most_starred_sync(model_name: str, query: str):
    service = bigquery.instance(app)
    model = getattr(report, model_name)

    db.session.query(model).delete()

    for row in job_results(Job(service, query)):
        info = repo_info(row[1])
        if not info:
            continue

        db.session.merge(
            model(
                id=row[0],
                cnt_watch=row[2],
                repo=Repo(
                    id=info['id'],
                    name=info['name'],
                    language=info['language'],
                    full_name=info['full_name'],
                    description=info['description'],
                    html_url=info['html_url'],
                    homepage=info['homepage'],
                    created_at=datetime.strptime(info['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                )
            )
        )

    db.session.commit()

# pylint: disable=E1002
from datetime import date
from gitmostwanted.models.repo import Repo
from gitmostwanted.models import report
from gitmostwanted.bigquery.query import fetch
from gitmostwanted.app import app, db, celery
from gitmostwanted.github.api import repo_info


class ContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

celery.Task = ContextTask


@celery.task()
def most_starred_day():
    most_starred_sync({
        'query': """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM [githubarchive:day.events_{0}]
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """.format(date.today().strftime('%Y%m%d'))
    }, 'ReportAllDaily')


@celery.task()
def most_starred_week():
    most_starred_sync({
        'query': """
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
    }, 'ReportAllWeekly')


@celery.task()
def most_starred_month():
    most_starred_sync({
        'query': """
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
    }, 'ReportAllMonthly')


def most_starred_sync(body, model_name):
    response = fetch(body)
    for row in response:
        info = repo_info(row[1])
        repo = Repo(
            id=info['id'],
            name=info['name'],
            language=info['language'],
            full_name=info['full_name'],
            description=info['description'],
            html_url=info['html_url']
        )

        db.session.merge(repo)
        db.session.merge(getattr(report, model_name)(id=row[0], cnt_watch=row[2]))
        db.session.commit()


db.create_all()  # @todo remove it

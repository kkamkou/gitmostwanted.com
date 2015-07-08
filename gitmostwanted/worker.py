# pylint: disable=E1002
from datetime import date, datetime
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
    model = getattr(report, model_name)

    db.session.query(model).delete()

    for row in response:
        info = repo_info(row[1])
        if not info:
            continue

        homepage = info['homepage'].strip() if info['homepage'] else None
        if homepage and homepage.find('http') != 0:
            homepage = 'http://' + homepage

        db.session.merge(
            model(
                id=row[0],
                cnt_watch=row[2],
                repo=Repo(
                    id=info['id'],
                    name=info['name'],
                    language=info['language'],
                    full_name=info['full_name'],
                    description=info['description'][:250] if info['description'] else None,
                    html_url=info['html_url'],
                    homepage=homepage,
                    created_at=datetime.strptime(info['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                )
            )
        )

    db.session.commit()

"""
    SELECT COUNT(1), DAYOFYEAR(created_at) AS doy FROM
        TABLE_DATE_RANGE(
            githubarchive:day.events_,
            TIMESTAMP('2015-05-01'),
            TIMESTAMP('2015-06-30')
        )
    WHERE repo.id = 458058 AND type = 'WatchEvent' GROUP BY doy
"""

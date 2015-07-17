# pylint: disable=E1002
from gitmostwanted.models.repo import Repo, RepoStars
from gitmostwanted.models import report
from gitmostwanted.bigquery.job import Job
from gitmostwanted.bigquery.service import ServiceGmw
from gitmostwanted.app import app, db, celery
from gitmostwanted.github.api import repo_info
from datetime import date, datetime, timedelta
from time import sleep


class ContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)

celery.Task = ContextTask


def service_bigquery():
    cfg = app.config['GOOGLE_BIGQUERY']
    return ServiceGmw(cfg['account_name'], cfg['private_key_path'], cfg['project_id'])


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
    bigquery = service_bigquery()
    model = getattr(report, model_name)

    db.session.query(model).delete()

    for row in job_results(Job(bigquery, query)):
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


@celery.task()
def repos_stars(days_from, days_to):
    bigquery = service_bigquery()
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
        job = Job(bigquery, query.format(id=repo.id, date_from=date_from, date_to=date_to), batch=True)
        for row in job_results(job):
            db.session.merge(RepoStars(repo_id=repo.id, stars=row[0], year=row[1], day=row[2]))
        db.session.commit()

# pylint: disable=E1002
from datetime import date
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.report import ReportAllDaily
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
def most_starred_today():
    response = fetch({
        'query': """
            SELECT
                repo.id, repo.name, COUNT(1) AS cnt
            FROM [githubarchive:day.events_%s]
            WHERE type = 'WatchEvent'
            GROUP BY repo.id, repo.name
            ORDER BY cnt DESC
            LIMIT 50
        """ % date.today().strftime('%Y%m%d')
    })

    for row in response:
        info = repo_info(row[1])
        repo = Repo(
            id=info['id'],
            name=info['name'],
            language=info['language'],
            full_name=info['full_name'],
            description=info['description']
        )

        db.session.merge(repo)
        db.session.merge(ReportAllDaily(row[0], row[2]))
        db.session.commit()

db.create_all()  # @todo remove it

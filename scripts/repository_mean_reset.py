from datetime import datetime
from gitmostwanted.app import app, db
from gitmostwanted.lib.bigquery.job import Job
from gitmostwanted.models.repo import Repo, RepoMean, RepoStars
from gitmostwanted.services import bigquery
from gitmostwanted.tasks.repo_stars import query_stars_by_repo
from gitmostwanted.tasks.repo_status import last_known_mean, repo_mean
from time import sleep


def results_of(j: Job):  # @todo #0:15m copy-paste code in multiple tasks
    while not j.complete:
        app.logger.debug('The job is not complete, waiting...')
        sleep(10)
    return j.results


results = Repo.query\
    .filter(
        (Repo.last_reset_at < datetime(year=2017, month=8, day=31))
        | Repo.last_reset_at.is_(None)
    )\
    .filter(Repo.mature.is_(True))\
    .filter(Repo.stargazers_count > 1000)\
    .order_by(Repo.worth.desc())\
    .yield_per(10)\
    .all()
for result in results:
    now = datetime.now()
    service = bigquery.instance(app)
    query = query_stars_by_repo(
        repo_id=result.id, date_from=datetime(year=now.year, month=1, day=1),
        date_to=datetime(year=now.year, month=now.month-1, day=1)
    )

    job = Job(service, query)
    job.execute()

    cnt = 0
    lst = {}
    for row in results_of(job):
        key = '{} {}'.format(row[1], row[3])
        lst[key] = lst.get(key, ()) + ((int(row[2]), int(row[0])),)

        db.session.merge(RepoStars(repo_id=result.id, stars=row[0], year=row[1], day=row[2]))
        cnt += 1

    db.session.query(RepoMean).filter(RepoMean.repo_id == result.id).delete()
    db.session.commit()

    for key in lst.keys():
        avg = repo_mean(lst[key], 28, 4, last_known_mean(result.id))
        db.session.add(
            RepoMean(repo_id=result.id, created_at=datetime.strptime(key, '%Y %m'), value=avg)
        )
        db.session.commit()

    db.session.query(Repo).filter(Repo.id == result.id)\
        .update({Repo.status: 'unknown', Repo.last_reset_at: now})
    db.session.commit()

    app.logger.info('Repository %d has %d days', result.id, cnt)

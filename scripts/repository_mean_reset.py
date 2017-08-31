from datetime import datetime, timedelta
from gitmostwanted.app import app, log, db
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


results = Repo\
    .filter(Repo.mature.is_(True))\
    .filter(Repo.stargazers_count > 1000)\
    .order_by(RepoMean.repo_id.asc())\
    .yield_per(100)\
    .all()
for result in results:
    date_to = datetime.now()
    service = bigquery.instance(app)
    query = query_stars_by_repo(
        repo_id=result.repo_id, date_from=datetime.datetime(year=date_to.year, month=1, day=1),
        date_to=datetime.now()
    )

    job = Job(service, query)
    job.execute()

    cnt = 0
    lst = {}
    for row in results_of(job):
        key = '{} {}'.format(row[1], row[3])
        lst[key] = lst.get(key, ()) + ((row[0], row[0]),)

        db.session.merge(RepoStars(repo_id=repo_id, stars=row[0], year=row[1], day=row[2]))
        cnt += 1

    for val, yj in lst:
        avg = val  # call normalization
        date = datetime.datetime.strptime(yj, '%Y %j')

        # insert to the mean table

    db.session.query(Repo).filter(Repo.id == repo_id).update({Repo.status: 'unknown'})

    db.session.commit()

    print(cnt)

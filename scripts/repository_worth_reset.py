from gitmostwanted.app import log, db
from gitmostwanted.models.repo import Repo, RepoMean
from gitmostwanted.tasks.repo_metadata import is_worth_decreased


cache = {}
results = db.session.query(Repo, RepoMean) \
    .filter((Repo.id == RepoMean.repo_id) & Repo.mature.is_(True)) \
    .order_by(RepoMean.created_at.asc()) \
    .yield_per(100) \
    .all()
for result in results:
    repo, mean = result

    if repo.id not in cache:
        cache[repo.id] = {'prev': mean.value, 'worth': 3}
        continue

    prev, curr = cache[repo.id]['prev'], mean.value
    cache[repo.id]['prev'] = curr
    cache[repo.id]['worth'] += -1 if is_worth_decreased(curr, prev) else 1

    log.info(
        '#{0}: prev value is {1}, next value is {2} > worth is: {3} (now {4})'
            .format(repo.id, prev, curr, cache[repo.id]['worth'], repo.worth)
    )

    repo.worth = cache[repo.id]['worth']
    db.session.commit()

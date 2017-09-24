from gitmostwanted.app import log, db
from gitmostwanted.models.repo import Repo, RepoMean
from gitmostwanted.tasks.repo_metadata import is_worth_decreased
import sys


cache = {}
query = db.session.query(Repo, RepoMean)\
    .filter(Repo.id == RepoMean.repo_id)\
    .order_by(RepoMean.created_at.asc())\
    .yield_per(100)

if sys.argv[0] and sys.argv[0].isdigit():
    log.info('#{0} is used as the repository id'.format(sys.argv[0]))
    query = query.filter(Repo.id == int(sys.argv[0]))

results = query.all()
for result in results:
    repo, mean = result

    if repo.id not in cache:
        cache[repo.id] = {'prev': mean.value, 'worth': 3, 'mature': 0}
        continue

    prev, curr = cache[repo.id]['prev'], mean.value
    cache[repo.id]['mature'] += 1
    cache[repo.id]['prev'] = curr
    cache[repo.id]['worth'] += -1 if is_worth_decreased(curr, prev) else 1

    log.info(
        '#{0}: prev value is {1}, next value is {2} > worth is: {3} (now {4}); mature: {5}'
        .format(repo.id, prev, curr, cache[repo.id]['worth'], repo.worth, cache[repo.id]['mature'])
    )

    repo.worth = cache[repo.id]['worth']
    repo.mature = cache[repo.id]['mature'] > 2

    db.session.commit()

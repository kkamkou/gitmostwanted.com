from flask import Blueprint, g, render_template, request
from sqlalchemy.sql import func

from gitmostwanted.app import app, db
from gitmostwanted.models.repo import Repo, RepoMean, RepoTopics
from gitmostwanted.models.user import UserAttitude

repo_rating = Blueprint('repo_rating', __name__)


@repo_rating.route('/', defaults={'page': 1, 'sort_by': 'wanted', 'filter_worth_by': 'solid'})
@repo_rating.route('/top/<sort_by>/', defaults={'page': 1, 'filter_worth_by': 'solid'})
@repo_rating.route('/top/<sort_by>/<filter_worth_by>/<int:page>', defaults={'page': 1})
@repo_rating.route('/top/<sort_by>/<filter_worth_by>/<int:page>')
@repo_rating.route(
    '/topic/<topic>/', defaults={'page': 1, 'sort_by': 'wanted', 'filter_worth_by': 'solid'}
)
@repo_rating.route('/topic/<topic>/<sort_by>/<filter_worth_by>/<int:page>')
def top(page, sort_by, filter_worth_by, topic=None):
    query = Repo.filter_by_args(Repo.query, request.args).filter(Repo.mature.is_(True))
    velocity = func.coalesce(
        db.session.query(RepoMean.value)
        .filter(RepoMean.repo_id == Repo.id)
        .order_by(RepoMean.created_at.desc())
        .limit(1)
        .correlate(Repo)
        .scalar_subquery(),
        0.0
    )
    discovery = (
        (velocity * 10 + Repo.forks_count * 2 + Repo.subscribers_count * 5) * 1000.0 /
        (Repo.stargazers_count + 100)
    )
    sorts = {
        'wanted': [Repo.worth.desc(), discovery.desc(), Repo.stargazers_count.desc()],
        'momentum': [velocity.desc(), discovery.desc(), Repo.worth.desc()],
        'stars': [Repo.stargazers_count.desc()]
    }

    if filter_worth_by not in ('rising', 'solid'):
        filter_worth_by = 'solid'

    query = query.filter(
        (Repo.worth >= app.config['REPOSITORY_WORTH_SOLID']) if filter_worth_by == 'solid' else (
            (Repo.worth > app.config['REPOSITORY_WORTH_DEFAULT']) &
            (Repo.worth < app.config['REPOSITORY_WORTH_SOLID'])
        )
    )

    if topic:
        query = query.join(RepoTopics).filter(RepoTopics.title == topic)

    for f in [sort for sort in (sorts['wanted'] if sort_by not in sorts else sorts[sort_by])]:
        query = query.order_by(f)

    if not g.user:
        query = query.add_columns(db.null())
    else:
        query = UserAttitude.join_by_user_and_repo(query, g.user.id, Repo.id)\
            .add_columns(UserAttitude.attitude)
    query = query.add_columns(velocity.label('velocity'))

    entries = query.paginate(page=page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return top(entries.pages, sort_by, filter_worth_by, topic=topic)

    return render_template(
        'repository/top.html', languages=Repo.language_distinct(),
        repos=entries, page=page, sort_by=sort_by, filter_worth_by=filter_worth_by, topic=topic
    )

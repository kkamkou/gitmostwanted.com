from flask import Blueprint, g, render_template, request
from gitmostwanted.app import app, db
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo

repo_rating = Blueprint('repo_rating', __name__)


@repo_rating.route('/', defaults={'page': 1, 'sort_by': 'wanted', 'filter_worth_by': 'solid'})
@repo_rating.route('/top/<sort_by>/', defaults={'page': 1, 'filter_worth_by': 'solid'})
@repo_rating.route('/top/<sort_by>/<filter_worth_by>/<int:page>', defaults={'page': 1})
@repo_rating.route('/top/<sort_by>/<filter_worth_by>/<int:page>')
def top(page, sort_by, filter_worth_by):
    query = Repo.filter_by_args(Repo.query, request.args).filter(Repo.mature.is_(True))
    sorts = {
        'wanted': [Repo.worth.desc(), Repo.stargazers_count.desc()],
        'stars': [Repo.stargazers_count.desc()]
    }

    if filter_worth_by not in ('rising', 'solid'):
        filter_worth_by = 'solid'

    query = query.filter(
        Repo.worth >= (
            app.config['REPOSITORY_WORTH_SOLID'] if filter_worth_by == 'solid'
            else app.config['REPOSITORY_WORTH_DEFAULT'] + 1
        )
    )

    for f in [sort for sort in (sorts['wanted'] if sort_by not in sorts else sorts[sort_by])]:
        query = query.order_by(f)

    if not g.user:
        query = query.add_columns(db.null())
    else:
        query = UserAttitude.join_by_user_and_repo(query, g.user.id, Repo.id)\
            .add_columns(UserAttitude.attitude)

    entries = query.paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return top(entries.pages, sort_by, filter_worth_by)

    return render_template(
        'repository/top.html', languages=Repo.language_distinct(),
        repos=entries, page=page, sort_by=sort_by, filter_worth_by=filter_worth_by
    )

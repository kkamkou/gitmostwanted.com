from flask import Blueprint, g, request, render_template
from gitmostwanted.app import db
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo

repo_rating = Blueprint('repo_rating', __name__)


@repo_rating.route('/top/', defaults={'page': 1, 'sort_by': 'wanted'})
@repo_rating.route('/top/<sort_by>/', defaults={'page': 1})
@repo_rating.route('/top/<sort_by>/<int:page>')
def top(sort_by, page):
    query = Repo.filter_by_args(Repo.query, request.args).filter(Repo.worth > 2)
    sorts = {
        'wanted': [Repo.worth.desc(), Repo.stargazers_count.desc()],
        'stars': [Repo.stargazers_count.desc()]
    }

    for f in [sort for sort in (sorts['wanted'] if sort_by not in sorts else sorts[sort_by])]:
        query = query.order_by(f)

    if not g.user:
        query = query.add_columns(db.null())
    else:
        query = UserAttitude.join_by_user_and_repo(query, g.user.id, Repo.id)\
            .add_columns(UserAttitude.attitude)

    entries = query.paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return top(sort_by, entries.pages)

    return render_template(
        'repository/top.html', languages=Repo.language_distinct(),
        repos=entries, page=page, sort_by=sort_by
    )

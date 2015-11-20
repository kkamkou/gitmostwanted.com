from flask import Blueprint, g, request, render_template
from gitmostwanted.app import db
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo

repo_rating = Blueprint('repo_rating', __name__)


@repo_rating.route('/top/', defaults={'page': 1})
@repo_rating.route('/top/<int:page>')
def top(page):
    q = Repo.filter_by_args(Repo.query, request.args)\
        .filter(Repo.worth > 4)\
        .order_by(Repo.worth.desc())\
        .order_by(Repo.stargazers_count.desc())

    if not g.user:
        q = q.add_columns(db.null())
    else:
        q = UserAttitude.join_by_user_and_repo(q, g.user.id, Repo.id)\
            .add_columns(UserAttitude.attitude)

    entries = q.paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return top(entries.pages)

    return render_template(
        'repository/top.html', repos=entries, page=page, languages=Repo.language_distinct()
    )

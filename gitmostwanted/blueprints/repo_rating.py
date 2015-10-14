from flask import Blueprint, g, request, render_template
from gitmostwanted.app import db
from gitmostwanted.blueprints.mixin import repository_filtered
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo

repo_rating = Blueprint('repo_rating', __name__)


@repo_rating.route('/top/', defaults={'page': 1})
@repo_rating.route('/top/<int:page>')
def top(page):
    if not g.user:
        q = Repo.query.add_columns(db.null())
    else:
        q = Repo.query \
            .add_columns(UserAttitude.attitude) \
            .outerjoin(
                UserAttitude,
                (UserAttitude.user_id == g.user.id) & (UserAttitude.repo_id == Repo.id)
            )

    q = q.filter(Repo.worth > 4) \
        .order_by(Repo.worth.desc()) \
        .order_by(Repo.created_at.asc())

    l = Repo.language_distinct()
    q = repository_filtered(request, l, Repo, q)

    entries = q.paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return top(entries.pages)

    return render_template('repository/top.html', repos=entries, page=page, languages=l)

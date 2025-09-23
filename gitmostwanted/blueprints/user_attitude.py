from flask import abort, Blueprint, g, jsonify, render_template, request
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.app import db

user_attitude = Blueprint('user_attitude', __name__)


def verify_attitude(attitude):
    return attitude in ['like', 'dislike', 'neutral']


@user_attitude.before_request
def verify_user():
    if not g.user:
        return abort(403)


@user_attitude.route('/attitude/<int:repo_id>/<attitude>')
def change(repo_id, attitude):
    if not verify_attitude(attitude):
        return abort(403)

    if not Repo.query.get(repo_id):
        return abort(404)

    db.session.merge(UserAttitude(user_id=g.user.id, repo_id=repo_id, attitude=attitude))
    db.session.commit()

    return jsonify(attitude=attitude)


@user_attitude.route('/unchecked/', defaults={'page': 1})
@user_attitude.route('/unchecked/<int:page>')
def list_unchecked(page):
    return list_by_attitude(None, page)


@user_attitude.route('/attitude/<attitude>', defaults={'page': 1})
@user_attitude.route('/attitude/<attitude>/<int:page>')
def list_attitude(attitude, page):
    if not verify_attitude(attitude):
        return abort(403)
    return list_by_attitude(attitude, page)


def list_by_attitude(attitude, page):
    q = UserAttitude.join_by_user_and_repo(Repo.query, g.user.id, Repo.id)\
        .add_columns(UserAttitude.attitude if attitude else db.null())\
        .filter(UserAttitude.attitude == attitude) \
        .order_by(Repo.worth.desc())\
        .order_by(Repo.stargazers_count.desc())

    q = Repo.filter_by_args(q, request.args)

    entries = q.paginate(page=page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return list_by_attitude(attitude, entries.pages)

    return render_template(
        'repository/attitude.html', repos=entries, attitude=attitude,
        languages=Repo.language_distinct()
    )

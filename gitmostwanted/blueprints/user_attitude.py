from flask import abort, Blueprint, g, make_response, render_template_string, render_template
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

def paginate(filter_by, page):
    return Repo.query\
        .filter(filter_by)\
        .outerjoin(
            UserAttitude,
            db.and_(
                UserAttitude.user_id == g.user.id,
                UserAttitude.repo_id == Repo.id
            )
        )\
        .paginate(page if page > 0 else 1, per_page=20, error_out=False)

@user_attitude.route('/attitude/<int:repo_id>/<attitude>')
def change(repo_id, attitude):
    if not verify_attitude(attitude):
        return abort(403)

    if not Repo.query.get(repo_id):
        return abort(404)

    db.session.merge(UserAttitude(user_id=g.user.id, repo_id=repo_id, attitude=attitude))
    db.session.commit()

    return make_response(render_template_string('Ok'), 204)


@user_attitude.route('/unchecked/', defaults={'page': 1})
@user_attitude.route('/unchecked/<int:page>')
def unchecked(page):
    entries = paginate(UserAttitude.repo_id.is_(None), page)
    if entries.pages < entries.page:
        return unchecked(entries.pages)

    return render_template('attitude.html', repos=entries)


@user_attitude.route('/attitude/<attitude>', defaults={'page': 1})
@user_attitude.route('/attitude/<attitude>/<int:page>')
def list_by_attitude(attitude, page):
    if not verify_attitude(attitude):
        return abort(403)

    entries = paginate(UserAttitude.attitude == attitude, page)
    if entries.pages < entries.page:
        return list(attitude, entries.pages)

    return render_template('attitude.html', repos=entries, attitude=attitude)

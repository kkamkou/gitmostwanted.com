from flask import abort, Blueprint, g, make_response, render_template_string, render_template
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.app import db

user_attitude = Blueprint('user_attitude', __name__)


@user_attitude.before_request
def user_verify():
    if not g.user:
        return abort(403)


@user_attitude.route('/attitude/<int:repo_id>/<attitude>')
def change(repo_id, attitude):
    if attitude not in ['like', 'dislike', 'neutral']:
        return abort(403)

    if not Repo.query.get(repo_id):
        return abort(404)

    db.session.merge(UserAttitude(user_id=g.user.id, repo_id=repo_id, attitude=attitude))
    db.session.commit()

    return make_response(render_template_string('Ok'), 204)


@user_attitude.route('/unchecked/')
def unchecked():
    entries = Repo.query\
        .filter(UserAttitude.repo_id.is_(None))\
        .outerjoin(
            UserAttitude,
            db.and_(
                UserAttitude.user_id == g.user.id,
                UserAttitude.repo_id == Repo.id
            )
        )
    return render_template('unchecked.html', repos=entries)

db.create_all()  # @todo remove it


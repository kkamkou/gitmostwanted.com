from flask import Blueprint, render_template
from gitmostwanted.models.user import User, UserAttitude
from gitmostwanted.models.repo import Repo

user_profile = Blueprint('user_profile', __name__)


@user_profile.route('/<name>')
def profile_view(name):
    entity = User.query.filter_by(username=name).first_or_404()
    repos = Repo.query.join(UserAttitude)\
        .filter(UserAttitude.user_id == entity.id)\
        .filter(UserAttitude.attitude == 'like')\
        .order_by(Repo.language.desc())
    return render_template('profile.html', account=entity, repos=repos)

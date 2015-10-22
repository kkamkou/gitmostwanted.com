from flask import Blueprint, g, render_template, make_response, render_template_string, session
from gitmostwanted.models.user import User, UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.lib.github.api import user_starred, user_starred_star
user_profile = Blueprint('user_profile', __name__)


@user_profile.route('/<name>')
def overview(name):
    entity = User.query.filter_by(username=name).first_or_404()
    repos = Repo.query.join(UserAttitude)\
        .filter(UserAttitude.user_id == entity.id)\
        .filter(UserAttitude.attitude == 'like')\
        .order_by(Repo.language.desc())
    return render_template('profile.html', account=entity, repos=repos)


@user_profile.route('/profile/github/sync')
def github_sync():
    starred, code = user_starred()
    if starred:
        attitudes = UserAttitude.query\
            .filter(UserAttitude.user == g.user)\
            .filter(UserAttitude.attitude == 'like')

        token, secret = session.get('github_token')

        [
            user_starred_star(r.repo.full_name, token) for r in attitudes
            if filter(lambda x: x['full_name'] == r.repo.full_name, starred)
        ]
    return make_response(render_template_string('Ok'), 204)

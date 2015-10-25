import flask
from gitmostwanted.lib.github.api import user_starred, user_starred_star
from gitmostwanted.models.user import User, UserAttitude
from gitmostwanted.models.repo import Repo

user_profile = flask.Blueprint('user_profile', __name__)


@user_profile.route('/<name>')
def overview(name):
    entity = User.query.filter_by(username=name).first_or_404()
    repos = Repo.query.join(UserAttitude)\
        .filter(UserAttitude.user_id == entity.id)\
        .filter(UserAttitude.attitude == 'like')\
        .order_by(Repo.language.desc())
    return flask.render_template('profile.html', account=entity, repos=repos)


@user_profile.route('/profile/github/sync')
def github_sync():
    token, secret = flask.session.get('github_token', (None, None))
    if not token:
        return flask.abort(403)

    starred, code = user_starred()
    if starred:
        attitudes = UserAttitude.query\
            .filter(UserAttitude.user == flask.g.user)\
            .filter(UserAttitude.attitude == 'like')

        lst = [user_starred_star(r.repo.full_name, token) for r in attitudes
               if filter(lambda x: x['full_name'] == r.repo.full_name, starred)]

        flask.flash(
            '{} repositories were successfully starred'.format(
                len([c for r, c in lst if c == 204])
            ), 'success'
        )
    return flask.redirect(flask.url_for('user_profile.overview', name=flask.g.user.username))

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
    token, scope = flask.session.get('oauth_access_token')
    if not token:
        return flask.abort(403)

    redirect = flask.redirect(flask.url_for('user_profile.overview', name=flask.g.user.username))

    if 'public_repo' not in scope:
        flask.flash('This action requires additional permissions', 'alert')
        return redirect

    starred, code = user_starred(token)
    if not starred:
        flask.flash('Unable to read from your profile', 'alert')
        return redirect

    # @todo! move this functionality to celery
    attitudes = UserAttitude.query\
        .filter(UserAttitude.user == flask.g.user)\
        .filter(UserAttitude.attitude == 'like')

    lst = [user_starred_star(r.repo.full_name, token) for r in attitudes
           if not [x for x in starred if x['full_name'] == r.repo.full_name]]

    flask.flash(
        '{} repositories were successfully starred'.format(
            len([c for r, c in lst if c == 204])
        ), 'success'
    )

    return redirect

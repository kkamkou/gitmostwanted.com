import flask
from gitmostwanted.app import db
from gitmostwanted.tasks.github import repo_starred_star
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
    if not flask.g.user:
        return flask.abort(403)

    token, scope = flask.session.get('oauth_access_token')
    if not token:
        return flask.abort(403)

    if 'public_repo' not in scope:
        flask.flash('This action requires additional permissions', 'alert')
    else:
        repo_starred_star.delay(flask.g.user.id, token)
        flask.flash('Synchronisation is successfully queued', 'success')

    return flask.redirect(flask.url_for('user_profile.overview', name=flask.g.user.username))


@user_profile.route('/profile/remove')
def remove():
    if not flask.g.user:
        return flask.abort(403)

    im_sure = flask.request.args.get('im_sure', False)
    if im_sure == 'True':
        db.session.delete(flask.g.user)
        db.session.commit()

    return flask.redirect(flask.url_for('user_oauth.logout'))

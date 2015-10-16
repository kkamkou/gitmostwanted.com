from flask import g, redirect, request, session, url_for
from gitmostwanted.blueprints.user_attitude import user_attitude
from gitmostwanted.blueprints.user_profile import user_profile
from gitmostwanted.blueprints.repo_trending import repo_trending
from gitmostwanted.blueprints.repo_rating import repo_rating
from gitmostwanted.services import oauth as service_oauth
from gitmostwanted.models.user import User
from gitmostwanted.app import app, db

app.register_blueprint(repo_trending)
app.register_blueprint(repo_rating)
app.register_blueprint(user_attitude)
app.register_blueprint(user_profile)
app.jinja_env.add_extension('jinja2.ext.do')

oauth = service_oauth.instance(app)


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/oauth/login')
def oauth_login():
    return oauth.github.authorize(
        callback=url_for('oauth_authorized', next=url_next(), _external=True)
    )


@app.route('/oauth/authorized')
def oauth_authorized():
    next_url = url_next() or url_for('/')

    resp = oauth.github.authorized_response()
    if resp is None:
        return redirect(next_url)

    session.permanent = True
    session['github_token'] = (resp['access_token'], '')
    me = oauth.github.get('user')
    session['user_id'] = user_get_or_create(me.data['id'], me.data['email'], me.data['login']).id

    return redirect(next_url)


@oauth.github.tokengetter
def oauth_github_token():
    return session.get('github_token')


@app.before_request
def user_load_from_session():
    ignored = ['/logout']
    if str(request.url_rule) in ignored:
        return None

    g.user = User.query.get(session['user_id']) if 'user_id' in session else None


def user_get_or_create(uid, uemail, uname):
    entity = User.query.filter_by(github_id=uid).first()
    if entity:
        return entity
    entity = User(github_id=uid, username=uname, email=uemail or None)
    db.session.add(entity)
    db.session.commit()
    return entity


def url_next():
    return request.args.get('next') or request.referrer or None

if __name__ == '__main__':
    app.run(host='0.0.0.0')

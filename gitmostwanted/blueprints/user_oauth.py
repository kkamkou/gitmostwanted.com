from flask import Blueprint, g, redirect, request, session, url_for
from gitmostwanted.services import oauth as service_oauth
from gitmostwanted.models.user import User
from gitmostwanted.app import app, db

user_oauth = Blueprint('user_oauth', __name__)
oauth = service_oauth.instance(app)

# @todo move the before_request method to a general place or a middleware
@app.before_request
def load_user_from_session():
    if str(request.url_rule) in ['/logout']:
        return None
    g.user = User.query.get(session['user_id']) if 'user_id' in session else None

# @todo move the after_request method to a general place or a middleware
@app.after_request
def browser_cache_flush(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache'
    return response


@user_oauth.route('/logout')
def logout():
    session.pop('oauth_access_token', None)
    session.pop('user_id', None)
    return redirect('/')


@user_oauth.route('/oauth/login')
def login():
    return oauth.github.authorize(
        callback=url_for('user_oauth.authorized', next=url_next(), _external=True),
        scope=request.args.get('scope')
    )


@user_oauth.route('/oauth/authorized')
def authorized():
    next_url = url_next() or url_for('/')

    resp = oauth.github.authorized_response()
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session.permanent = True
    session['oauth_access_token'] = (resp['access_token'], resp['scope'].split(','))

    me = oauth.github.get('user')
    session['user_id'] = user_get_or_create(me.data['id'], me.data['email'], me.data['login']).id

    return redirect(next_url)


@oauth.github.tokengetter
def tokengetter():
    return session.get('oauth_access_token')


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

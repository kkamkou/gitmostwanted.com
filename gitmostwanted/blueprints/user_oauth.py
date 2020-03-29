from flask import Blueprint, g, redirect, request, session, url_for

from gitmostwanted.app import app, db
from gitmostwanted.models.user import User
from gitmostwanted.services import oauth as service_oauth

user_oauth = Blueprint('user_oauth', __name__)

oauth = service_oauth.instance(app)
oauth.register(
    'github', **app.config['GITHUB_OAUTH'],
    fetch_token=lambda: session.get('oauth_access_token')
)


# @todo #1:15min move before_request method to a general place or a middleware
@app.before_request
def load_user_from_session():
    if str(request.url_rule) in ['/logout']:
        return None
    g.user = User.query.get(session['user_id']) if 'user_id' in session else None


# @todo #2:15min move after_request method to a general place or a middleware
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
    return oauth.github.authorize_redirect(
        redirect_uri=url_for('user_oauth.authorized', next=url_next(), _external=True),
        scope=request.args.get('scope')
    )


@user_oauth.route('/oauth/authorized')
def authorized():
    next_url = url_next() or url_for('/')

    resp = oauth.github.authorize_access_token()
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session.permanent = True
    session['oauth_access_token'] = (resp['access_token'], resp['scope'].split(','))

    result = oauth.github.get('user')
    if result:
        json = result.json()
        user = user_get_or_create(json['id'], json['email'], json['login'])
        session['user_id'] = user.id

    return redirect(next_url)


def user_get_or_create(uid: int, user_email: str, user_name: str):
    entity = User.query.filter_by(github_id=uid).first()
    if not entity:
        entity = User(github_id=uid, username=user_name, email=user_email or None)
        db.session.add(entity)
        db.session.commit()
    return entity


def url_next():
    return request.args.get('next') or request.referrer or None

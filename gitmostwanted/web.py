from flask import g, render_template, redirect, request, session, url_for
from gitmostwanted.blueprints.user_attitude import user_attitude
from gitmostwanted.blueprints.user_profile import user_profile
from gitmostwanted.blueprints.repo_rating import repo_rating
from gitmostwanted.blueprints.mixin import repository_filtered
from gitmostwanted.services import oauth as service_oauth
from gitmostwanted.models.user import User, UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.models import report
from gitmostwanted.app import app, db


app.register_blueprint(user_attitude)
app.register_blueprint(user_profile)
app.register_blueprint(repo_rating)
app.jinja_env.add_extension('jinja2.ext.do')

oauth = service_oauth.instance(app)


@app.route('/', defaults={'rng': 'day'})
@app.route('/trending/<rng>/')
def index(rng):
    map_list = {'day': 'ReportAllDaily', 'week': 'ReportAllWeekly', 'month': 'ReportAllMonthly'}
    if rng not in map_list:
        rng = 'day'

    model = getattr(report, map_list[rng])
    lngs = Repo.language_distinct()

    if not g.user:
        query = model.query.join(Repo).add_columns(db.null())
    else:
        query = model.query\
            .join(Repo)\
            .add_columns(UserAttitude.attitude)\
            .outerjoin(
                UserAttitude,
                (UserAttitude.user_id == g.user.id) & (UserAttitude.repo_id == Repo.id)
            )

    query = repository_filtered(request, lngs, Repo, query)\
        .order_by(model.cnt_watch.desc())

    return render_template('index.html', entries=query, languages=lngs)


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/oauth/login')
def oauth_login():
    return oauth.github.authorize(
        callback=url_for('oauth_authorized', next=url_next(), _external=True)
    )


@app.route('/oauth/authorized')
def oauth_authorized():
    next_url = url_next() or url_for('index')

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

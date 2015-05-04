from flask import g, render_template, redirect, request, session, url_for
from gitmostwanted.blueprints.user_attitude import user_attitude
from gitmostwanted.app import app, db, oauth
from gitmostwanted.models.user import User, UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.models import report


app.register_blueprint(user_attitude)


@app.route('/', defaults={'rng': 'day'})
@app.route('/trending/<rng>/')
def index(rng):
    map_list = {
        'day': 'ReportAllDaily',
        'week': 'ReportAllWeekly',
        'month': 'ReportAllMonthly'
    }

    if rng not in map_list:
        rng = 'day'

    model = getattr(report, map_list[rng])

    if not g.user:
        q = model.query.add_columns(db.null())
    else:
        q = model.query\
            .join(Repo)\
            .add_columns(UserAttitude.attitude)\
            .outerjoin(
                UserAttitude,
                db.and_(
                    UserAttitude.user_id == g.user.id,
                    UserAttitude.repo_id == Repo.id
                )
            )

    return render_template(
        'index.html', range=rng, entries=q.order_by(db.desc(model.cnt_watch))
    )


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

    session['github_token'] = (resp['access_token'], '')
    me = oauth.github.get('user')
    session['user_id'] = user_get_or_create(me.data['email'], me.data['id'], me.data['login']).id

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


def user_get_or_create(uemail, uid, uname):
    entity = User.query.filter_by(email=uemail).first()
    if entity:
        return entity

    entity = User(email=uemail, github_id=uid, username=uname)
    db.session.add(entity)
    db.session.commit()
    return entity


def url_next():
    return request.args.get('next') or request.referrer or None

if __name__ == '__main__':
    app.run(host='0.0.0.0')

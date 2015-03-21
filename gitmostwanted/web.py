from gitmostwanted.app import app, db, oauth
from gitmostwanted.models.user import User
from flask import render_template, redirect, request, session, url_for, jsonify


@app.route('/')
def index():
    if 'github_token' in session:
        me = oauth.github.get('user')
        if not User.query.filter_by(email=me.data['email']).count():
            db.session.add(User(me.data['email'], me.data['login']))
            db.session.commit()
            return jsonify(me.data)
    return render_template('index.html')


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

    return redirect(next_url)


@oauth.github.tokengetter
def oauth_github_token():
    return session.get('github_token')


def url_next():
    return request.args.get('next') or request.referrer or None

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')

from gitmostwanted.app import app, oauth
from flask import render_template, redirect, request, session, url_for


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/oauth/login')
def oauth_login():
    url_next = request.args.get('next') or request.referrer or None
    url_cb = url_for('oauth_authorized', next=url_next, _external=True)
    return oauth.github.authorize(callback=url_cb)


@app.route('/oauth/authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')

    resp = oauth.github.authorized_response()
    if resp is None:
        return redirect(next_url)

    session['github_token'] = (resp['access_token'], '')

    return redirect(next_url)


@oauth.github.tokengetter
def oauth_github_token():
    return session.get('github_token')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

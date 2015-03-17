from gitmostwanted.app import app, db, github
from flask import flash, render_template, redirect, request, session, url_for

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/oauth/cb')
def oauth_cb():
    return redirect(url_for('index'))


@app.route('/oauth/login')
def oauth_login():
    url_next = request.args.get('next') or request.referrer or None
    return github.authorize(callback=url_for('oauth_authorized', next=url_next))


@app.route('/oauth/authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')

    resp = github.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['github_token'] = (resp['oauth_token'], resp['oauth_token_secret'])
    session['github_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

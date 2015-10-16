from gitmostwanted.app import app
from gitmostwanted.blueprints import\
    user_oauth, user_profile, user_attitude, repo_rating, repo_trending

app.register_blueprint(user_oauth.user_oauth)
app.register_blueprint(repo_trending.repo_trending)
app.register_blueprint(repo_rating.repo_rating)
app.register_blueprint(user_attitude.user_attitude)
app.register_blueprint(user_profile.user_profile)

app.jinja_env.add_extension('jinja2.ext.do')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

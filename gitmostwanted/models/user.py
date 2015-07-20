from gitmostwanted.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80))
    github_id = db.Column(db.BigInteger, unique=True)


class UserAttitude(db.Model):
    __tablename__ = 'users_attitude'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_users_id', ondelete='CASCADE'),
        primary_key=True
    )
    repo_id = db.Column(
        db.BigInteger,
        db.ForeignKey('repos.id', name='fk_repos_id', ondelete='CASCADE'),
        primary_key=True, index=True
    )
    attitude = db.Column(db.Enum('like', 'dislike', 'neutral'), nullable=False)

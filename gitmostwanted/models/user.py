from gitmostwanted.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80))
    github_id = db.Column(db.BigInteger, unique=True)


class UserAttitude(db.Model):
    __tablename__ = 'users_attitude'

    user = db.relationship('User')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_users_id', ondelete='CASCADE'),
        primary_key=True
    )
    repo = db.relationship('Repo', lazy=False)
    repo_id = db.Column(
        db.BigInteger,
        db.ForeignKey('repos.id', name='fk_repos_id', ondelete='CASCADE'),
        primary_key=True, index=True
    )
    attitude = db.Column(db.Enum('like', 'dislike', 'neutral'), nullable=False)

    @classmethod
    def join_by_user_and_repo(cls, query, user_id: int, repo_id: int):
        return query.outerjoin(cls, (cls.user_id == user_id) & (cls.repo_id == repo_id))

    @classmethod
    def liked_by_user(cls, user_id: int):
        return cls.query.filter(cls.user_id == user_id).filter(cls.attitude == 'like')

from gitmostwanted.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80))
    github_id = db.Column(db.BigInteger, unique=True)

    def __init__(self, email, github_id, username='Unknown'):
        self.email = email
        self.github_id = github_id
        self.username = username

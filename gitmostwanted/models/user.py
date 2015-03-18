from gitmostwanted.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=True)
    github_id = db.Column(db.BigInteger, unique=True)

    def __init__(self, email, username):
        self.email = email
        self.username = username

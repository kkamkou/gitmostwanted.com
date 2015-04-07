from gitmostwanted.app import db


class Repo(db.Model):
    __tablename__ = 'repos'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80))
    language = db.Column(db.String(20))
    full_name = db.Column(db.String(120))
    description = db.Column(db.String(250))
    html_url = db.Column(db.String(150))

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

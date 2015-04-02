from gitmostwanted.app import db
from gitmostwanted.models.repo import Repo


class ReportAllDaily(db.Model):
    id = db.Column(db.BigInteger, db.ForeignKey('repos.id'), primary_key=True)
    repo = db.relationship(Repo, uselist=False)
    cnt_watch = db.Column(db.Integer)

    def __init__(self, rid, cnt_watch):
        self.id = rid
        self.cnt_watch = cnt_watch

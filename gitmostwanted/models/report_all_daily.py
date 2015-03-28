from gitmostwanted.app import db


class ReportAllDaily(db.Model):
    repo_id = db.Column(db.BigInteger, primary_key=True)
    repo_name = db.Column(db.String(100), unique=True)
    repo_cnt_watch = db.Column(db.Integer)

    def __init__(self, rid, name, **kwargs):
        self.repo_id = rid
        self.repo_name = name

        for k in kwargs.keys():
            self.__dict__['repo_' + k] = kwargs[k]

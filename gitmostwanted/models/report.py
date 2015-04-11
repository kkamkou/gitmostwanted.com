from gitmostwanted.app import db
from gitmostwanted.models.repo import Repo
from sqlalchemy.ext.declarative import declared_attr


class ReportBase(db.Model):
    __abstract__ = True

    @declared_attr
    def id(self):
        return db.Column(db.BigInteger, db.ForeignKey('repos.id'), primary_key=True)

    @declared_attr
    def repo(self):
        return db.relationship(Repo, uselist=False)

    cnt_watch = db.Column(db.Integer)


class ReportAllDaily(ReportBase):
    __tablename__ = 'report_all_daily'


class ReportAllWeekly(ReportBase):
    __tablename__ = 'report_all_weekly'

class ReportAllMonthly(ReportBase):
    __tablename__ = 'report_all_monthly'

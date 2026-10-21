from sqlalchemy.ext.declarative import declared_attr

from gitmostwanted.app import db
from gitmostwanted.models.repo import Repo


class ReportBase(db.Model):
    __abstract__ = True

    @declared_attr
    def id(self):
        return db.Column(db.BigInteger, db.ForeignKey('repos.id'), primary_key=True)

    @declared_attr
    def repo(self):
        return db.relationship(Repo, uselist=False, lazy='joined')

    cnt_watch = db.Column(db.Integer, nullable=False)


class ReportAllDaily(ReportBase):
    __tablename__ = 'report_all_daily'


class ReportAllWeekly(ReportBase):
    __tablename__ = 'report_all_weekly'


class ReportAllMonthly(ReportBase):
    __tablename__ = 'report_all_monthly'


class ReportAllQuarterly(ReportBase):
    __tablename__ = 'report_all_quarterly'


class ReportAllYearly(ReportBase):
    __tablename__ = 'report_all_yearly'

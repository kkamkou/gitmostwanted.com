from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from sqlalchemy.sql import expression
from gitmostwanted.app import db
from datetime import datetime


class Repo(db.Model):
    __tablename__ = 'repos'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(20))
    full_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250))
    html_url = db.Column(db.String(150), nullable=False)
    homepage = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, nullable=False, index=True)
    mature = db.Column(db.Boolean, nullable=False, server_default=expression.false(), index=True)
    worth = db.Column(TINYINT(display_width=1), nullable=False, server_default='3', index=True)
    status_updated_at = db.Column(db.DateTime)
    status = db.Column(
        db.Enum('promising', 'new', 'unknown', 'deleted', 'hopeless'),
        server_default='new', nullable=False, index=True
    )

    def __setattr__(self, key, value):
        if key == 'status' and self.status != value:
            if value not in ('promising', 'new', 'unknown', 'deleted', 'hopeless'):
                raise ValueError('Unknown status provided')
            self.status_updated_at = datetime.now()
        super().__setattr__(key, value)

    @staticmethod
    def language_distinct():
        if not hasattr(Repo.language_distinct, 'memoize'):
            q = db.session.query(Repo.language).distinct().filter(Repo.language.isnot(None))
            setattr(Repo.language_distinct, 'memoize', q.all())
        return getattr(Repo.language_distinct, 'memoize')


class RepoStars(db.Model):
    __tablename__ = 'repos_stars'

    repo_id = db.Column(
        db.BigInteger,
        db.ForeignKey('repos.id', name='fk_repos_stars_repo_id', ondelete='CASCADE'),
        primary_key=True
    )
    stars = db.Column(SMALLINT(display_width=4, unsigned=True), nullable=False)
    year = db.Column(
        SMALLINT(display_width=4, unsigned=True),
        autoincrement=False, nullable=False, primary_key=True
    )
    day = db.Column(
        SMALLINT(display_width=3, unsigned=True),
        autoincrement=False, nullable=False, primary_key=True
    )

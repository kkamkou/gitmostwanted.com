from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.sql import expression
from werkzeug.datastructures import ImmutableMultiDict

from gitmostwanted.app import app, db
from gitmostwanted.lib.regex import SearchTerm
from gitmostwanted.lib.status import Status
from gitmostwanted.lib.text import TextWithoutSmilies, TextNormalized
from gitmostwanted.lib.url import Url


class RepoTopics(db.Model):
    __tablename__ = 'repos_topics'
    __table_args__ = (UniqueConstraint('repo_id', 'title', name='uc_repos_topics_repo_id_title'),)

    id = db.Column(db.BigInteger, primary_key=True)
    repo_id = db.Column(
        db.BigInteger,
        db.ForeignKey('repos.id', name='fk_repos_topics_repo_id', ondelete='CASCADE'),
        nullable=False
    )
    title = db.Column(db.String(30), nullable=False)


class Repo(db.Model):
    __tablename__ = 'repos'

    id = db.Column(db.BigInteger, primary_key=True)
    checked_at = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, nullable=False, index=True)
    description = db.Column(db.String(250))
    forks_count = db.Column(INTEGER(unsigned=True), nullable=False, server_default='0', index=True)
    full_name = db.Column(db.String(120), nullable=False)
    homepage = db.Column(db.String(150))
    html_url = db.Column(db.String(150), nullable=False)
    language = db.Column(db.String(25))
    license = db.Column(db.String(20), index=True)
    last_reset_at = db.Column(db.DateTime, index=True)
    mature = db.Column(db.Boolean, nullable=False, server_default=expression.false(), index=True)
    name = db.Column(db.String(80), nullable=False)
    open_issues_count = db.Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    size = db.Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    stargazers_count = db.Column(
        INTEGER(unsigned=True), nullable=False, server_default='0', index=True
    )
    status = db.Column(
        db.Enum('promising', 'new', 'unknown', 'deleted', 'hopeless'),
        server_default='new', nullable=False, index=True
    )
    status_updated_at = db.Column(db.DateTime)
    subscribers_count = db.Column(
        INTEGER(unsigned=True), nullable=False, server_default='0', index=True
    )
    topics = db.relationship(RepoTopics, cascade='all, delete-orphan')
    worth = db.Column(
        SMALLINT(display_width=2), index=True, nullable=False,
        server_default=str(app.config['REPOSITORY_WORTH_DEFAULT'])
    )
    worth_max = db.Column(SMALLINT(display_width=2), nullable=False, server_default='0')

    def __setattr__(self, key, value):
        if key == 'status' and self.status != value:
            value = str(Status(value))
            self.status_updated_at = datetime.now()

        if key == 'homepage':
            value = str(Url(value[:150])) if value else None

        if key == 'description':
            value = str(TextWithoutSmilies(str(TextNormalized(value[:250])))) if value else None

        if key == 'worth' and self.worth_max < value:
            self.worth_max = value

        super().__setattr__(key, value)

    @classmethod
    def filter_by_args(cls, q, args: ImmutableMultiDict):
        lang = args.get('lang')
        if lang != 'All' and (lang,) in cls.language_distinct():
            q = q.filter(cls.language == lang)

        status = args.get('status')
        if status in ('promising', 'hopeless'):
            q = q.filter(cls.status == status)

        if bool(args.get('mature')):
            q = q.filter(cls.mature.is_(True))

        try:
            q = q.filter(cls.full_name.like(str(SearchTerm(args.get('term', '')))))
        except ValueError:
            pass

        return q

    @staticmethod
    def language_distinct():
        if not hasattr(Repo.language_distinct, 'memoize'):
            q = db.session.query(Repo.language).distinct().filter(Repo.language.isnot(None))
            setattr(Repo.language_distinct, 'memoize', sorted(q.all()))
        return getattr(Repo.language_distinct, 'memoize')

    @classmethod
    def get_one_by_full_name(cls, name):
        return cls.query.filter(cls.full_name == name).first()


class RepoStars(db.Model):
    __tablename__ = 'repos_stars'

    repo_id = db.Column(
        db.BigInteger, db.ForeignKey('repos.id', name='fk_repos_stars_repo_id', ondelete='CASCADE'),
        primary_key=True
    )
    stars = db.Column(
        SMALLINT(display_width=4, unsigned=True),
        nullable=False
    )
    year = db.Column(
        SMALLINT(display_width=4, unsigned=True),
        autoincrement=False, nullable=False, primary_key=True
    )
    day = db.Column(
        SMALLINT(display_width=3, unsigned=True),
        autoincrement=False, nullable=False, primary_key=True
    )


class RepoMean(db.Model):
    __tablename__ = 'repos_mean'

    repo = db.relationship(Repo)
    repo_id = db.Column(
        db.BigInteger, db.ForeignKey('repos.id', name='fk_repos_mean_repo_id', ondelete='CASCADE'),
        primary_key=True
    )
    created_at = db.Column(
        db.Date,
        default=datetime.today().strftime('%Y-%m-%d'), nullable=False, primary_key=True
    )
    value = db.Column(db.Float(), nullable=False)

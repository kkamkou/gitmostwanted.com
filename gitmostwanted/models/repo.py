from gitmostwanted.app import db

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

    @staticmethod
    def language_distinct():
        if not hasattr(Repo.language_distinct, 'memoize'):
            q = db.session.query(Repo.language).distinct().filter(Repo.language.isnot(None))
            setattr(Repo.language_distinct, 'memoize', q.all())
        return getattr(Repo.language_distinct, 'memoize')

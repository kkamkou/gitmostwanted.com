from flask.ext.sqlalchemy import SQLAlchemy


def instance(app):
    return SQLAlchemy(app)

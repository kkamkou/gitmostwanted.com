from flask.ext.sqlalchemy import SQLAlchemy


def instance(app):
    """:rtype: SQLAlchemy"""
    return SQLAlchemy(app)

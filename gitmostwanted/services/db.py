from flask_sqlalchemy import SQLAlchemy


def instance(app):
    """:rtype: SQLAlchemy"""
    return SQLAlchemy(app)

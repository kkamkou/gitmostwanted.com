from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import event, exc


def instance(app):
    """:rtype: SQLAlchemy"""
    db = SQLAlchemy(app)

    if app.testing:
        return db

    @event.listens_for(db.engine, 'checkout')
    def checkout(dbapi_con, con_record, con_proxy):
        try:
            try:
                dbapi_con.ping(False)
            except TypeError:
                app.logger.debug('MySQL connection died. Restoring...')
                dbapi_con.ping()
        except dbapi_con.OperationalError as e:
            app.logger.warning(e)
            if e.args[0] in (2006, 2013, 2014, 2045, 2055):
                raise exc.DisconnectionError()
            else:
                raise

    return db

"""
Application for running the DAO API
"""

import datetime
import jsonpickle
import os

from flask import Flask

# pylint: disable=W0621
def create_app():
    """Config for the app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://docker:{}@{}:{}/{}'.format(
            os.environ['DB_PASSWORD'],
            os.environ['DB_PORT_5432_TCP_ADDR'],
            os.environ['DB_PORT_5432_TCP_PORT'],
            os.environ['DB_NAME'])

    from models.db_connection import db as db_conn
    db_conn.init_app(app)

    from dao import APP
    app.register_blueprint(APP)

    return app

# pylint: disable=C0103
if __name__ == "__main__":

    app = create_app()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    # pylint: disable=W0232
    class DatetimeHandler(jsonpickle.handlers.BaseHandler):
        """Custom handler to get datetimes as ISO dates"""
        def flatten(self, obj, data):   # pylint: disable=C0111,W0613,R0201
            return obj.isoformat()

    jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)
    jsonpickle.handlers.registry.register(datetime.date, DatetimeHandler)

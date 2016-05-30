"""
Application for running the DAO API
"""

import datetime
import ConfigParser
import os
import jsonpickle

from flask import Flask

from permissions import set_up_permissions

# pylint: disable=W0621
def create_app():
    """Config for the app"""
    config = ConfigParser.ConfigParser()
    config.read('/webapp/environment_config.ini')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://docker:{}@{}:{}/{}'.format(
            config.get('DATABASE', 'DB_PASSWORD'),
            os.environ['DB_PORT_5432_TCP_ADDR'],
            os.environ['DB_PORT_5432_TCP_PORT'],
            config.get('DATABASE', 'DB_NAME'))

    from models.db_connection import db as db_conn
    db_conn.init_app(app)

    from dao import APP
    app.register_blueprint(APP)

    return app

# pylint: disable=invalid-name
if __name__ == "__main__":

    app = create_app()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    # pylint: disable=no-init
    class DatetimeHandler(jsonpickle.handlers.BaseHandler):
        """Custom handler to get datetimes as ISO dates"""
        def flatten(self, obj, data):   # pylint: disable=missing-docstring,W0613,R0201
            return obj.isoformat()

    jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)
    jsonpickle.handlers.registry.register(datetime.date, DatetimeHandler)

    set_up_permissions(commit=True)

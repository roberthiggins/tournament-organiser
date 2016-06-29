"""
Application for running the DAO API
"""

import datetime
import os
import jsonpickle

from flask import Flask

from permissions import set_up_permissions

# pylint: disable=W0621
def create_app():
    """Config for the app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://docker:{}@{}:{}/{}'.format(
            os.environ['DATABASE_PASSWORD'],
            os.environ['DATABASE_PORT_5432_TCP_ADDR'],
            os.environ['DATABASE_PORT_5432_TCP_PORT'],
            os.environ['POSTGRES_DB'])

    from models.db_connection import db as db_conn
    db_conn.init_app(app)

    from dao import APP
    from feedback import FEEDBACK
    from user import USER
    app.register_blueprint(APP)
    app.register_blueprint(FEEDBACK, url_prefix='/feedback')
    app.register_blueprint(USER, url_prefix='/user')

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

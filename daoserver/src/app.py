"""
Application for running the DAO API
"""

import datetime
import os
import jsonpickle

from flask import Flask, make_response

from controllers.dao import APP
from controllers.feedback import FEEDBACK
from controllers.tournament import TOURNAMENT
from controllers.tournament_entry import ENTRY
from controllers.tournament_round import TOURNAMENT_ROUND
from controllers.user import USER
from models.authentication import PermissionDeniedException
from models.dao.db_connection import db
from models.permissions import set_up_permissions

# pylint: disable=W0621
def create_app():
    """Config for the app"""
    app = Flask(__name__)
    db_container = os.environ['DB_CONTAINER']
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://docker:{}@{}:{}/{}'.format(
            os.environ['DATABASE_PASSWORD'],
            os.environ['{}_PORT_5432_TCP_ADDR'.format(db_container)],
            os.environ['{}_PORT_5432_TCP_PORT'.format(db_container)],
            os.environ['POSTGRES_DB'])

    db.init_app(app)

    app.register_blueprint(APP)
    app.register_blueprint(FEEDBACK, url_prefix='/feedback')
    app.register_blueprint(TOURNAMENT, url_prefix='/tournament')
    app.register_blueprint(TOURNAMENT_ROUND,
                           url_prefix='/tournament/<tournament_id>/rounds')
    app.register_blueprint(ENTRY,
                           url_prefix='/tournament/<tournament_id>/entry')
    app.register_blueprint(USER, url_prefix='/user')

    @app.errorhandler(PermissionDeniedException)
    # pylint: disable=unused-variable
    def permission_denied(err):
        """Permission denied (as opposed to auth failed)"""
        print type(err).__name__
        print err
        import traceback
        traceback.print_exc()
        return make_response(str(err), 403)

    @app.errorhandler(RuntimeError)
    @app.errorhandler(ValueError)
    @app.errorhandler(TypeError)
    # pylint: disable=unused-variable
    def input_error(err):
        """Input errors"""
        print type(err).__name__
        print err
        import traceback
        traceback.print_exc()
        return make_response(str(err), 400)

    @app.errorhandler(Exception)
    # pylint: disable=unused-variable
    def unknown_error(err):
        """All other exceptions are essentially just raised with logging"""
        print type(err).__name__
        print err
        import traceback
        traceback.print_exc()
        return make_response(str(err), 500)

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

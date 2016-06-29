"""
Users for the site. Note this is separate from an entry in a tournament.
"""

import jsonpickle

from flask import Blueprint, make_response, Response

from models.account import Account

USER = Blueprint('USER', __name__)

@USER.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 400)

@USER.route('/<u_name>', methods=['GET'])
def user_details(u_name=None):
    """
    GET to get account details in url form
    TODO security
    """
    # pylint: disable=no-member
    user = Account.query.filter_by(username=u_name).first()
    if user is None:
        raise ValueError('Cannot find user {}'.format(u_name))

    return Response(
        jsonpickle.encode({u_name: user.contact_email}, unpicklable=False),
        mimetype='application/json')

"""
Users for the site. Note this is separate from an entry in a tournament.
"""

import jsonpickle

from flask import Blueprint, make_response, Response

from controllers.request_variables import enforce_request_variables
from models.authentication import check_auth
from models.dao.account import Account, add_account

USER = Blueprint('USER', __name__)

@USER.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 400)

@USER.route('/login', methods=['POST'])
@enforce_request_variables('inputUsername', 'inputPassword')
def login():
    """
    POST to login
    Expects:
        - inputUsername
        - inputPassword
    """
    # pylint: disable=E0602
    return make_response(
        "Login successful" if check_auth(inputUsername, inputPassword) \
        else "Login unsuccessful",
        200)

def validate_user_email(email):
    """
    Validates email based on django validator
    """
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# pylint: disable=undefined-variable
@USER.route('', methods=['POST'])
@enforce_request_variables('username', 'email', 'password1', 'password2')
def create():
    """
    POST to add an account
    Expects:
        - username
        - email
        - password1
        - password2
    """
    if not validate_user_email(email):
        return make_response("This email does not appear valid", 400)

    if password1 != password2:
        return make_response("Please enter two matching passwords", 400)

    if Account.username_exists(username):
        return make_response("A user with the username {} already exists! \
            Please choose another name".format(username), 400)

    add_account(username, email, password1)

    return make_response('<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(username, email), 200)

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

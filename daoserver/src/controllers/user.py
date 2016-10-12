"""
Users for the site. Note this is separate from an entry in a tournament.
"""

from flask import Blueprint, g

from controllers.request_helpers import enforce_request_variables, \
json_response, requires_auth, text_response
from models.user import User

USER = Blueprint('USER', __name__)

@USER.url_value_preprocessor
# pylint: disable=unused-argument
def get_user(endpoint, values):
    """Attempt to retrieve user from URL"""
    g.user = User(values.pop('username', None))

@USER.route('/actions', methods=['GET'])
@requires_auth
@json_response
def available_actions():
    """Returns a list of actions the user can perform"""
    return g.user.available_actions()

# pylint: disable=undefined-variable
@USER.route('/login', methods=['POST'])
@text_response
@enforce_request_variables('inputPassword')
def login():
    """POST to login"""
    g.user.login(inputPassword)
    return 'Login successful'

# pylint: disable=undefined-variable
@USER.route('', methods=['POST'])
@text_response
@enforce_request_variables('email', 'password1', 'password2')
def create():
    """POST to add an account"""
    g.user.add_account({
        'email': email,
        'password1': password1,
        'password2': password2
    })
    return '<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(g.user.username, email)

@USER.route('', methods=['GET'])
@requires_auth
@json_response
def user_details():
    """
    GET to get account details in json form
    """
    return g.user.details()

"""
Users for the site. Note this is separate from an entry in a tournament.
"""

import re
from flask import Blueprint, g

from controllers.request_helpers import enforce_request_variables, \
json_response, requires_auth, text_response
from models.authentication import check_auth
from models.dao.account import Account, add_account

USER = Blueprint('USER', __name__)

@USER.url_value_preprocessor
# pylint: disable=unused-argument
def get_user(endpoint, values):
    """Attempt to retrieve user from URL"""
    g.username = values.pop('username', None)
    if g.username:
        # pylint: disable=no-member
        g.account = Account.query.filter_by(username=g.username).first()

# pylint: disable=undefined-variable
@USER.route('/login', methods=['POST'])
@text_response
@enforce_request_variables('inputPassword')
def login():
    """
    POST to login
    Expects:
        - inputPassword
    """
    if g.account is None:
        raise ValueError('Username or password incorrect')

    return "Login successful" if check_auth(g.username, inputPassword) \
        else "Login unsuccessful"

# pylint: disable=undefined-variable
@USER.route('', methods=['POST'])
@text_response
@enforce_request_variables('email', 'password1', 'password2')
def create():
    """
    POST to add an account
    Expects:
        - email
        - password1
        - password2
    """
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        raise ValueError('This email does not appear valid')

    if password1 != password2 or not password1:
        raise ValueError('Please enter two matching passwords')

    if g.account:
        raise ValueError('A user with the username {} already exists! \
            Please choose another name'.format(g.username))

    add_account(g.username, email, password1)

    return '<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(g.username, email)

@USER.route('', methods=['GET'])
@requires_auth
@json_response
def user_details():
    """
    GET to get account details in url form
    TODO security
    """
    if g.account is None:
        raise ValueError('Cannot find user {}'.format(g.username))

    return {g.username: g.account.contact_email}

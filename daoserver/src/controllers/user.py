"""
Users for the site. Note this is separate from an entry in a tournament.
"""

from flask import Blueprint

from controllers.request_helpers import enforce_request_variables, \
json_response, text_response
from models.authentication import check_auth
from models.dao.account import Account, add_account

USER = Blueprint('USER', __name__)

@USER.route('/login', methods=['POST'])
@text_response
@enforce_request_variables('inputUsername', 'inputPassword')
def login():
    """
    POST to login
    Expects:
        - inputUsername
        - inputPassword
    """
    # pylint: disable=E0602
    return "Login successful" if check_auth(inputUsername, inputPassword) \
        else "Login unsuccessful"

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
@text_response
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
        raise ValueError('This email does not appear valid')

    if password1 != password2:
        raise ValueError('Please enter two matching passwords')

    if Account.username_exists(username):
        raise ValueError('A user with the username {} already exists! \
            Please choose another name'.format(username))

    add_account(username, email, password1)

    return '<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(username, email)

@USER.route('/<u_name>', methods=['GET'])
@json_response
def user_details(u_name=None):
    """
    GET to get account details in url form
    TODO security
    """
    # pylint: disable=no-member
    user = Account.query.filter_by(username=u_name).first()
    if user is None:
        raise ValueError('Cannot find user {}'.format(u_name))

    return {u_name: user.contact_email}

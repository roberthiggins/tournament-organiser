"""Module to enforce auth on requests coming from the client apps."""

from functools import wraps
from flask import request, Response
from passlib.hash import sha256_crypt

from models.dao.account import AccountSecurity

class PermissionDeniedException(Exception):
    """No permissions for requested action"""
    pass

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    if not username or not password:
        raise ValueError("Enter username and password")

    # pylint: disable=no-member
    creds = AccountSecurity.query.filter_by(id=username).first().password
    if sha256_crypt.verify(password, creds):
        return True

    return False

def requires_auth(func):
    """Decorator to check login creds for a request"""
    @wraps(func)
    def decorated(*args, **kwargs):
        """decorator"""
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return func(*args, **kwargs)
    return decorated

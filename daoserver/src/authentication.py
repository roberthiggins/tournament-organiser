"""Module to enforce auth on requests coming from the client apps."""

from functools import wraps
from flask import request, Response
from passlib.hash import sha256_crypt

from models.account import AccountSecurity

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        if not username or not password:
            raise RuntimeError("Enter username and password")

        creds = AccountSecurity.query.filter_by(id=username).first().password
        if not sha256_crypt.verify(password, creds):
            raise RuntimeError("Username or password incorrect")
        return True
    except RuntimeError:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(func):
    """Decorator to check login creds for a request"""
    @wraps(func)
    def decorated(*args, **kwargs):
        """decorator"""
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)
    return decorated

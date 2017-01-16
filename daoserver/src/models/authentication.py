"""Module to enforce auth on requests coming from the client apps."""

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
        return False

    try:
        # pylint: disable=no-member
        creds = AccountSecurity.query.filter_by(id=username).first().password
        if sha256_crypt.verify(password, creds):
            return True
    except AttributeError:
        return False

    return False

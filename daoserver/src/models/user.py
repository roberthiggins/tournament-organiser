"""
Model of a user
"""

import re

from models.authentication import check_auth
from models.dao.account import Account, add_account

# pylint: disable=no-member

def must_exist_in_db(func):
    """ A decorator that requires the tournament exists in the db"""
    def wrapped(self, *args, **kwargs): # pylint: disable=missing-docstring
        if not self.exists_in_db:
            print 'Cannot find user {}'.format(self.username)
            raise ValueError('Cannot find user {}'.format(self.username))
        return func(self, *args, **kwargs)
    return wrapped

def strip_none(array):
    """Strip all elements that are None"""
    return [x for x in array if x is not None]

class User(object):
    """A User"""

    def __init__(self, username):
        self.username = username
        self.exists_in_db = self.get_dao() is not None

    def get_dao(self):
        """Convenience method to recover DAO"""
        return Account.query.filter_by(username=self.username).first()

    def add_account(self, email, password1, password2):
        """Add an account"""
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('This email does not appear valid')

        if password1 != password2 or not password1:
            raise ValueError('Please enter two matching passwords')

        if self.exists_in_db:
            raise ValueError('A user with the username {} already exists! \
                Please choose another name'.format(self.username))

        add_account(self.username, email, password1)
        self.exists_in_db = True

    def login(self, password):
        """Log the user in"""
        if Account.query.filter_by(username=self.username).first() is None or \
        not check_auth(self.username, password):
            raise ValueError('Username or password incorrect')

    @must_exist_in_db
    def details(self):
        """ username and email for contact and identification"""
        return {self.username: self.get_dao().contact_email}

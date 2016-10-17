"""
ORM module for accounts
"""
# pylint: disable=invalid-name

from passlib.hash import sha256_crypt

from models.dao.db_connection import db

class Account(db.Model):
    """Basic user account"""
    __tablename__ = 'account'
    username = db.Column(db.String(30), primary_key=True)
    contact_email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False, default='')
    last_name = db.Column(db.String(100), nullable=False, default='')
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)

    # pylint: disable=too-many-arguments
    def __init__(self, username, contact_email, first_name=None, last_name=None,
                 is_superuser=False):
        self.username = username
        self.contact_email = contact_email
        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser

    def __repr__(self):
        return '<Account ({}, {}, {}, {}, {})>'.format(
            self.username,
            self.first_name,
            self.last_name,
            self.contact_email,
            self.is_superuser)

    @staticmethod
    def username_exists(username):
        """Check if a username exists for a player"""
        # pylint: disable=no-member
        return Account.query.filter_by(username=username).first() is not None

class AccountSecurity(db.Model):
    """Authentication for users"""

    __tablename__ = 'account_security'
    id = db.Column(
        db.String(30),
        db.ForeignKey(Account.username),
        primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    account = db.relationship(Account, backref='security')


    def __init__(self, username, password):
        self.id = username
        self.password = sha256_crypt.encrypt(password)

    def __repr__(self):
        return '<AccountSecurity ({}, {})>'.format(self.id, self.password)

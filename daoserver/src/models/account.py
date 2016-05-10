"""
ORM module for accounts
"""
# pylint: disable=invalid-name

from passlib.hash import sha256_crypt

from models.db_connection import db, write_to_db

class Account(db.Model):
    """Basic user account"""
    __tablename__ = 'account'
    username = db.Column(db.String(30), primary_key=True)
    contact_email = db.Column(db.String(100), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, username, contact_email, is_superuser=False):
        self.username = username
        self.contact_email = contact_email
        self.is_superuser = is_superuser

    def __repr__(self):
        return '<Account ({}, {}, {})>'.format(
            self.username,
            self.contact_email,
            self.is_superuser)

    def delete(self):
        """Remove from db"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def add_account(account):
        """Add an account. Username cannot exist"""
        write_to_db(Account(account['user_name'], account['email']))
        write_to_db(AccountSecurity(account['user_name'], account['password']))

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

    def __init__(self, username, password):
        self.id = username
        self.password = sha256_crypt.encrypt(password)

    def __repr__(self):
        return '<AccountSecurity ({}, {})>'.format(self.id, self.password)

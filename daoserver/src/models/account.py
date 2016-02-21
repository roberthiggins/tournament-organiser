"""
ORM module for accounts
"""

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def username_exists(username):
        """Check if a username exists for a player"""
        return Account.query.filter_by(username=username).first() is not None

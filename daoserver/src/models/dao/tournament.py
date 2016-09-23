"""
ORM module for a tournament
"""
# pylint: disable=invalid-name

from models.dao.account import Account
from models.dao.db_connection import db
from models.dao.permissions import ProtectedObject

class Tournament(db.Model):
    """Represents a row in the tournament table"""
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    num_rounds = db.Column(db.Integer, default=0)
    protected_object_id = db.Column(
        db.Integer,
        db.ForeignKey(ProtectedObject.id),
        nullable=False)
    creator_username = db.Column(
        db.String(50),
        db.ForeignKey(Account.username),
        nullable=False)

    protected_object = db.relationship(ProtectedObject)
    creator = db.relationship(Account)

    def __init__(self, name):
        if not name.strip():
            raise ValueError('Enter a valid name')
        self.name = name
        self.protected_object = ProtectedObject()
        db.session.add(self.protected_object)
        db.session.flush()

    def __repr__(self):
        return '<Tournament {}>'.format(self.name)

"""
ORM module for a tournament
"""
# pylint: disable=invalid-name

from models.db_connection import db
from models.permissions import ProtectedObject

class Tournament(db.Model):
    """Represents a row in the tournament table"""
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime, nullable=False)
    num_rounds = db.Column(db.Integer, default=0)
    protected_object_id = db.Column(
        db.Integer,
        db.ForeignKey(ProtectedObject.id))
    protected_object = db.relationship(ProtectedObject)

    def __init__(self, name):
        self.name = name
        self.protected_object = ProtectedObject()
        db.session.add(self.protected_object)
        db.session.flush()

    def __repr__(self):
        return '<Tournament {}>'.format(self.name)

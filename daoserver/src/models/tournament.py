"""
ORM module for a tournament
"""

from flask.ext.sqlalchemy import SQLAlchemy
from models.protected_object import ProtectedObject

db = SQLAlchemy()

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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tournament {}>'.format(self.name)

    def write(self):
        """To the DB"""
        try:
            protected_object = ProtectedObject()
            protected_object.write()
            self.protected_object_id = protected_object.id
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

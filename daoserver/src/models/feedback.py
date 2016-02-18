"""
ORM module for feedback from the user
"""
# pylint: disable=C0103

import datetime

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
    """
    A Row in the feedback table. Used for submitting improvement ideas, etc.
    """

    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text, unique=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, feedback):
        self.feedback = feedback

    def __repr__(self):
        return '<User {} - {} - {}>'.format(self.id, self.time, self.feedback)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
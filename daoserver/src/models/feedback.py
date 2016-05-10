"""
ORM module for feedback from the user
"""
# pylint: disable=invalid-name

import datetime

from models.db_connection import db

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

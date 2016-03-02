"""
ORM module for a round in a tournament
"""
# pylint: disable=C0103

from flask.ext.sqlalchemy import SQLAlchemy
from models.tournament import Tournament

db = SQLAlchemy()

class TournamentRound(db.Model):
    """A row in the tournament_round table"""

    __tablename__ = 'tournament_round'
    id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(
        db.String(50),
        db.ForeignKey(Tournament.name),
        nullable=False)
    ordering = db.Column(db.Integer, default=1, nullable=False)
    mission = db.Column(db.String(20), default='TBA', nullable=False)

    def __init__(self, tournament, round_num, mission=None):
        self.tournament_name = tournament
        self.ordering = round_num
        self.mission = mission

    def __repr__(self):
        return '<TournamentRound ({}, {}, {})>'.format(
            self.tournament_name,
            self.ordering,
            self.mission)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def delete(self):
        """Remove from db"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

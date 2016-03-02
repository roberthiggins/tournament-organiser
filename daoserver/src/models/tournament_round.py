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
    id = db.Column(db.Integer, db.Sequence('tournament_round_id_seq'))
    tournament_name = db.Column(
        db.String(50),
        db.ForeignKey(Tournament.name),
        primary_key=True)
    ordering = db.Column(db.Integer, default=1, primary_key=True)
    mission = db.Column(db.String(20), default='TBA', nullable=False)

    def __init__(self, tournament, round_num, mission=None):
        self.tournament_name = tournament
        self.mission = mission

        round_num = int(round_num)
        if round_num <= 0:
            raise ValueError('Round ording must be a positive integer')
        if round_num > Tournament.query.filter_by(name=tournament).\
            first().num_rounds + 1:
                raise ValueError('Tournament {} only has {} rounds'.format(
                    tournament,
                    round_num
                ))
        self.ordering = round_num

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

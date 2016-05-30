"""
ORM module for a round in a tournament
"""
# pylint: disable=invalid-name

from models.db_connection import db
from models.tournament import Tournament

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
    tournament = db.relationship(Tournament,
                                 backref=db.backref('rounds', lazy='dynamic'))

    def __init__(self, tournament, round_num, mission=None):
        self.tournament_name = tournament
        self.mission = mission

        round_num = int(round_num)
        if round_num <= 0:
            raise ValueError('Round ording must be a positive integer')
        # pylint: disable=no-member
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

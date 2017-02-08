"""
ORM module for a tournament's entry matching_strategy
"""
# pylint: disable=invalid-name

from models.dao.db_connection import db
from models.dao.tournament import Tournament

class MatchingStrategy(db.Model):
    """
    A Row in the matching_strategy table.
    """

    __tablename__ = 'matching_strategy'
    id = db.Column(db.String(20), primary_key=True)

    def __init__(self, name):
        self.id = name

    def __repr__(self):
        return '<MatchStrat {}>'.format(self.id)

class TournamentMatchingStrategy(db.Model):
    """
    A join table fo Tournament and MatchingStrategy
    """

    __tablename__ = 'tournament_matching_strategy'
    tournament_id = db.Column(db.Integer, db.ForeignKey(Tournament.id),
                              primary_key=True)
    matching_strategy = db.Column(db.String(20),
                                  db.ForeignKey(MatchingStrategy.id),
                                  primary_key=True)

    tournament = db.relationship(Tournament, \
        backref=db.backref('matching_strategy', lazy='dynamic'))
    strategy = db.relationship(MatchingStrategy)

    def __init__(self, tourn, strat):
        self.tournament_id = tourn
        self.matching_strategy = strat

    def __repr__(self):
        return '<TournMatchStrat {}, {}>'.format(self.tournament.name,
                                                 self.matching_strategy)

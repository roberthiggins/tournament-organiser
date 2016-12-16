"""
ORM module for a game in a tournament
"""

# pylint: disable=invalid-name,no-member

from models.dao.db_connection import db
from models.dao.permissions import ProtectedObject
from models.dao.tournament_round import TournamentRound

class TournamentGame(db.Model):
    """
    A Tournament is has many TournamentGame. Each game has many GameEntry
    """
    __tablename__ = 'game'
    id = db.Column(db.Integer, db.Sequence('game_id_seq'), unique=True)
    tournament_round_id = db.Column(db.Integer,
                                    db.ForeignKey(TournamentRound.id,
                                                  ondelete='CASCADE'),
                                    primary_key=True)
    table_num = db.Column(db.Integer, primary_key=True)
    protected_object_id = db.Column(db.Integer,
                                    db.ForeignKey(ProtectedObject.id))
    score_entered = db.Column(db.Boolean)

    protected_object = db.relationship(ProtectedObject)
    tournament_round = db.relationship(TournamentRound, \
        backref=db.backref('games', lazy='dynamic'))

    def __init__(self, round_id, table_num):
        self.tournament_round_id = round_id
        self.table_num = table_num
        self.protected_object = ProtectedObject()
        db.session.add(self.protected_object)
        db.session.flush()
        self.protected_object_id = self.protected_object.id
        self.score_entered = False

    def __repr__(self):
        return '<TournamentGame {}, {}, {}>'.format(
            self.id, self.tournament_round_id, self.table_num)

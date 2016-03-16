"""
ORM module for a game in a tournament
"""

# pylint: disable=invalid-name,no-member

from models.db_connection import db
from models.tournament import Tournament
from models.protected_object import ProtectedObject

class TournamentGame(db.Model):
    """
    A Tournament is has many TournamentGame. Each game has many GameEntry
    """
    __tablename__ = 'game'
    id = db.Column(db.Integer, db.Sequence('game_id_seq'), unique=True)
    round_num = db.Column(db.Integer, primary_key=True)
    tourn = db.Column(db.String(50),
                      db.ForeignKey(Tournament.name),
                      primary_key=True)
    table_num = db.Column(db.Integer, primary_key=True)
    protected_object_id = db.Column(db.Integer,
                                    db.ForeignKey(ProtectedObject.id))
    score_entered = db.Column(db.Boolean)

    protected_object = db.relationship(ProtectedObject)

    def __init__(self, tournament, round_num, table_num):
        self.tourn = tournament
        self.round_num = round_num
        self.table_num = table_num
        self.protected_object = ProtectedObject()
        self.protected_object.write()
        self.protected_object_id = self.protected_object.id
        self.score_entered = False

    def __repr__(self):
        return '<TournamentGame {}, {}, {}>'.format(
            self.tournament, self.round_num, self.table_num)

    def write(self):
        """To the DB"""
        try:

            if self.protected_object is not None:
                self.protected_object.write()

            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

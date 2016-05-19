"""
ORM module for an entrant in a game
"""
# pylint: disable=invalid-name

from models.db_connection import db
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame

class GameEntrant(db.Model):
    """A TournamentGame typically has 2+ GameEntrant"""

    __tablename__ = 'game_entrant'
    game_id = db.Column(db.Integer,
                        db.ForeignKey(TournamentGame.id),
                        primary_key=True)
    entrant_id = db.Column(db.Integer,
                           db.ForeignKey(TournamentEntry.id),
                           primary_key=True)

    game = db.relationship(TournamentGame,
                           backref=db.backref('entrants', lazy='dynamic'))
    entrant = db.relationship(TournamentEntry)

    def __init__(self, game_id, entrant_id):
        self.game_id = game_id
        self.entrant_id = entrant_id

    def __repr__(self):
        return '<GameEntrant {}, {}>'.format(self.game_id, self.entrant_id)

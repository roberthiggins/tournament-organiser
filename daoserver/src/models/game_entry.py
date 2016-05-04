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

    def __init__(self, game, entrant):
        self.game = game
        self.entrant = entrant

    def __repr__(self):
        return '<GameEntrant {}, {}>'.format(self.game.id, self.entrant.id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

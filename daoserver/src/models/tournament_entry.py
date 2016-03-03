"""
ORM moduel for an entry in a tournament
"""

# pylint: disable=invalid-name

from models.account import Account
from models.db_connection import db
from models.tournament import Tournament

class TournamentEntry(db.Model):
    """
    A tournament is composed of entries who play each other. This is distinct
    from users or accounts as there may be multiple players on a team, etc.
    """

    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(30), db.ForeignKey(Account.username))
    tournament_id = db.Column(db.String(50), db.ForeignKey(Tournament.name))

    tournament = db.relationship(Tournament, backref='entries')
    account = db.relationship(Account, backref='account')

    def __init__(self, player_id, tournament_id):
        self.player_id = player_id
        self.tournament_id = tournament_id

    def __repr__(self):
        return '<TournamentEntry ({}, {}, {})>'.format(
            self.id,
            self.player_id,
            self.tournament_id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

"""
ORM module for a registration of a user into a tournament
"""
# pylint: disable=invalid-name, no-member

from sqlalchemy.sql.expression import and_

from models.account import Account
from models.db_connection import db
from models.tournament import Tournament

class TournamentRegistration(db.Model):
    """A row in the registration table"""

    __tablename__ = 'registration'
    player_id = db.Column(db.String(30),
                          db.ForeignKey(Account.username),
                          primary_key=True)
    tournament_id = db.Column(db.Integer,
                              db.ForeignKey(Tournament.id),
                              primary_key=True)
    has_paid = db.Column(db.Boolean, nullable=False, default=False)
    turned_up = db.Column(db.Boolean, nullable=False, default=False)
    list_accept = db.Column(db.Boolean, nullable=False, default=False)

    account = db.relationship(Account, backref='registrations')
    tournament = db.relationship(Tournament, backref='registrations')

    def __init__(self, player_id, tournament_name):
        self.player_id = player_id
        self.tournament_id = Tournament.query.filter_by(name=tournament_name).\
        first().id

    def __repr__(self):
        return '<TournamentRegistration ({}, {}, {})>'.format(
            self.player_id,
            self.tournament_id,
            self.tournament.name)

    def clashes(self):
        """
        Check to see if the registration clashes with a registration to
        another tournament.

        You cannot enter two tournaments for the same day.
        """

        candidate = Tournament.query.filter_by(id=self.tournament_id).first()
        clash = TournamentRegistration.query.join(Tournament).filter(
            and_(TournamentRegistration.player_id == self.player_id,
                 Tournament.date == candidate.date)).first()

        if clash is None:
            return False

        if clash.tournament_id == self.tournament_id:
            raise ValueError("You've already applied to {}".format(
                clash.tournament.name))

        raise ValueError("%s clashes with %s that you are registered \
            for already" % (candidate.name, clash.tournament.name))

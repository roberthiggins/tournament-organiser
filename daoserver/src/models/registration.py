"""
ORM module for a registration of a user into a tournament
"""
# pylint: disable=invalid-name

from sqlalchemy.sql.expression import and_

from models.account import Account
from models.db_connection import db
from models.tournament import Tournament

# pylint: disable=no-member
class TournamentRegistration(db.Model):
    """A row in the registration table"""

    __tablename__ = 'registration'
    player_id = db.Column(db.String(30),
                          db.ForeignKey(Account.username),
                          primary_key=True)
    tournament_id = db.Column(db.String(50),
                              db.ForeignKey(Tournament.name),
                              primary_key=True)
    has_paid = db.Column(db.Boolean, nullable=False, default=False)
    turned_up = db.Column(db.Boolean, nullable=False, default=False)
    list_accept = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, player_id, tournament_id):
        self.player_id = player_id
        self.tournament_id = tournament_id

    def __repr__(self):
        return '<TournamentRegistration ({}, {})>'.format(
            self.player_id,
            self.tournament_id)

    def write(self, commit=True):
        """To the DB"""
        if Tournament.query.filter_by(name=self.tournament_id).first() is None:
            raise RuntimeError("Check username and tournament")
        if not Account.username_exists(self.player_id):
            raise RuntimeError("Check username and tournament")

        clash = self.clashes()
        if clash is not None and clash.name == self.tournament_id:
            raise RuntimeError("You've already applied to {}".format(
                self.tournament_id))
        elif clash is not None:
            raise RuntimeError("%s clashes with %s that you are registered \
                for already" % (self.tournament_id, clash.name))

        try:
            db.session.add(self)
            if commit:
                db.session.commit()
            return "Application Submitted"
        except Exception:
            db.session.rollback()
            raise

    def clashes(self):
        """
        Check if the date of the tournament overlaps with another tournament
        that has been registered for by the player
        Expects:
            - tournament_id - existing tounament name as per listtournaments
            - username - existing username
        """

        # do this by hand cause I can't get relationships working
        my_tourn = Tournament.query.filter_by(name=self.tournament_id).first()

        clash = db.session.query(TournamentRegistration, Tournament).\
            join(Tournament).\
            filter(and_(
                TournamentRegistration.player_id == self.player_id,
                Tournament.date == my_tourn.date)).first()

        return None if clash is None else clash[1]

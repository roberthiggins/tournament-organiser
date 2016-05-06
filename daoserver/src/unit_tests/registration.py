"""
Players registering for tournaments
"""
import datetime
from flask.ext.testing import TestCase

from app import create_app
from models.account import Account
from models.registration import TournamentRegistration
from models.tournament import db as tournament_db, Tournament as TournamentDAO

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class TournamentRegistrations(TestCase):

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):
        tournament_db.create_all()

    def tearDown(self):
        tournament_db.session.remove()

    def test_register(self):
        """Register a user for a tournament"""
        tournament_1 = 'loving_strahotski'
        tournament_2 = 'loving_casey'
        tournament_3 = 'hating_chuck'
        player_1 = 'strahotski'
        tournament = TournamentDAO(tournament_3)
        tournament.date = datetime.date.today() + datetime.timedelta(days=1)
        tournament.write()
        tournament = TournamentDAO(tournament_1)
        tournament.date = datetime.date.today()
        tournament.write()
        tournament = TournamentDAO(tournament_2)
        tournament.date = datetime.date.today()
        tournament.write()
        Account(player_1, 'spy@strahotski.com').write()

        # First rego good
        TournamentRegistration(player_1, tournament_1).write()
        # another day good
        TournamentRegistration(player_1, tournament_3).write()
        # Repeat bad
        self.assertRaises(
            ValueError,
            TournamentRegistration(player_1, tournament_1).write)
        # Same day bad
        self.assertRaises(
            ValueError,
            TournamentRegistration(player_1, tournament_2).write)
        # Repeat bad
        self.assertRaises(
            ValueError,
            TournamentRegistration(player_1, tournament_3).write)

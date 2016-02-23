"""
Players registering for tournaments
"""
import datetime
from flask.ext.testing import TestCase

from app import create_app
from models.account import Account
from models.registration import TournamentRegistration
from models.tournament import db as tournament_db, Tournament as TournamentDAO

class TournamentRegistrations(TestCase):

    tournament_1 = 'loving_strahotski'
    tournament_2 = 'loving_casey'
    tournament_3 = 'hating_chuck'
    player_1 = 'strahotski'
    player_2 = 'captain_awesome'

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):
        tournament_db.create_all()

    def tearDown(self):
        tournament_db.session.remove()

    def test_register(self):
        """Register a user for a tournament"""

        Account(self.player_1, 'spy@strahotski.com').write()

        TournamentRegistration(self.player_1, self.tournament_1).write()
        TournamentRegistration(self.player_1, self.tournament_3).write()
        self.assertRaises(RuntimeError,
            TournamentRegistration(self.player_1, self.tournament_1).write)
        self.assertRaises(RuntimeError,
            TournamentRegistration(self.player_1, self.tournament_2).write)
        self.assertRaises(RuntimeError,
            TournamentRegistration(self.player_1, self.tournament_3).write)


    def test_clash_detection(self):
        """Check if a registration clashes with another tournament entry"""

        Account(self.player_2, 'captain@strahotski.com').write()
        tournament = TournamentDAO(self.tournament_3)
        tournament.date = datetime.date.today() + datetime.timedelta(days=1)
        tournament.write()
        tournament = TournamentDAO(self.tournament_1)
        tournament.date = datetime.date.today()
        tournament.write()
        tournament = TournamentDAO(self.tournament_2)
        tournament.date = datetime.date.today()
        tournament.write()

        rego_1 = TournamentRegistration(self.player_2, self.tournament_2)
        rego_1.write()
        rego_2 = TournamentRegistration(self.player_2, self.tournament_1)
        tournament_db.session.add(rego_2)
        self.assertTrue(rego_1.clashes().name == self.tournament_2)
        self.assertTrue(rego_2.clashes().name == self.tournament_2)

        rego_3 = TournamentRegistration(self.player_2, self.tournament_3)
        rego_3.write()
        self.assertTrue(rego_3.clashes().name == self.tournament_3)

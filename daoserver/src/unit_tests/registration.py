"""
Players registering for tournaments
"""
import datetime
from flask.ext.testing import TestCase

from app import create_app
from models.account import Account
from models.db_connection import db
from models.registration import TournamentRegistration as TReg

from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,invalid-name,missing-docstring
class TournamentRegistrations(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()
        self.applicant = 'test_register_applicant_1'
        Account(self.applicant, 'spy@strahotski.com').write()

    def tearDown(self):
        TReg.query.filter_by(player_id=self.applicant).delete()
        Account.query.filter_by(username=self.applicant).delete()
        self.injector.delete()
        db.session.remove()

    def test_register(self):
        """Register a user for a tournament"""
        t_1 = 'test_register_1'
        self.injector.inject(t_1, num_players=0)
        t_2 = 'test_register_2'
        self.injector.inject(t_2, num_players=0)
        t_3 = 'test_register_3'
        self.injector.inject(t_3, num_players=0, date=datetime.datetime.now())

        TReg(self.applicant, t_1).write()
        TReg(self.applicant, t_2).write()
        # Repeat bad
        self.assertRaises(ValueError, TReg(self.applicant, t_1).write)
        self.assertRaises(ValueError, TReg(self.applicant, t_2).write)
        # Same day bad
        self.assertRaises(ValueError, TReg(self.applicant, t_3).write)

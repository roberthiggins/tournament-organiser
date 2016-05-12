"""
Players registering for tournaments
"""
import datetime
from flask.ext.testing import TestCase
from sqlalchemy.exc import IntegrityError

from app import create_app
from models.account import Account
from models.db_connection import db, write_to_db
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
        db.session.add(Account(self.applicant, 'spy@strahotski.com'))

    def tearDown(self):
        TReg.query.filter_by(player_id=self.applicant).delete()
        Account.query.filter_by(username=self.applicant).delete()
        self.injector.delete()
        db.session.remove()

    def test_clashes(self):
        """Register a user for a tournament"""
        t_1 = 'test_register_1'
        self.injector.inject(t_1, num_players=0)
        t_2 = 'test_register_2'
        self.injector.inject(t_2, num_players=0)
        t_3 = 'test_register_3'
        self.injector.inject(t_3, num_players=0, date=datetime.datetime.now())
        t_4 = 'test_register_4'
        self.injector.inject(t_4, num_players=0)

        write_to_db(TReg(self.applicant, t_1))
        write_to_db(TReg(self.applicant, t_2))

        self.assertFalse(TReg(self.applicant, t_4).clashes())

        # Repeat bad
        self.assertRaises(ValueError, TReg(self.applicant, t_1).clashes)
        self.assertRaises(ValueError, TReg(self.applicant, t_2).clashes)
        # Same day bad
        self.assertRaises(ValueError, TReg(self.applicant, t_3).clashes)

    def test_insert(self):
        """Register a user for a tournament"""
        t_1 = 'test_register_1'
        self.injector.inject(t_1, num_players=0)
        t_2 = 'test_register_2'
        self.injector.inject(t_2, num_players=0)
        t_3 = 'test_register_3'
        self.injector.inject(t_3, num_players=0, date=datetime.datetime.now())
        t_4 = 'test_register_4'
        self.injector.inject(t_4, num_players=0)

        write_to_db(TReg(self.applicant, t_1))
        write_to_db(TReg(self.applicant, t_2))


        # Repeat bad
        self.assertRaises(IntegrityError, write_to_db,
                          TReg(self.applicant, t_1))
        self.assertRaises(IntegrityError, write_to_db,
                          TReg(self.applicant, t_2))
        # Same day bad, but that needs to be caught by clashes
        write_to_db(TReg(self.applicant, t_3))

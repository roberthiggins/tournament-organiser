"""
Players registering for tournaments
"""
import datetime
from sqlalchemy.exc import IntegrityError

from models.dao.account import Account
from models.dao.registration import TournamentRegistration as TReg

from unit_tests.db_simulating_test import DbSimulatingTest

# pylint: disable=no-member,missing-docstring
class TournamentRegistrations(DbSimulatingTest):

    def setUp(self):
        super(TournamentRegistrations, self).setUp()

        self.applicant = 'test_register_applicant_1'
        self.db.session.add(Account(self.applicant, 'spy@strahotski.com'))

    def tearDown(self):
        TReg.query.filter_by(player_id=self.applicant).delete()
        Account.query.filter_by(username=self.applicant).delete()

        super(TournamentRegistrations, self).tearDown()

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

        self.db.session.add(TReg(self.applicant, t_1))
        self.db.session.add(TReg(self.applicant, t_2))
        self.db.session.flush()

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

        self.db.session.add(TReg(self.applicant, t_1))
        self.db.session.add(TReg(self.applicant, t_2))
        self.db.session.commit()

        # Repeat bad
        self.db.session.add(TReg(self.applicant, t_1))
        self.assertRaises(IntegrityError, self.db.session.commit)
        self.db.session.rollback()

        self.db.session.add(TReg(self.applicant, t_2))
        self.assertRaises(IntegrityError, self.db.session.commit)
        self.db.session.rollback()

        # Same day bad, but that needs to be caught by clashes
        self.db.session.add(TReg(self.applicant, t_3))
        self.db.session.commit()

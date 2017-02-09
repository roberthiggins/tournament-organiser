"""
Basic class for test cases
"""
from flask_testing import TestCase

from app import create_app
from models.dao.db_connection import db
from models.dao.matching_strategy import MatchingStrategy
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=invalid-name,missing-docstring
class AppSimulatingTest(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.db = db
        # pylint: disable=no-member
        if MatchingStrategy.query.count() == 0:
            self.db.session.add(MatchingStrategy('round_robin'))
            self.db.session.add(MatchingStrategy('swiss_chess'))
        self.db.session.flush()
        self.injector = TournamentInjector()

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

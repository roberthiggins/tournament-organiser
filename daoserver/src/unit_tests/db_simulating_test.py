"""
Basic class for test cases
"""
from flask_testing import TestCase

from app import create_app
from models.dao.db_connection import db
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=invalid-name,missing-docstring
class DbSimulatingTest(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.db = db
        self.injector = TournamentInjector()

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

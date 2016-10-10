"""
Test entering scores for games in a tournament
"""

from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.dao.db_connection import db

from models.tournament import Tournament
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,invalid-name,missing-docstring
class TournamentMissionsTests(TestCase):
    """Comes from a range of files"""

    tourn_1 = 'test_missions'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()

        self.injector.inject(self.tourn_1)
        self.injector.add_round(self.tourn_1, 1, None)
        self.injector.add_round(self.tourn_1, 2, None)
        self.tourn = Tournament(self.tourn_1)

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_add_missions(self):
        self.tourn.set_missions(['foo', 'bar'])
        self.tourn.set_missions(['foo', 'bar'])

        self.assertRaises(ValueError, self.tourn.set_missions, [])
        self.assertRaises(ValueError, self.tourn.set_missions, ['1'])
        self.assertRaises(ValueError, self.tourn.set_missions, ['1', '2', '3'])

    def test_get_missions(self):
        compare(self.tourn.get_missions(), ['TBA', 'TBA'])

        self.tourn.set_missions(['foo', 'bar'])
        compare(self.tourn.get_missions(), ['foo', 'bar'])

    def test_round_change(self):
        self.tourn.set_number_of_rounds(0)
        self.tourn.set_number_of_rounds(1)

        compare(self.tourn.get_round(1).get_dao().get_mission(), 'TBA')

"""
Test entering scores for games in a tournament
"""

from testfixtures import compare

from models.tournament import Tournament

from unit_tests.app_simulating_test import AppSimulatingTest

# pylint: disable=no-member,missing-docstring
class TournamentMissionsTests(AppSimulatingTest):

    tourn_1 = 'test_missions'

    def setUp(self):
        super(TournamentMissionsTests, self).setUp()

        self.injector.inject(self.tourn_1)
        self.tourn = Tournament(self.tourn_1)
        self.tourn.update({'rounds': 2})

    # pylint: disable=protected-access
    def test_add_missions(self):
        self.tourn.update({'missions': ['foo', 'bar']})

        self.assertRaises(ValueError, self.tourn._set_missions, [])
        self.assertRaises(ValueError, self.tourn.update, {'missions': []})
        self.assertRaises(ValueError, self.tourn._set_missions, ['1'])
        self.assertRaises(ValueError, self.tourn.update, {'missions': ['1']})
        self.assertRaises(ValueError, self.tourn._set_missions, ['1', '2', '3'])
        self.assertRaises(ValueError, self.tourn.update,
                          {'missions': ['1', '2', '3']})

    def test_get_missions(self):
        compare(self.tourn.get_missions(), ['TBA', 'TBA'])

        self.tourn.update({'missions': ['foo', 'bar']})
        compare(self.tourn.get_missions(), ['foo', 'bar'])

    def test_round_change(self):
        self.tourn.update({'rounds': 0})
        self.tourn.update({'rounds': 1})

        compare(self.tourn.get_round(1).get_dao().get_mission(), 'TBA')

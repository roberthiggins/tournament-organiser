"""
Setting the number of rounds in a tournament
"""
from testfixtures import compare

from models.dao.tournament_round import TournamentRound
from models.tournament import Tournament

from unit_tests.db_simulating_test import DbSimulatingTest

# pylint: disable=no-member,missing-docstring,protected-access
class SetRounds(DbSimulatingTest):

    def test_set_rounds(self):
        """change the number of rounds in a tournament"""
        name = 'test_set_rounds'
        self.injector.inject(name)

        tourn = Tournament(name)
        tourn._set_rounds(6)
        self.assertTrue(tourn.details()['rounds'] == 6)

        tourn._set_rounds(2)
        self.assertTrue(tourn.details()['rounds'] == 2)

    def test_tournament_round_deletion(self):
        """Check that the rounds get deleted when rounds are reduced"""
        name = 'test_tournament_round_deletion'
        self.injector.inject(name)

        tourn = Tournament(name)
        tourn.update({'rounds': 6})
        compare(
            len(TournamentRound.query.filter_by(tournament_name=name).all()),
            6)

        tourn.update({'rounds': 2})
        compare(
            len(TournamentRound.query.filter_by(tournament_name=name).all()),
            2)

    def test_get_missions(self):
        """get missions for the rounds"""
        name = 'test_get_missions'
        self.injector.inject(name)
        tourn = Tournament(name)
        tourn.update({
            'rounds': 3,
            'missions': ['mission_1', 'mission_2', 'mission_3']
        })


        tourn.update({'rounds': 4})
        compare(tourn.get_round(1).get_dao().mission, 'mission_1')
        compare(tourn.get_round(4).get_dao().mission, None)

        compare(Tournament(name).get_missions(),
                ['mission_1', 'mission_2', 'mission_3', 'TBA'])

    def test_get_round(self):
        """Test the round getter"""
        name = 'test_get_round'
        self.injector.inject(name)

        tourn = Tournament(name)
        tourn.update({'rounds': 2})

        self.assertTrue(tourn.get_round(1).get_dao().ordering == 1)
        self.assertTrue(tourn.get_round(2).get_dao().ordering == 2)

        self.assertRaises(ValueError, tourn.get_round, 3)
        self.assertRaises(ValueError, tourn.get_round, -1)
        self.assertRaises(ValueError, tourn.get_round, 'a')
        self.assertRaises(ValueError, tourn.get_round, 0)

    def test_errors(self):
        """Illegal values"""
        name = 'test_errors'
        self.injector.inject(name)

        tourn = Tournament(name)
        self.assertRaises(ValueError, tourn._set_rounds, 'foo')
        self.assertRaises(ValueError, tourn.update, {'rounds': 'foo'})
        self.assertRaises(ValueError, tourn._set_rounds, '')
        self.assertRaises(ValueError, tourn.update, {'rounds': ''})
        self.assertRaises(TypeError, tourn._set_rounds, None)

        name_2 = 'test_errors_2'
        self.injector.inject(name_2)
        tourn = Tournament(name_2)
        self.assertRaises(ValueError, tourn._set_rounds, 'foo')
        self.assertRaises(ValueError, tourn.update, {'rounds': 'foo'})
        self.assertRaises(ValueError, tourn._set_rounds, '')
        self.assertRaises(ValueError, tourn.update, {'rounds': ''})
        self.assertRaises(TypeError, tourn._set_rounds, None)

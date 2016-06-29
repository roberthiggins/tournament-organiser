"""
Setting the number of rounds in a tournament
"""
from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.dao.tournament import db
from models.dao.tournament_round import TournamentRound
from models.tournament import Tournament

from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class SetRounds(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_set_rounds(self):
        """change the number of rounds in a tournament"""
        name = 'test_set_rounds'
        self.injector.inject(name, rounds=4)

        tourn = Tournament(name)
        self.assertTrue(tourn.details()['rounds'] == 4)

        tourn.set_number_of_rounds(6)
        self.assertTrue(tourn.details()['rounds'] == 6)

        tourn.set_number_of_rounds(2)
        self.assertTrue(tourn.details()['rounds'] == 2)

    def test_tournament_round_deletion(self):
        """Check that the rounds get deleted when rounds are reduced"""
        name = 'test_tournament_round_deletion'
        self.injector.inject(name, rounds=4)

        tourn = Tournament(name)
        tourn.set_number_of_rounds(6)
        compare(
            len(TournamentRound.query.filter_by(tournament_name=name).all()),
            6)

        tourn.set_number_of_rounds(2)
        compare(
            len(TournamentRound.query.filter_by(tournament_name=name).all()),
            2)

    def test_get_missions(self):
        """get missions for the rounds"""
        name = 'test_get_missions'
        self.injector.inject(name, rounds=3)
        self.injector.add_round(name, 1, 'mission_1')
        self.injector.add_round(name, 2, 'mission_2')
        self.injector.add_round(name, 3, 'mission_3')

        tourn = Tournament(name)
        tourn.set_number_of_rounds(4)
        compare(tourn.get_round(1).mission, 'mission_1')
        compare(tourn.get_round(4).mission, 'TBA')

        compare(
            [x.mission for x in Tournament(name).get_dao().rounds],
            ['mission_1', 'mission_2', 'mission_3', 'TBA'])

    def test_get_round(self):
        """Test the round getter"""
        name = 'test_get_round'
        self.injector.inject(name)

        tourn = Tournament(name)
        tourn.set_number_of_rounds(2)

        self.assertTrue(tourn.get_round(1).ordering == 1)
        self.assertTrue(tourn.get_round(2).ordering == 2)

        self.assertRaises(ValueError, tourn.get_round, 3)
        self.assertRaises(ValueError, tourn.get_round, -1)
        self.assertRaises(ValueError, tourn.get_round, 'a')
        self.assertRaises(ValueError, tourn.get_round, 0)

    def test_errors(self):
        """Illegal values"""
        name = 'test_errors'
        self.injector.inject(name)

        tourn = Tournament(name)
        self.assertRaises(ValueError, tourn.set_number_of_rounds, 'foo')
        self.assertRaises(ValueError, tourn.set_number_of_rounds, '')
        self.assertRaises(TypeError, tourn.set_number_of_rounds, None)

        name_2 = 'test_errors_2'
        self.injector.inject(name_2, rounds=5)
        tourn = Tournament(name_2)
        self.assertRaises(ValueError, tourn.set_number_of_rounds, 'foo')
        self.assertRaises(ValueError, tourn.set_number_of_rounds, '')
        self.assertRaises(TypeError, tourn.set_number_of_rounds, None)

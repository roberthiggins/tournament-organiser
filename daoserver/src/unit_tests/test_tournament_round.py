"""
Setting the number of rounds in a tournament
"""
from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from models.tournament import db as tournament_db
from models.tournament_round import TournamentRound
from tournament import Tournament

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class SetRounds(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        tournament_db.create_all()

    def tearDown(self):
        tournament_db.session.remove()

    def set_up_tournament(self, name):
        """While using a live db we still need to hack this"""
        from datetime import date
        from models.tournament import Tournament as TournamentDAO
        dao = TournamentDAO(name)
        dao.date = date.today()
        dao.num_rounds = 4
        dao.write()

        TournamentRound(name, 1, 'mission_1').write()
        TournamentRound(name, 2, 'mission_2').write()
        TournamentRound(name, 3, 'mission_3').write()
        TournamentRound(name, 4).write()

    def test_set_rounds(self):
        """change the number of rounds in a tournament"""
        name = 'test_set_rounds'
        self.set_up_tournament(name)

        tourn = Tournament(name)
        self.assertTrue(tourn.details()['rounds'] == 4)

        tourn.set_number_of_rounds(6)
        self.assertTrue(tourn.details()['rounds'] == 6)

        tourn.set_number_of_rounds(2)
        self.assertTrue(tourn.details()['rounds'] == 2)

    def test_tournament_round_deletion(self):
        """Check that the rounds get deleted when rounds are reduced"""
        name = 'test_tournament_round_deletion'
        self.set_up_tournament(name)

        tourn = Tournament(name)
        tourn.set_number_of_rounds(6)
        # set_number_of_rounds only deletes excess rounds
        self.assertTrue(4 == len(TournamentRound.query.filter_by(
            tournament_name=name).all())) # thus still 4

        tourn.set_number_of_rounds(2)
        self.assertTrue(2 == len(TournamentRound.query.filter_by(
            tournament_name=name).all()))

    def test_get_missions(self):
        """get missions for the rounds"""
        name = 'test_get_missions'
        self.set_up_tournament(name)

        tourn = Tournament(name)
        compare(tourn.get_mission(1), 'mission_1')
        compare(tourn.get_mission(4), 'TBA')

        self.assertRaises(ValueError, tourn.get_mission, 'a')
        self.assertRaises(ValueError, tourn.get_mission, 5)

        compare(
            [x.mission for x in Tournament(name).get_dao().rounds],
            ['mission_1', 'mission_2', 'mission_3', 'TBA'])

    def test_set_mission(self):
        """add a mission to the tournament round"""
        name = 'test_set_mission'
        self.set_up_tournament(name)

        tourn = Tournament(name)
        self.assertRaises(ValueError, tourn.set_mission, 'a', 'should_fail')
        self.assertRaises(ValueError, tourn.set_mission, -1, 'should_fail')
        self.assertRaises(ValueError, tourn.set_mission, 7, 'should_fail')

        tourn.set_mission(5, 'mission_5')
        self.assertTrue(tourn.get_mission(5), 'mission_5')
        tourn.set_mission(4, 'mission_4')
        self.assertTrue(tourn.get_mission(4), 'mission_4')
        tourn.set_mission(2, 'mission_2')
        self.assertTrue(tourn.get_mission(2), 'mission_2')

    def test_errors(self):
        """Illegal values"""
        name = 'test_errors'
        self.set_up_tournament(name)

        tourn = Tournament(name)
        self.assertRaises(ValueError, tourn.set_number_of_rounds, 'foo')
        self.assertRaises(ValueError, tourn.set_number_of_rounds, '')
        self.assertRaises(TypeError, tourn.set_number_of_rounds, None)

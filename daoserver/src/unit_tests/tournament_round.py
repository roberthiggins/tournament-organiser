"""
Setting the number of rounds in a tournament
"""
from testfixtures import compare

from models.dao.tournament_round import TournamentRound
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry
from models.tournament_round import TournamentRound as TRoundModel

from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args as cat

# pylint: disable=no-member,missing-docstring,protected-access
class SetRounds(AppSimulatingTest):

    def test_set_rounds(self):
        """change the number of rounds in a tournament"""
        name = 'test_set_rounds'
        tourn = self.injector.inject(name)

        tourn._set_rounds(6)
        self.assertTrue(tourn.details()['rounds'] == 6)

        tourn._set_rounds(2)
        self.assertTrue(tourn.details()['rounds'] == 2)

    def test_tournament_round_deletion(self):
        """Check that the rounds get deleted when rounds are reduced"""
        name = 'test_tournament_round_deletion'
        tourn = self.injector.inject(name)

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
        tourn = self.injector.inject(name)
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
        tourn = self.injector.inject(name)

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
        tourn = self.injector.inject(name)

        self.assertRaises(ValueError, tourn._set_rounds, 'foo')
        self.assertRaises(ValueError, tourn.update, {'rounds': 'foo'})
        self.assertRaises(ValueError, tourn._set_rounds, '')
        self.assertRaises(ValueError, tourn.update, {'rounds': ''})
        self.assertRaises(TypeError, tourn._set_rounds, None)

        name_2 = 'test_errors_2'
        tourn = self.injector.inject(name_2)
        self.assertRaises(ValueError, tourn._set_rounds, 'foo')
        self.assertRaises(ValueError, tourn.update, {'rounds': 'foo'})
        self.assertRaises(ValueError, tourn._set_rounds, '')
        self.assertRaises(ValueError, tourn.update, {'rounds': ''})
        self.assertRaises(TypeError, tourn._set_rounds, None)

    def test_is_complete(self):
        """Check that all the games are complete in the round"""
        name = 'test_complete'
        cat_1 = 'per_round'
        tourn = self.injector.inject(name)
        tourn.update({
            'rounds': 2,
            'score_categories': [cat(cat_1, 100, False, 0, 100)]
        })

        self.assertFalse(TRoundModel(name, 2).is_complete())
        # Enter scores for round 1
        for idx, ent in enumerate(tourn.get_dao().entries.all()):
            self.assertFalse(TRoundModel(name, 1).is_complete())
            model = TournamentEntry(name, ent.player_id)
            game_id = model.get_next_game()['game_id']

            model.set_scores([
                {'game_id': game_id, 'category': cat_1, 'score': idx + 1},
            ])
        self.assertTrue(TRoundModel(name, 1).is_complete())
        self.assertFalse(TRoundModel(name, 2).is_complete())

    def test_get_ordering(self):
        name = 'test_ordering'
        self.injector.inject(name).update({'rounds': 5})
        rnd = TRoundModel(name, 1)
        compare(rnd.get_ordering(), 1)
        rnd = TRoundModel(name, 2)
        compare(rnd.get_ordering(), 2)

"""
Setting the number of rounds in a tournament
"""
from flask_testing import TestCase

from app import create_app
from models.dao.registration import TournamentRegistration
from models.dao.tournament import db
from models.tournament import Tournament

from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class TournamentInProgress(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()
        self.name = 'test_in_progress'
        self.player_1 = 'p1'

        self.injector.inject(self.name, num_players=0)
        self.injector.add_player(self.name, self.player_1)
        self.injector.add_round(self.name, 1, 'mission01')
        self.tournament = Tournament(self.name)

        self.tournament.set_score_categories([{
            'name':       'cat',
            'percentage': 100,
            'per_tourn':  True,
            'min_val':    1,
            'max_val':    1,
            'zero_sum':   False
        }])

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_default_state(self):
        self.assertFalse(self.tournament.get_dao().in_progress)

    def test_no_categories(self):
        self.injector.delete_scores()
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_entries(self):
        self.injector.delete_accounts()
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_missions(self):
        self.tournament.set_number_of_rounds(0)
        self.tournament.set_number_of_rounds(1)
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_rounds(self):
        self.tournament.set_number_of_rounds(0)
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_set_in_progress(self):
        self.tournament.set_in_progress()
        self.assertTrue(self.tournament.get_dao().in_progress)

    def test_non_finalised_only_actions(self):
        self.tournament.set_in_progress()

        self.assertRaises(ValueError, self.tournament.set_date, '3099-04-04')
        self.assertRaises(ValueError, self.tournament.set_score_categories,
                          [{
                              'name':       'disallowed_category',
                              'percentage': 100,
                              'per_tourn':  True,
                              'min_val':    1,
                              'max_val':    1
                          }])
        self.assertRaises(ValueError, self.tournament.set_number_of_rounds, 5)

        rego = TournamentRegistration(self.player_1, self.name)
        rego.add_to_db()
        self.assertRaises(ValueError, self.tournament.confirm_entries)

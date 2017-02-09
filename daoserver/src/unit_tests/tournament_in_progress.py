"""
Setting the number of rounds in a tournament
"""
from models.dao.registration import TournamentRegistration as Reg
from models.dao.tournament_entry import TournamentEntry

from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args

# pylint: disable=no-member,missing-docstring
class TournamentInProgress(AppSimulatingTest):

    def setUp(self):
        super(TournamentInProgress, self).setUp()

        self.name = 'test_in_progress'
        self.player_1 = 'p1'

        self.tournament = self.injector.inject(self.name, num_players=0)
        self.injector.add_player(self.name, self.player_1)
        self.tournament.update({
            'rounds': 1,
            'missions': ['mission01'],
            'score_categories': [score_cat_args('cat', 100, True, 1, 1, False)]
        })

    def test_default_state(self):
        self.assertFalse(self.tournament.get_dao().in_progress)

    def test_no_categories(self):
        self.tournament.update({'score_categories': []})
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_entries(self):
        self.tournament.update({'rounds': 0})
        dao = self.tournament.get_dao()
        Reg.query.filter_by(tournament_id=dao.id).delete()
        TournamentEntry.query.filter_by(tournament_id=dao.name).delete()
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_missions(self):
        self.tournament.update({'rounds': 0})
        self.tournament.update({'rounds': 1})
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_no_rounds(self):
        self.tournament.update({'rounds': 0})
        self.assertRaises(ValueError, self.tournament.set_in_progress)

    def test_set_in_progress(self):
        self.tournament.set_in_progress()
        self.assertTrue(self.tournament.get_dao().in_progress)

    def test_non_finalised_only_actions(self):
        self.tournament.set_in_progress()

        args = score_cat_args('disallowed_cat', 100, True, 1, 1)
        self.assertRaises(ValueError, self.tournament.update,
                          {'score_categories': [args]})
        self.assertRaises(ValueError, self.tournament.update, {'rounds': 5})

        rego = Reg(self.player_1, self.name)
        rego.add_to_db()
        self.assertRaises(ValueError, self.tournament.confirm_entries)

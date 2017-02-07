"""
Test getting the scores entered by a entrant
"""

from testfixtures import compare

from models.dao.tournament_entry import TournamentEntry

from models.tournament import Tournament
from models.tournament_entry import TournamentEntry as EntryModel

from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args as cat

# pylint: disable=no-member,missing-docstring
class TestPerTournamentScores(AppSimulatingTest):

    t_name = 'score_entered_tournament_0'

    def setUp(self):
        super(TestPerTournamentScores, self).setUp()
        self.injector.inject(self.t_name, num_players=1)
        tourn = Tournament(self.t_name)
        tourn.update({
            'score_categories': [cat('per_t_cat_1', 1, True, 0, 100),
                                 cat('per_t_cat_2', 1, True, 0, 100)]
        })

        dao = TournamentEntry.query.\
            filter_by(tournament_id=self.t_name).first()
        self.entry = EntryModel(self.t_name, dao.player_id)

    def test_format(self):
        """The basic format of the output when no scores entered"""
        expected = {
            'per_t_cat_1': None,
            'per_t_cat_2': None
        }
        compare(self.entry.get_tournament_entered_scores(), expected)


    def test_per_tournament_scores(self):
        """Add some per-tournament scores"""
        expected = {
            'per_t_cat_1': None,
            'per_t_cat_2': 2
        }
        self.entry.set_scores([{'category': 'per_t_cat_2', 'score': 2}])

        compare(self.entry.get_tournament_entered_scores(), expected)


class TestPerGameScores(AppSimulatingTest):
    """Test the per-game score dict"""

    t_name = 'score_entered_tournament_1'

    def setUp(self):
        super(TestPerGameScores, self).setUp()
        self.injector.inject(self.t_name, num_players=4)
        tourn = Tournament(self.t_name)
        tourn.update({
            'rounds': 2,
            'missions': ['mission_1', 'mission_2'],
            'score_categories': [cat('per_g_cat_1', 1, False, 0, 100),
                                 cat('per_g_cat_2', 1, False, 0, 100)]
        })

        dao = TournamentEntry.query.\
            filter_by(tournament_id=self.t_name).first()
        self.entry = EntryModel(self.t_name, dao.player_id)
        tourn.make_draws()
        self.ent_1_g_1 = self.entry.get_next_game()

        # Enter scores for round 1
        for ent in tourn.get_dao().entries.all():
            model = EntryModel(self.t_name, ent.player_id)
            game_id = model.get_next_game()['game_id']
            model.set_scores([
                {'game_id': game_id, 'category': 'per_g_cat_1', 'score': 1},
                {'game_id': game_id, 'category': 'per_g_cat_2', 'score': 2}
            ])

    def test_per_game_scores(self):
        """The basic format of the output when no scores entered"""

        g_1 = {
            'game_id': self.ent_1_g_1['game_id'],
            'per_g_cat_1': 1,
            'per_g_cat_2': 2
        }
        next_game = self.entry.get_next_game()['game_id']
        g_2 = {
            'game_id': next_game,
            'per_g_cat_1': None,
            'per_g_cat_2': None
        }

        compare(self.entry.get_game_entered_scores(self.ent_1_g_1['game_id']),
                g_1)
        compare(self.entry.get_game_entered_scores(next_game), g_2)


    def test_all_scores(self):
        """Test once a game is partially scored"""

        # Enter 1 score for round 2
        game_id = self.entry.get_next_game()['game_id']
        self.entry.set_scores(
            [{'game_id': game_id, 'category': 'per_g_cat_1', 'score': 3}])

        expected = {
            'per_tournament': {},
            'per_game': [
                {
                    'game_id': self.ent_1_g_1['game_id'],
                    'per_g_cat_1': 1,
                    'per_g_cat_2': 2
                },
                {
                    'game_id': self.entry.get_next_game()['game_id'],
                    'per_g_cat_1': 3,
                    'per_g_cat_2': None
                }
            ]
        }

        compare(self.entry.get_scores_entered(), expected)

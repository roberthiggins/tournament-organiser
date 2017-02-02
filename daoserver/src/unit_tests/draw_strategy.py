"""
Draw strategy unit tests
"""
# pylint: disable=invalid-name,missing-docstring

from testfixtures import compare

from models.matching_strategy import RoundRobin, SwissChess
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry

from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args as cat

class RoundRobinTests(AppSimulatingTest):
    """Tests for `matching_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""

        self.injector.inject('dst', num_players=5)

        entries = Tournament('dst').get_entries()
        draw = RoundRobin().set_round(1).match(entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(2).match(entries)
        compare(draw[0][0].player_id, 'dst_player_5')
        compare(draw[0][1].player_id, 'dst_player_4')
        compare(draw[1][0].player_id, 'dst_player_1')
        compare(draw[1][1].player_id, 'dst_player_3')
        compare(draw[2][0].player_id, 'dst_player_2')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(3).match(entries)
        compare(draw[0][0].player_id, 'dst_player_4')
        compare(draw[0][1].player_id, 'dst_player_3')
        compare(draw[1][0].player_id, 'dst_player_5')
        compare(draw[1][1].player_id, 'dst_player_2')
        compare(draw[2][0].player_id, 'dst_player_1')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(4).match(entries)
        compare(draw[0][0].player_id, 'dst_player_3')
        compare(draw[0][1].player_id, 'dst_player_2')
        compare(draw[1][0].player_id, 'dst_player_4')
        compare(draw[1][1].player_id, 'dst_player_1')
        compare(draw[2][0].player_id, 'dst_player_5')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(5).match(entries)
        compare(draw[0][0].player_id, 'dst_player_2')
        compare(draw[0][1].player_id, 'dst_player_1')
        compare(draw[1][0].player_id, 'dst_player_3')
        compare(draw[1][1].player_id, 'dst_player_5')
        compare(draw[2][0].player_id, 'dst_player_4')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(6).match(entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')

def contains(draw, ent_1, ent_2):
    """check that ent_1 and ent_2 are playing each other in draw"""
    names = [(x[0].player_id, x[1].player_id) for x in draw]
    for x in names:
        if ent_1 in x and ent_2 in x:
            return True
    return False

class SwissChessTests(AppSimulatingTest):
    """Tests for `matching_strategy.py`."""

    @staticmethod
    # pylint: disable=unused-argument
    def round_1(entry):
        """all players should have a score of 0 in the first round"""
        return 0

    @staticmethod
    # pylint: disable=unused-variable
    def round_2(entry):
        """The scores for each player after round 1"""
        if entry.player_id == 'dst_player_1':
            return 5
        if entry.player_id == 'dst_player_2':
            return 8
        if entry.player_id == 'dst_player_3':
            return 10
        if entry.player_id == 'dst_player_4':
            return 2
        if entry.player_id == 'dst_player_5':
            return 5
        if entry.player_id == 'dst_player_6':
            return 1

    @staticmethod
    # pylint: disable=unused-argument
    def re_match(entries):
        """re-matches are allowed"""
        return False

    def test_match(self):
        """Test get_draw"""
        tourn_id = 'dst'
        self.injector.inject(tourn_id, num_players=6)
        entries = Tournament(tourn_id).get_entries()

        draw = SwissChess(rank=self.round_1, re_match=self.re_match).\
            match(entries)
        self.assertTrue(contains(draw, 'dst_player_1', 'dst_player_2'))
        self.assertTrue(contains(draw, 'dst_player_3', 'dst_player_4'))
        self.assertTrue(contains(draw, 'dst_player_5', 'dst_player_6'))

        draw = SwissChess(rank=self.round_2, re_match=self.re_match).\
            match(entries)
        self.assertTrue(contains(draw, 'dst_player_4', 'dst_player_6'))
        self.assertTrue(contains(draw, 'dst_player_1', 'dst_player_5'))
        self.assertTrue(contains(draw, 'dst_player_2', 'dst_player_3'))

    # pylint: disable=protected-access
    def test_legal_draws(self):
        legal = [
            ({'name': 'one'}, {'name': 'two'}),
            ({'name': 'three'}, {'name': 'five'}),
            ({'name': 'four'}, {'name': 'BYE'}),
        ]
        self.assertTrue(SwissChess(rank=self.round_1, re_match=self.re_match)\
            ._check_legal_draw(legal))

        illegal = [
            ({'name': 'one'}, {'name': 'two'}),
            ({'name': 'three'}, {'name': 'one'}),
        ]
        self.assertFalse(SwissChess(rank=self.round_1, re_match=self.re_match)\
            ._check_legal_draw(illegal))

class SwissChessFitnessTests(AppSimulatingTest):
    # pylint: disable=too-many-instance-attributes
    """Checking for re-matches and scores"""

    def setUp(self):
        super(SwissChessFitnessTests, self).setUp()
        tourn_id = 'sct'
        self.injector.inject(tourn_id, num_players=6)
        tournament = Tournament(tourn_id)
        tournament.update({
            'rounds': 2,
            'score_categories': [cat('c_1', 100, False, 0, 100)]
        })

        self.entries = tournament.get_entries()
        self.def_rnk = tournament.ranking_strategy.total_score
        self.clash = tournament.check_re_match

        self.p_1 = TournamentEntry(tourn_id, 'sct_player_1')
        self.p_2 = TournamentEntry(tourn_id, 'sct_player_2')
        self.p_3 = TournamentEntry(tourn_id, 'sct_player_3')
        self.p_4 = TournamentEntry(tourn_id, 'sct_player_4')
        self.p_5 = TournamentEntry(tourn_id, 'sct_player_5')
        self.p_6 = TournamentEntry(tourn_id, 'sct_player_6')

    @staticmethod
    # pylint: disable=unused-argument
    def re_match(entries):
        return False

    def test_rank_function(self):

        game = self.p_1.get_next_game()['game_id']
        self.p_1.set_scores([{'category': 'c_1', 'score': 5, 'game_id': game}])

        game = self.p_2.get_next_game()['game_id']
        self.p_2.set_scores([{'category': 'c_1', 'score': 8, 'game_id': game}])

        game = self.p_3.get_next_game()['game_id']
        self.p_3.set_scores([{'category': 'c_1', 'score': 10, 'game_id': game}])

        game = self.p_4.get_next_game()['game_id']
        self.p_4.set_scores([{'category': 'c_1', 'score': 2, 'game_id': game}])

        game = self.p_5.get_next_game()['game_id']
        self.p_5.set_scores([{'category': 'c_1', 'score': 5, 'game_id': game}])

        game = self.p_6.get_next_game()['game_id']
        self.p_6.set_scores([{'category': 'c_1', 'score': 1, 'game_id': game}])

        draw = SwissChess(rank=self.def_rnk, re_match=self.re_match).\
            match(self.entries)
        self.assertTrue(contains(draw, 'sct_player_4', 'sct_player_6'))
        self.assertTrue(contains(draw, 'sct_player_1', 'sct_player_5'))
        self.assertTrue(contains(draw, 'sct_player_2', 'sct_player_3'))

    def test_re_match_function(self):
        game = self.p_1.get_next_game()['game_id']
        opponent_1 = self.p_1.get_next_game()['opponent']
        self.p_1.set_scores([{'category': 'c_1', 'score': 50, 'game_id': game}])

        game = self.p_2.get_next_game()['game_id']
        self.p_2.set_scores([{'category': 'c_1', 'score': 50, 'game_id': game}])

        game = self.p_3.get_next_game()['game_id']
        self.p_3.set_scores([{'category': 'c_1', 'score': 10, 'game_id': game}])

        game = self.p_4.get_next_game()['game_id']
        self.p_4.set_scores([{'category': 'c_1', 'score': 2, 'game_id': game}])

        game = self.p_5.get_next_game()['game_id']
        self.p_5.set_scores([{'category': 'c_1', 'score': 5, 'game_id': game}])

        game = self.p_6.get_next_game()['game_id']
        self.p_6.set_scores([{'category': 'c_1', 'score': 8, 'game_id': game}])

        draw = SwissChess(rank=self.def_rnk, re_match=self.clash).\
            match(self.entries)
        self.assertFalse(contains(draw, 'sct_player_1', opponent_1))


class SwissChessTestByes(AppSimulatingTest):
    """Checking for re-matches and scores"""

    @staticmethod
    # pylint: disable=unused-argument
    def round_1_scores(entry):
        """The scores for each player at start"""
        return 0

    @staticmethod
    # pylint: disable=unused-argument
    def round_2_scores(entry):
        """The scores for each player after round 1"""
        return 50

    @staticmethod
    # pylint: disable=unused-argument
    def re_match_r_1(entry):
        """None"""
        return False

    @staticmethod
    # pylint: disable=unused-argument
    def re_match_r_2(game):
        """Round one draw should be 1v2, 3v4, 5vNone"""
        pair = set([game[0]['name'], game[1]['name']])
        if 'sct_2_player_1' in pair and 'sct_2_player_2' in pair:
            return True
        if 'sct_2_player_3' in pair and 'sct_2_player_4' in pair:
            return True
        if 'sct_2_player_5' in pair and 'BYE' in pair:
            return True
        return False

    def test_re_match_function_for_bye(self):

        matching_strategy = SwissChess(rank=self.round_1_scores,
                                       re_match=self.re_match_r_1)

        tourn_id = 'sct_2'
        self.injector.inject(tourn_id, num_players=5)
        entries = Tournament(tourn_id).get_entries()

        draw = matching_strategy.match(entries)
        bye_player = [g for g in draw if g[1] == 'BYE'][0][0].player_id


        matching_strategy = SwissChess(rank=self.round_2_scores,
                                       re_match=self.re_match_r_2)
        draw = matching_strategy.match(entries)
        bye_player_r2 = [g for g in draw if g[1] == 'BYE'][0][0].player_id


        self.assertFalse(bye_player == bye_player_r2)

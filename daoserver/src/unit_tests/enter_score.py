"""
Test entering scores for games in a tournament
"""

from testfixtures import compare
import unittest

from db_connections.db_connection import db_conn
from game import get_game_from_score

# pylint: disable=no-member,no-init,invalid-name,missing-docstring,undefined-variable
class ScoreEnteringTests(unittest.TestCase):
    """Comes from a range of files"""

    def test_get_game_from_score(self):
        """
        You should be able to determine game from entry_id and the score_key
        """

        # A regular player
        game = get_game_from_score(5, 'sports')
        self.assertTrue(game is not None)

        game = get_game_from_score(5, 'round_1_battle')
        self.assertTrue(game is not None)
        self.assertTrue(game.entry_1 is not None)
        self.assertTrue(game.entry_2 is not None)
        self.assertTrue(game.entry_1 == 5 or game.entry_2 == 5)
        self.assertTrue(game.entry_1 == 3 or game.entry_2 == 3)


        # A score that isn't tied to a game
        game = get_game_from_score(1, 'number_tassles')
        self.assertTrue(game is None)


        # A player in a bye
        game = get_game_from_score(4, 'round_1_battle')
        self.assertTrue(game is not None)
        self.assertTrue(game.entry_1 == 4)
        self.assertTrue(game.entry_2 is None)


        # Poor data will return None rather than an error
        game = get_game_from_score(15, 'round_1_battle')
        self.assertTrue(game is None)
        game = get_game_from_score(1, 'number_fdssfdtassles')
        self.assertTrue(game is None)


    @db_conn()
    def test_score_entered(self):

        # A completed game
        game = get_game_from_score(5, 'round_1_battle')
        compare(game.entry_1, 3)
        compare(game.entry_2, 5)
        self.assertTrue(game.is_score_entered())

        # a bye should be false
        # TODO resolve Bye Scoring
        game = get_game_from_score(4, 'round_1_battle')
        compare(game.entry_1, 4)
        compare(game.entry_2, None)
        self.assertFalse(game.is_score_entered())

        # Ensure the rd2 game bart vs. maggie is listed as not scored. This
        # will force a full check. Maggie's score hasn't been entered.
        cur.execute("UPDATE game SET score_entered = False WHERE id = 5")
        game = get_game_from_score(5, 'round_2_battle')

        compare(game.entry_1, 6)
        compare(game.entry_2, 5)
        self.assertFalse(game.is_score_entered())

        # Enter the final score for maggie
        cur.execute("INSERT INTO score VALUES(6, 4, 2)")
        conn.commit()

        self.assertTrue(game.is_score_entered())
        game.set_score_entered()
        self.assertTrue(game.is_score_entered())

    def test_list_scores_for_game(self):
        """
        Games have a scores_entered which should return all the scores entered
        for by each entrant.
        """
        # Bye
        game = get_game_from_score(4, 'round_1_battle')
        compare(
            game.scores_entered(),
            [(4, 'round_1_battle', None), (4, 'sports', 5)])

        # Regular, completed game
        game = get_game_from_score(2, 'round_1_battle')
        compare(
            game.scores_entered(),
            [(6, 'round_1_battle', 0), (2, 'round_1_battle', 20),
             (6, 'sports', 5), (2, 'sports', 1)])

        # Game partially filled in
        game = get_game_from_score(5, 'round_2_battle')
        compare(
            game.scores_entered(),
            [(5, 'round_2_battle', 5)])

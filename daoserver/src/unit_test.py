"""
Unit Tests for the daoserver
"""

import unittest
from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from db_connections.db_connection import db_conn
from db_connections.entry_db import Entry
from matching_strategy import RoundRobin
from models.tournament import db as tournament_db
from table_strategy import ProtestAvoidanceStrategy, Table
from tournament import Tournament

class TournamentInfo(TestCase):

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):

        tournament_db.create_all()

    def tearDown(self):

        tournament_db.session.remove()
        #tournament_db.drop_all()

    def test_get_score_keys(self):
        """Get the score keys for the round"""
        tourn = Tournament('ranking_test')

        self.assertRaises(NotImplementedError, tourn.get_score_keys_for_round)
        compare(tourn.get_score_keys_for_round(1),
            [(3, "round_1_battle", 0, 20, 3, 3, 1),
            (5, "sports", 1, 5, 4, 5, 1)])
        compare(tourn.get_score_keys_for_round(2),
            [(4, "round_2_battle", 0, 20, 3, 4, 2)])

        self.assertRaises(ValueError, tourn.get_score_keys_for_round, 3)

        tourn.set_mission(3, 'Third Mission')
        compare(tourn.get_score_keys_for_round(3), []) # no score yet

        tourn.set_score(key='round_3_battle', min_val=0, max_val=25,
            category=3, round_id=3)
        compare(tourn.get_score_keys_for_round(3)[0][1:],
            ('round_3_battle', 25, 0, 3, 34, 3))

class DrawStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `matching_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""
        matching_strategy = RoundRobin('ranking_test')
        draw = matching_strategy.match(1)
        self.assertTrue(draw[0][0].username == 'homer')
        self.assertTrue(draw[0][1].username == 'maggie')
        self.assertTrue(draw[1][0].username == 'marge')
        self.assertTrue(draw[1][1].username == 'bart')
        self.assertTrue(draw[2][0].username == 'lisa')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(2)
        self.assertTrue(draw[0][0].username == 'maggie')
        self.assertTrue(draw[0][1].username == 'bart')
        self.assertTrue(draw[1][0].username == 'homer')
        self.assertTrue(draw[1][1].username == 'lisa')
        self.assertTrue(draw[2][0].username == 'marge')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(3)
        self.assertTrue(draw[0][0].username == 'bart')
        self.assertTrue(draw[0][1].username == 'lisa')
        self.assertTrue(draw[1][0].username == 'maggie')
        self.assertTrue(draw[1][1].username == 'marge')
        self.assertTrue(draw[2][0].username == 'homer')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(4)
        self.assertTrue(draw[0][0].username == 'lisa')
        self.assertTrue(draw[0][1].username == 'marge')
        self.assertTrue(draw[1][0].username == 'bart')
        self.assertTrue(draw[1][1].username == 'homer')
        self.assertTrue(draw[2][0].username == 'maggie')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(5)
        self.assertTrue(draw[0][0].username == 'marge')
        self.assertTrue(draw[0][1].username == 'homer')
        self.assertTrue(draw[1][0].username == 'lisa')
        self.assertTrue(draw[1][1].username == 'maggie')
        self.assertTrue(draw[2][0].username == 'bart')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(6)
        self.assertTrue(draw[0][0].username == 'homer')
        self.assertTrue(draw[0][1].username == 'maggie')
        self.assertTrue(draw[1][0].username == 'marge')
        self.assertTrue(draw[1][1].username == 'bart')
        self.assertTrue(draw[2][0].username == 'lisa')
        self.assertTrue(draw[2][1] == 'BYE')

class TableStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `table_strategy_strategy.py`."""

    def test_get_protest_score_for_game(self):
        """Test that individual games get the correct protest score"""
        entry1 = Entry(entry_id='entry1', game_history=[1, 3])
        entry2 = Entry(entry_id='entry2', game_history=[2, 3])
        game = [entry1, entry2]

        self.assertTrue(Table(1, game).protest_score() == 1)
        self.assertTrue(Table(2, game).protest_score() == 1)
        self.assertTrue(Table(3, game).protest_score() == 2)
        self.assertTrue(Table(4, game).protest_score() == 0)
        self.assertTrue(Table(5, game).protest_score() == 0)
        self.assertTrue(Table(-1, game).protest_score() == 0)
        self.assertTrue(Table(-1, [entry1]).protest_score() == 0)
        self.assertTrue(Table(1, [entry1]).protest_score() == 1)
        self.assertTrue(Table(-1, []).protest_score() == 0)
        self.assertTrue(Table(1, []).protest_score() == 0)
        self.assertTrue(Table(3, [entry1, entry1, entry1]).protest_score() == 3)
        self.assertTrue(Table(1, ['spanner', entry2]).protest_score() == 0)

        self.assertRaises(ValueError, Table, 'a', game)

    def test_protest_score_for_layout(self):
        """
        Protest object for a layout
        Should be something like [0s, 1s, 2s, totals]
        """
        entry1 = Entry(entry_id='entry1', game_history=[1, 2])
        entry2 = Entry(entry_id='entry1', game_history=[2, 1])
        entry3 = Entry(entry_id='entry1', game_history=[3, 2])
        entry4 = Entry(entry_id='entry1', game_history=[1, 3])
        entry5 = Entry(entry_id='entry1', game_history=[2, 3])
        entry6 = Entry(entry_id='entry1', game_history=[3, 1])

        func = ProtestAvoidanceStrategy.get_protest_score_for_layout

        layout = [
            Table(3, [entry1, entry2]), # should get 0
            Table(2, [entry3, entry4]), # should get 1 from e3
            Table(1, [entry5, entry6])] # should get 1 from e6
        result = func(layout)
        compare(result.protests, [1, 2, 0])
        compare(result.total_protests(), 2)

        layout = [
            Table(1, [entry1, entry2]), # should get 2
            Table(2, [entry3, entry4]), # should get 1 from e3
            Table(3, [entry5, entry6])] # should get 2 from e6
        result = func(layout)
        compare(result.protests, [0, 1, 2])
        compare(result.total_protests(), 5)


        layout = [Table(3, [entry1, entry2])] # should get 0
        result = func(layout)
        compare(result.protests, [1, 0, 0])
        compare(result.total_protests(), 0)


        layout = [] # should get 0
        result = func(layout)
        compare(result.protests, [0, 0, 0])
        compare(result.total_protests(), 0)


        layout = None
        self.assertRaises(TypeError, func, layout)

        layout = [
            Table(1, [entry1]), # should get 1
            Table(2, [entry3, entry4]), # explode as longer than first game
            Table(3, [entry5, entry6])]
        self.assertRaises(IndexError, func, layout)

    def test_determine_layouts(self):
        """
        We can change the history and you should get different draws
        """

        entry1 = Entry(entry_id='entry1', game_history=[1, 2])
        entry2 = Entry(entry_id='entry2', game_history=[2, 1])
        entry3 = Entry(entry_id='entry3', game_history=[3, 2])
        entry4 = Entry(entry_id='entry4', game_history=[1, 3])
        entry5 = Entry(entry_id='entry5', game_history=[2, 3])
        entry6 = Entry(entry_id='entry6', game_history=[3, 1])
        games = [(entry1, entry2), (entry3, entry4), (entry5, entry6)]
        strategy = ProtestAvoidanceStrategy()

        draw = strategy.determine_tables(games)
        compare(draw[2].entrants, [entry1, entry2])
        compare(draw[0].entrants, [entry3, entry4])
        compare(draw[1].entrants, [entry5, entry6])

        # if we swap matchup one and two they should switch places
        entry1.game_history = [3, 2]
        entry2.game_history = [1, 3]
        entry3.game_history = [1, 2]
        entry4.game_history = [2, 1]
        draw = strategy.determine_tables(games)
        compare(draw[0].entrants, [entry1, entry2])
        compare(draw[2].entrants, [entry3, entry4])
        compare(draw[1].entrants, [entry5, entry6])

from permissions import PermissionsChecker
class PermissionsTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `permissions.py`."""

    def test_is_admin(self):
        """check if a user is an admin"""
        checker = PermissionsChecker()

        self.assertFalse(checker.is_admin(None))
        self.assertFalse(checker.is_admin(''))
        self.assertFalse(checker.is_admin('charlie_murphy'))
        self.assertFalse(checker.is_admin('not_a_person'))

        self.assertTrue(checker.is_admin('superman'))

    def test_is_organiser(self):
        """check if a user is an organiser"""
        checker = PermissionsChecker()

        options = [None, 'ranking_test', 'not_a_tournament', '', 'lisa', \
            'not_a_person', 'superman', 'permission_test', 'lex_luthor']

        for user in options:
            for tourn in options:
                if user == 'lex_luthor' and tourn == 'permission_test':
                    self.assertTrue(checker.is_organiser(user, tourn))
                else:
                    self.assertFalse(checker.is_organiser(user, tourn))

    def test_is_player(self):
        """users can be a player by being involved in a game"""
        checker = PermissionsChecker()

        options = [None, '', 'lisa', 2, ]

        self.assertTrue(checker.is_game_player('lisa', 1))
        self.assertFalse(checker.is_game_player('lisa', 12))
        self.assertFalse(checker.is_game_player('superman', 1))
        self.assertFalse(checker.is_game_player('homer', 1))

        self.assertTrue(checker.is_tournament_player('lisa', 'ranking_test'))
        self.assertFalse(checker.is_tournament_player('superman', 'ranking_test'))

    def test_check_permissions(self):
        """Test the entrypoint method"""
        checker = PermissionsChecker()

        self.assertRaises(
            ValueError, checker.check_permission, None, None, None, None)
        self.assertRaises(
            ValueError, checker.check_permission, '', None, None, None)
        self.assertRaises(
            ValueError, checker.check_permission, 'not_a_list', None, None, None)
        self.assertRaises(
            ValueError, checker.check_permission, 'ENTER_SCORE', None, None, None)

        self.assertRaises(
            ValueError,
            checker.check_permission,
            'enter_score',
            None,
            None,
            None)
        self.assertTrue(checker.check_permission(
            'enter_score',
            'lex_luthor',
            None,
            'permission_test'))
        self.assertTrue(checker.check_permission(
            'enter_score',
            'superman',
            None,
            'permission_test'))
        self.assertTrue(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'permission_test_player',
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            'charlie_murphy',
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'permission_test_player',
            None,
            'permission_test'))
        self.assertFalse(checker.check_permission(
            'enter_score',
            'charlie_murphy',
            None,
            'permission_test'))

from game import get_game_from_score
class ScoreEnteringTests(unittest.TestCase):             # pylint: disable=R0904
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

if __name__ == '__main__':
    unittest.main()

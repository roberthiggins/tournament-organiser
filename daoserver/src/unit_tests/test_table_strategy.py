"""
The process by which players are allocated to tables
"""

import unittest
from testfixtures import compare

from models.tournament_entry import TournamentEntry
from table_strategy import ProtestAvoidanceStrategy, Table

class TableStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `table_strategy_strategy.py`."""

    def test_get_protest_score_for_game(self):
        """Test that individual games get the correct protest score"""
        entry1 = TournamentEntry('entry1', 'foo', game_history=[1, 3])
        entry2 = TournamentEntry('entry2', 'foo', game_history=[2, 3])
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
        entry1 = TournamentEntry('entry1', 'foo', game_history=[1, 2])
        entry2 = TournamentEntry('entry1', 'foo', game_history=[2, 1])
        entry3 = TournamentEntry('entry1', 'foo', game_history=[3, 2])
        entry4 = TournamentEntry('entry1', 'foo', game_history=[1, 3])
        entry5 = TournamentEntry('entry1', 'foo', game_history=[2, 3])
        entry6 = TournamentEntry('entry1', 'foo', game_history=[3, 1])

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

        entry1 = TournamentEntry('entry1', 'foo', game_history=[1, 2])
        entry2 = TournamentEntry('entry2', 'foo', game_history=[2, 1])
        entry3 = TournamentEntry('entry3', 'foo', game_history=[3, 2])
        entry4 = TournamentEntry('entry4', 'foo', game_history=[1, 3])
        entry5 = TournamentEntry('entry5', 'foo', game_history=[2, 3])
        entry6 = TournamentEntry('entry6', 'foo', game_history=[3, 1])
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

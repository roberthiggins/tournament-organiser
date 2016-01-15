"""
Tests for the Round Robin DrawStrategy
"""

import unittest
from testfixtures import compare

from draw_strategy import RoundRobin
from entry_db import Entry
from table_strategy import ProtestAvoidanceStrategy

class DrawStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `draw_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""
        draw_strategy = RoundRobin('ranking_test')
        draw = draw_strategy.draw(1)
        self.assertTrue(draw[0]['entry_1'].username == 'homer')
        self.assertTrue(draw[0]['entry_2'].username == 'maggie')
        self.assertTrue(draw[1]['entry_1'].username == 'marge')
        self.assertTrue(draw[1]['entry_2'].username == 'bart')
        self.assertTrue(draw[2]['entry_1'].username == 'lisa')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(2)
        self.assertTrue(draw[0]['entry_1'].username == 'maggie')
        self.assertTrue(draw[0]['entry_2'].username == 'bart')
        self.assertTrue(draw[1]['entry_1'].username == 'homer')
        self.assertTrue(draw[1]['entry_2'].username == 'lisa')
        self.assertTrue(draw[2]['entry_1'].username == 'marge')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(3)
        self.assertTrue(draw[0]['entry_1'].username == 'bart')
        self.assertTrue(draw[0]['entry_2'].username == 'lisa')
        self.assertTrue(draw[1]['entry_1'].username == 'maggie')
        self.assertTrue(draw[1]['entry_2'].username == 'marge')
        self.assertTrue(draw[2]['entry_1'].username == 'homer')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(4)
        self.assertTrue(draw[0]['entry_1'].username == 'lisa')
        self.assertTrue(draw[0]['entry_2'].username == 'marge')
        self.assertTrue(draw[1]['entry_1'].username == 'bart')
        self.assertTrue(draw[1]['entry_2'].username == 'homer')
        self.assertTrue(draw[2]['entry_1'].username == 'maggie')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(5)
        self.assertTrue(draw[0]['entry_1'].username == 'marge')
        self.assertTrue(draw[0]['entry_2'].username == 'homer')
        self.assertTrue(draw[1]['entry_1'].username == 'lisa')
        self.assertTrue(draw[1]['entry_2'].username == 'maggie')
        self.assertTrue(draw[2]['entry_1'].username == 'bart')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(6)
        self.assertTrue(draw[0]['entry_1'].username == 'homer')
        self.assertTrue(draw[0]['entry_2'].username == 'maggie')
        self.assertTrue(draw[1]['entry_1'].username == 'marge')
        self.assertTrue(draw[1]['entry_2'].username == 'bart')
        self.assertTrue(draw[2]['entry_1'].username == 'lisa')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

class TableStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `table_strategy_strategy.py`."""

    def test_get_protest_score_for_game(self):
        """Test that individual games get the correct protest score"""
        entry1 = Entry(entry_id='entry1', game_history=[1, 3])
        entry2 = Entry(entry_id='entry2', game_history=[2, 3])
        game = [entry1, entry2]
        func = ProtestAvoidanceStrategy.get_protest_score_for_game

        self.assertTrue(func(1, game) == 1)
        self.assertTrue(func(2, game) == 1)
        self.assertTrue(func(3, game) == 2)
        self.assertTrue(func(4, game) == 0)
        self.assertTrue(func(5, game) == 0)
        self.assertTrue(func(-1, game) == 0)
        self.assertTrue(func(-1, [entry1]) == 0)
        self.assertTrue(func(1, [entry1]) == 1)
        self.assertTrue(func(-1, []) == 0)
        self.assertTrue(func(1, []) == 0)
        self.assertTrue(func(3, [entry1, entry1, entry1]) == 3)

        self.assertRaises(AttributeError, func, 1, ['spanner', entry2])
        self.assertRaises(ValueError, func, 'a', game)

    def test_protest_score_for_layout(self):
        """
        Protest object for a layout
        Should be something like [total, 0s, 1s, 2s]
        """
        entry1 = Entry(entry_id='entry1', game_history=[1, 2])
        entry2 = Entry(entry_id='entry1', game_history=[2, 1])
        entry3 = Entry(entry_id='entry1', game_history=[3, 2])
        entry4 = Entry(entry_id='entry1', game_history=[1, 3])
        entry5 = Entry(entry_id='entry1', game_history=[2, 3])
        entry6 = Entry(entry_id='entry1', game_history=[3, 1])

        func = ProtestAvoidanceStrategy.get_protest_score_for_layout

        layout = [
            (3, [entry1, entry2]), # should get 0
            (2, [entry3, entry4]), # should get 1 from e3
            (1, [entry5, entry6])] # should get 1 from e6
        result = func(layout)
        compare(result.protests, [1, 2, 0])
        compare(result.total_protests(), 2)

        layout = [
            (1, [entry1, entry2]), # should get 2
            (2, [entry3, entry4]), # should get 1 from e3
            (3, [entry5, entry6])] # should get 2 from e6
        result = func(layout)
        compare(result.protests, [0, 1, 2])
        compare(result.total_protests(), 5)


        layout = [(3, [entry1, entry2])] # should get 0
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
            (1, [entry1]), # should get 1
            (2, [entry3, entry4]), # explode as longer than first game
            (3, [entry5, entry6])]
        self.assertRaises(IndexError, func, layout)

        layout = [
            (None, [entry1, entry2]), # explode
            (2, [entry3, entry4]),
            (3, [entry5, entry6])]
        self.assertRaises(TypeError, func, layout)

if __name__ == '__main__':
    unittest.main()

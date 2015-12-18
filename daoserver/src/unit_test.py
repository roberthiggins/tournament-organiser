"""
Tests for the Round Robin DrawStrategy
"""

import unittest

from draw_strategy import RoundRobin
from table_strategy import ProtestAvoidanceStrategy

class DrawStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `draw_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""
        draw_strategy = RoundRobin('ranking_test')
        draw = draw_strategy.draw(1)
        self.assertTrue(draw[0]['entry_1']['username'] == 'homer')
        self.assertTrue(draw[0]['entry_2']['username'] == 'maggie')
        self.assertTrue(draw[1]['entry_1']['username'] == 'marge')
        self.assertTrue(draw[1]['entry_2']['username'] == 'bart')
        self.assertTrue(draw[2]['entry_1']['username'] == 'lisa')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(2)
        self.assertTrue(draw[0]['entry_1']['username'] == 'maggie')
        self.assertTrue(draw[0]['entry_2']['username'] == 'bart')
        self.assertTrue(draw[1]['entry_1']['username'] == 'homer')
        self.assertTrue(draw[1]['entry_2']['username'] == 'lisa')
        self.assertTrue(draw[2]['entry_1']['username'] == 'marge')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(3)
        self.assertTrue(draw[0]['entry_1']['username'] == 'bart')
        self.assertTrue(draw[0]['entry_2']['username'] == 'lisa')
        self.assertTrue(draw[1]['entry_1']['username'] == 'maggie')
        self.assertTrue(draw[1]['entry_2']['username'] == 'marge')
        self.assertTrue(draw[2]['entry_1']['username'] == 'homer')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(4)
        self.assertTrue(draw[0]['entry_1']['username'] == 'lisa')
        self.assertTrue(draw[0]['entry_2']['username'] == 'marge')
        self.assertTrue(draw[1]['entry_1']['username'] == 'bart')
        self.assertTrue(draw[1]['entry_2']['username'] == 'homer')
        self.assertTrue(draw[2]['entry_1']['username'] == 'maggie')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(5)
        self.assertTrue(draw[0]['entry_1']['username'] == 'marge')
        self.assertTrue(draw[0]['entry_2']['username'] == 'homer')
        self.assertTrue(draw[1]['entry_1']['username'] == 'lisa')
        self.assertTrue(draw[1]['entry_2']['username'] == 'maggie')
        self.assertTrue(draw[2]['entry_1']['username'] == 'bart')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

        draw = draw_strategy.draw(6)
        self.assertTrue(draw[0]['entry_1']['username'] == 'homer')
        self.assertTrue(draw[0]['entry_2']['username'] == 'maggie')
        self.assertTrue(draw[1]['entry_1']['username'] == 'marge')
        self.assertTrue(draw[1]['entry_2']['username'] == 'bart')
        self.assertTrue(draw[2]['entry_1']['username'] == 'lisa')
        self.assertTrue(draw[2]['entry_2'] == 'BYE')

class TableStrategyTests(unittest.TestCase):             # pylint: disable=R0904
    """Tests for `table_strategy_strategy.py`."""

    def test_get_protest_score_for_game(self):
        """Test that individual games get the correct protest score"""
        entry1 = {'id': 'entry1', 'games': [1, 3]}
        entry2 = {'id': 'entry2', 'games': [2, 3]}
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

        self.assertRaises(TypeError, func, 1, ['spanner', entry2])
        self.assertRaises(ValueError, func, 'a', game)

if __name__ == '__main__':
    unittest.main()

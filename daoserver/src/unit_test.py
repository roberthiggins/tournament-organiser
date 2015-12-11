"""
Tests for the Round Robin DrawStrategy
"""

import unittest
from draw_strategy import RoundRobin

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

if __name__ == '__main__':
    unittest.main()

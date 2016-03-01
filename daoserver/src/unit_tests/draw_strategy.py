"""
Draw strategy unit tests
"""

import unittest

from matching_strategy import RoundRobin

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


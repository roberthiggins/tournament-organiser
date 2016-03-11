"""
Draw strategy unit tests
"""

from flask.ext.testing import TestCase

from app import create_app
from matching_strategy import RoundRobin
from models.db_connection import db
from tournament import Tournament

# pylint: disable=no-member,no-init,invalid-name,missing-docstring,undefined-variable
class DrawStrategyTests(TestCase):
    """Tests for `matching_strategy.py`."""

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_get_draw(self):
        """Test get_draw"""
        entries = Tournament('ranking_test').entries()
        matching_strategy = RoundRobin()
        draw = matching_strategy.match(1, entries)
        self.assertTrue(draw[0][0].username == 'homer')
        self.assertTrue(draw[0][1].username == 'maggie')
        self.assertTrue(draw[1][0].username == 'marge')
        self.assertTrue(draw[1][1].username == 'bart')
        self.assertTrue(draw[2][0].username == 'lisa')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(2, entries)
        self.assertTrue(draw[0][0].username == 'maggie')
        self.assertTrue(draw[0][1].username == 'bart')
        self.assertTrue(draw[1][0].username == 'homer')
        self.assertTrue(draw[1][1].username == 'lisa')
        self.assertTrue(draw[2][0].username == 'marge')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(3, entries)
        self.assertTrue(draw[0][0].username == 'bart')
        self.assertTrue(draw[0][1].username == 'lisa')
        self.assertTrue(draw[1][0].username == 'maggie')
        self.assertTrue(draw[1][1].username == 'marge')
        self.assertTrue(draw[2][0].username == 'homer')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(4, entries)
        self.assertTrue(draw[0][0].username == 'lisa')
        self.assertTrue(draw[0][1].username == 'marge')
        self.assertTrue(draw[1][0].username == 'bart')
        self.assertTrue(draw[1][1].username == 'homer')
        self.assertTrue(draw[2][0].username == 'maggie')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(5, entries)
        self.assertTrue(draw[0][0].username == 'marge')
        self.assertTrue(draw[0][1].username == 'homer')
        self.assertTrue(draw[1][0].username == 'lisa')
        self.assertTrue(draw[1][1].username == 'maggie')
        self.assertTrue(draw[2][0].username == 'bart')
        self.assertTrue(draw[2][1] == 'BYE')

        draw = matching_strategy.match(6, entries)
        self.assertTrue(draw[0][0].username == 'homer')
        self.assertTrue(draw[0][1].username == 'maggie')
        self.assertTrue(draw[1][0].username == 'marge')
        self.assertTrue(draw[1][1].username == 'bart')
        self.assertTrue(draw[2][0].username == 'lisa')
        self.assertTrue(draw[2][1] == 'BYE')


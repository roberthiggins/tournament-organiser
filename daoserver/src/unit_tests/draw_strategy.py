"""
Draw strategy unit tests
"""
# pylint: disable=invalid-name,missing-docstring

from flask_testing import TestCase
from testfixtures import compare

from app import create_app
from models.matching_strategy import RoundRobin
from models.dao.db_connection import db
from models.tournament import Tournament

from unit_tests.tournament_injector import TournamentInjector

class DrawStrategyTests(TestCase):
    """Tests for `matching_strategy.py`."""

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_get_draw(self):
        """Test get_draw"""

        self.injector.inject('dst', rounds=5, num_players=5)

        entries = Tournament('dst').entries()
        matching_strategy = RoundRobin()
        draw = matching_strategy.match(1, entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')

        draw = matching_strategy.match(2, entries)
        compare(draw[0][0].player_id, 'dst_player_5')
        compare(draw[0][1].player_id, 'dst_player_4')
        compare(draw[1][0].player_id, 'dst_player_1')
        compare(draw[1][1].player_id, 'dst_player_3')
        compare(draw[2][0].player_id, 'dst_player_2')
        compare(draw[2][1], 'BYE')

        draw = matching_strategy.match(3, entries)
        compare(draw[0][0].player_id, 'dst_player_4')
        compare(draw[0][1].player_id, 'dst_player_3')
        compare(draw[1][0].player_id, 'dst_player_5')
        compare(draw[1][1].player_id, 'dst_player_2')
        compare(draw[2][0].player_id, 'dst_player_1')
        compare(draw[2][1], 'BYE')

        draw = matching_strategy.match(4, entries)
        compare(draw[0][0].player_id, 'dst_player_3')
        compare(draw[0][1].player_id, 'dst_player_2')
        compare(draw[1][0].player_id, 'dst_player_4')
        compare(draw[1][1].player_id, 'dst_player_1')
        compare(draw[2][0].player_id, 'dst_player_5')
        compare(draw[2][1], 'BYE')

        draw = matching_strategy.match(5, entries)
        compare(draw[0][0].player_id, 'dst_player_2')
        compare(draw[0][1].player_id, 'dst_player_1')
        compare(draw[1][0].player_id, 'dst_player_3')
        compare(draw[1][1].player_id, 'dst_player_5')
        compare(draw[2][0].player_id, 'dst_player_4')
        compare(draw[2][1], 'BYE')

        draw = matching_strategy.match(6, entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')


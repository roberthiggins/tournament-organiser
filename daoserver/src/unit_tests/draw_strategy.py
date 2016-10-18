"""
Draw strategy unit tests
"""
# pylint: disable=invalid-name,missing-docstring

from testfixtures import compare

from models.matching_strategy import RoundRobin
from models.tournament import Tournament

from unit_tests.db_simulating_test import DbSimulatingTest

class DrawStrategyTests(DbSimulatingTest):
    """Tests for `matching_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""

        self.injector.inject('dst', num_players=5)

        entries = Tournament('dst').get_entries()
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

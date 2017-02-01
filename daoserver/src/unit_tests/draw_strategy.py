"""
Draw strategy unit tests
"""
# pylint: disable=invalid-name,missing-docstring

from testfixtures import compare

from models.matching_strategy import RoundRobin
from models.tournament import Tournament

from unit_tests.app_simulating_test import AppSimulatingTest

class DrawStrategyTests(AppSimulatingTest):
    """Tests for `matching_strategy.py`."""

    def test_get_draw(self):
        """Test get_draw"""

        self.injector.inject('dst', num_players=5)

        entries = Tournament('dst').get_entries()
        draw = RoundRobin().set_round(1).match(entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(2).match(entries)
        compare(draw[0][0].player_id, 'dst_player_5')
        compare(draw[0][1].player_id, 'dst_player_4')
        compare(draw[1][0].player_id, 'dst_player_1')
        compare(draw[1][1].player_id, 'dst_player_3')
        compare(draw[2][0].player_id, 'dst_player_2')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(3).match(entries)
        compare(draw[0][0].player_id, 'dst_player_4')
        compare(draw[0][1].player_id, 'dst_player_3')
        compare(draw[1][0].player_id, 'dst_player_5')
        compare(draw[1][1].player_id, 'dst_player_2')
        compare(draw[2][0].player_id, 'dst_player_1')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(4).match(entries)
        compare(draw[0][0].player_id, 'dst_player_3')
        compare(draw[0][1].player_id, 'dst_player_2')
        compare(draw[1][0].player_id, 'dst_player_4')
        compare(draw[1][1].player_id, 'dst_player_1')
        compare(draw[2][0].player_id, 'dst_player_5')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(5).match(entries)
        compare(draw[0][0].player_id, 'dst_player_2')
        compare(draw[0][1].player_id, 'dst_player_1')
        compare(draw[1][0].player_id, 'dst_player_3')
        compare(draw[1][1].player_id, 'dst_player_5')
        compare(draw[2][0].player_id, 'dst_player_4')
        compare(draw[2][1], 'BYE')

        draw = RoundRobin().set_round(6).match(entries)
        compare(draw[0][0].player_id, 'dst_player_1')
        compare(draw[0][1].player_id, 'dst_player_5')
        compare(draw[1][0].player_id, 'dst_player_2')
        compare(draw[1][1].player_id, 'dst_player_4')
        compare(draw[2][0].player_id, 'dst_player_3')
        compare(draw[2][1], 'BYE')

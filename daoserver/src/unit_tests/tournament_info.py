"""
Retrieving tournament info
"""

from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from models.tournament import db as tournament_db
from tournament import Tournament

# pylint: disable=C0111,C0103,W0232
class TournamentInfo(TestCase):

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):

        tournament_db.create_all()

    def tearDown(self):

        tournament_db.session.remove()

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
                ('round_3_battle', 25, 0, 3, 6, 3))

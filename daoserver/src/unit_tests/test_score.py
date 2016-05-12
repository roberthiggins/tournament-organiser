"""
Joing a score key to a round instance
"""
from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from models.db_connection import db
from models.score import RoundScore, ScoreCategory, ScoreKey
from models.tournament import db, Tournament as TournamentDAO
from models.tournament_round import TournamentRound
from tournament import Tournament

# pylint: disable=no-member,no-init,invalid-name,missing-docstring
class TestRoundScore(TestCase):
    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_get_score_keys(self):
        """Get the score keys linked to the round"""

        tourn = Tournament('ranking_test')
        tourn.set_number_of_rounds(5)

        # make a bogus tournament in the hopes we can select a key from another
        # tournament
        t = TournamentDAO('foobar')
        t.date = '2015-07-08'
        t.num_rounds = 5
        t.write()

        cat = ScoreCategory('foobar', 'nonsense', 50, False)
        cat.tournament = t
        cat.write()

        key = ScoreKey('some_key', cat.id, 0, 100)
        key.score_category = cat
        db.session.add(key)

        rnd = TournamentRound('foobar', 1, 'foo_mission_1')
        db.session.add(rnd)

        score = RoundScore(key.id, 1)
        score.score_id = key
        score.round = rnd
        db.session.add(score)

        round_1_keys_exp = [
            ('round_1_battle', 0, 20),
            ('sports', 1, 5)
        ]
        round_1_keys_act = [x[1:4] for x in tourn.get_round(1).get_score_keys()]
        compare(round_1_keys_exp, round_1_keys_act)

        round_2_keys_exp = [
            ('round_2_battle', 0, 20),
        ]
        round_2_keys_act = [x[1:4] for x in tourn.get_round(2).get_score_keys()]
        compare(round_2_keys_exp, round_2_keys_act)

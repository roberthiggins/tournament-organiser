"""
Joing a score key to a round instance
"""
from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from models.score import RoundScore, ScoreCategory, ScoreKey
from models.tournament import db, Tournament as TournamentDAO
from models.tournament_round import TournamentRound
from tournament import Tournament

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
        dao = TournamentDAO.query.filter_by(name='ranking_test').first()

        # make a bogus tournament in the hopes we can select a key from another
        # tournament
        t = TournamentDAO('foobar')
        t.date = '2015-07-08'
        t.num_rounds = 5
        t.write()

        cat = ScoreCategory('foobar', 'nonsense', 50)
        cat.tournament = t
        cat.write()

        key = ScoreKey('some_key', 0, 100, cat.id)
        key.score_category = cat
        key.write()

        rd = TournamentRound('foobar', 1, 'foo_mission_1')
        rd.write()

        score = RoundScore(key.id, 1)
        score.score_id = key
        score.round = rd
        score.write()

        round_1_keys_exp = [
            ('round_1_battle', 0, 20, 3, 3, 1),
            ('sports', 1, 5, 4, 5, 1)
        ]
        round_1_keys_act = [x[1:] for x in tourn.get_score_keys_for_round(1)]
        compare(round_1_keys_exp, round_1_keys_act)

        round_2_keys_exp = [
            ('round_2_battle', 0, 20, 3, 4, 2),
        ]
        round_2_keys_act = [x[1:] for x in tourn.get_score_keys_for_round(2)]
        compare(round_2_keys_exp, round_2_keys_act)

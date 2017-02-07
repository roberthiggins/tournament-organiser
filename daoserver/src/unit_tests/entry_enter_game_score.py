"""
Test entering scores for games in a tournament
"""

from sqlalchemy.sql.expression import and_
from testfixtures import compare

from models.dao.game_entry import GameEntrant
from models.dao.score import GameScore, Score as ScoreDAO
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound

from models.score import Score
from models.tournament import Tournament

from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args as cat

# pylint: disable=no-member,missing-docstring
class EnterScore(AppSimulatingTest):

    tourn_1 = 'enter_score_tournament'

    def setUp(self):
        super(EnterScore, self).setUp()
        self.injector.inject(self.tourn_1, num_players=5)
        tourn = Tournament(self.tourn_1)
        tourn.update({
            'rounds': 2,
            'missions': ['foo_mission_1', 'foo_mission_2'],
            'score_categories': [cat('per_round', 50, False, 0, 100)]
        })
        self.cat_1 = 'per_round'
        self.entry = TournamentEntry.query.\
            filter_by(tournament_id=self.tourn_1).first().id

    def test_enter_score_bad_games(self):
        """These should all fail for one reason or another"""
        good_args = {
            'tournament': Tournament(self.tourn_1),
            'entry_id': self.entry,
            'category': self.cat_1,
            'score': 5
        }
        self.assertRaises(TypeError, Score, game_id='foo', **good_args)
        self.assertRaises(TypeError, Score, game_id=1000000, **good_args)
        self.assertRaises(TypeError, Score, game_id=-1, **good_args)

    def test_enter_score(self):
        """
        Enter a score for an entry
        """
        tourn = Tournament(self.tourn_1)

        # a per_round score
        tourn.make_draws()

        round_id = TournamentRound.query.\
            filter_by(tournament_name=self.tourn_1, ordering=2).first().id
        game_id = TournamentGame.query.join(GameEntrant).\
            filter(and_(GameEntrant.entrant_id == self.entry,
                        TournamentGame.tournament_round_id == round_id)).\
                first().id
        Score(category=self.cat_1, tournament=tourn, game_id=game_id,
              entry_id=self.entry, score=17).write()
        scores = GameScore.query.\
            filter_by(entry_id=self.entry, game_id=game_id).all()
        compare(len(scores), 1)
        compare(scores[0].score.value, 17)

        # score already entered
        score = Score(tournament=tourn, entry_id=self.entry, score=100,
                      category=self.cat_1, game_id=game_id)
        self.assertRaises(ValueError, score.write)

    def test_enter_score_cleanup(self):
        """make sure no scores are added accidentally"""
        game_scores = len(GameScore.query.all())
        scores = len(ScoreDAO.query.all())

        self.test_enter_score_bad_games()

        compare(game_scores, len(GameScore.query.all()))
        compare(scores, len(ScoreDAO.query.all()))

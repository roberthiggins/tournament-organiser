"""
Test entering scores for games in a tournament
"""

from testfixtures import compare

from models.dao.score import ScoreCategory, TournamentScore, Score as ScoreDAO
from models.dao.tournament_entry import TournamentEntry

from models.score import Score
from models.tournament import Tournament
from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args as cat

# pylint: disable=no-member,missing-docstring
class EnterScore(AppSimulatingTest):

    player = 'enter_score_account'
    tourn_1 = 'enter_score_tournament'

    def setUp(self):
        super(EnterScore, self).setUp()
        self.injector.inject(self.tourn_1, num_players=5)
        self.injector.add_player(self.tourn_1, self.player)

        # per tournament category
        self.cat_1 = ScoreCategory(tournament_id=self.tourn_1,
                                   **cat('per_tournament', 50, True, 0, 100))
        self.db.session.add(self.cat_1)

        self.db.session.commit()

    def test_enter_score_bad_values(self):
        """These should all fail for one reason or another"""
        entry = TournamentEntry.query.filter_by(
            player_id=self.player, tournament_id=self.tourn_1).first()

        # bad entry
        self.assertRaises(
            ValueError,
            Score,
            tournament=Tournament(self.tourn_1),
            entry_id=10000000,
            category=self.cat_1.name,
            score=5)
        # bad key
        self.assertRaises(
            TypeError,
            Score,
            tournament=Tournament(self.tourn_1),
            entry_id=entry.id,
            category='not_a_key',
            score=5)
        # bad score - character
        self.assertRaises(
            ValueError,
            Score,
            tournament=Tournament(self.tourn_1),
            entry_id=entry.id,
            category=self.cat_1.name,
            score='a')
        # bad score - low
        score = Score(tournament=Tournament(self.tourn_1), entry_id=entry.id,
                      category=self.cat_1.name, score=-1)
        self.assertRaises(ValueError, score.write)
        # bad score - high
        score = Score(tournament=Tournament(self.tourn_1), entry_id=entry.id,
                      category=self.cat_1.name, score=101)
        self.assertRaises(ValueError, score.write)


    def test_enter_score(self):
        """
        Enter a score for an entry
        """
        entry = TournamentEntry.query.filter_by(
            player_id=self.player, tournament_id=self.tourn_1).first()
        tourn = Tournament(self.tourn_1)

        # a one-off score
        Score(category=self.cat_1.name, tournament=tourn, entry_id=entry.id,
              score=0).write()
        scores = TournamentScore.query.\
            filter_by(entry_id=entry.id, tournament_id=tourn.get_dao().id).all()
        compare(len(scores), 1)
        compare(scores[0].score.value, 0)

        # score already entered
        score = Score(tournament=tourn, entry_id=entry.id, score=100,
                      category=self.cat_1.name)
        self.assertRaises(ValueError, score.write)

    def test_enter_score_cleanup(self):
        """make sure no scores are added accidentally"""
        tournament_scores = len(TournamentScore.query.all())
        scores = len(ScoreDAO.query.all())

        self.test_enter_score_bad_values()

        compare(tournament_scores, len(TournamentScore.query.all()))
        compare(scores, len(ScoreDAO.query.all()))

"""
Test entering scores for games in a tournament
"""

from sqlalchemy.sql.expression import and_
from testfixtures import compare

from models.dao.game_entry import GameEntrant
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound

from models.score import Score
from models.tournament import Tournament
from unit_tests.app_simulating_test import AppSimulatingTest
from unit_tests.tournament_injector import score_cat_args

# pylint: disable=no-member,missing-docstring
class TestScoreEntered(AppSimulatingTest):

    tournament_1 = 'score_entered_tournament'

    def setUp(self):
        super(TestScoreEntered, self).setUp()

        self.injector.inject(self.tournament_1, num_players=5)
        tourn = Tournament(self.tournament_1)
        tourn.update({
            'rounds': 2,
            'missions': ['foo_mission_1', 'foo_mission_2']
        })

    def test_get_game_from_score(self):
        """
        You should be able to determine game from entry_id and the score_cat
        """
        entry_2_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 2),
            tournament_id=self.tournament_1).first().id
        entry_3_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 3),
            tournament_id=self.tournament_1).first().id
        entry_4_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 4),
            tournament_id=self.tournament_1).first().id

        # A regular player
        game = self.get_game_by_round(entry_4_id, 1)
        self.assertTrue(game is not None)

        game = self.get_game_by_round(entry_4_id, 1)
        entrants = [x.entrant_id for x in game.entrants.all()]
        compare(len(entrants), 2)
        self.assertTrue(entry_4_id in entrants)
        self.assertTrue(entry_2_id in entrants)

        # A player in a bye
        game = self.get_game_by_round(entry_3_id, 1)
        entrants = [x.entrant_id for x in game.entrants.all()]
        compare(len(entrants), 1)
        self.assertTrue(entry_3_id in entrants)

        # Poor data will return None rather than an error
        game = self.get_game_by_round(15, 1)
        self.assertTrue(game is None)
        game = self.get_game_by_round(1, 12)
        self.assertTrue(game is None)


    def test_no_scores(self):
        """
        There should be an error when you check a game before score categories \
        are assigned to it.
        """
        entry_1_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 1),
            tournament_id=self.tournament_1).first().id
        game = self.get_game_by_round(entry_1_id, 1)
        self.assertRaises(AttributeError, Score.is_score_entered, game)


    def test_score_entered(self):
        # Add a score category
        Tournament(self.tournament_1).update({
            'score_categories': [score_cat_args('per_round', 50, False, 0, 100)]
        })
        category_1 = 'per_round'

        tourn = Tournament(self.tournament_1)

        entry_2_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 2),
            tournament_id=self.tournament_1).first().id
        entry_3_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 3),
            tournament_id=self.tournament_1).first().id
        entry_4_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 4),
            tournament_id=self.tournament_1).first().id
        entry_5_id = TournamentEntry.query.filter_by(
            player_id='{}_player_{}'.format(self.tournament_1, 5),
            tournament_id=self.tournament_1).first().id

        # A completed game
        game = self.get_game_by_round(entry_4_id, 1)
        Score(category=category_1, game_id=game.id, tournament=tourn,
              entry_id=entry_2_id, score=2).write()
        Score(category=category_1, game_id=game.id, tournament=tourn,
              entry_id=entry_4_id, score=4).write()
        entrants = [x.entrant_id for x in game.entrants.all()]
        self.assertTrue(entry_2_id in entrants)
        self.assertTrue(entry_4_id in entrants)
        self.assertTrue(Score.is_score_entered(game))

        # A BYE will only have one entrant
        game = self.get_game_by_round(entry_3_id, 1)
        Score(category=category_1, game_id=game.id, tournament=tourn,
              entry_id=entry_3_id, score=3).write()
        entrants = [x.entrant_id for x in game.entrants.all()]
        compare(len(entrants), 1)
        self.assertTrue(entry_3_id in entrants)
        self.assertTrue(Score.is_score_entered(game))

        # Ensure the rd2 game entry_4 vs. entry_5 is listed as not scored. This
        # will force a full check. entry_5's score hasn't been entered.
        game = self.get_game_by_round(entry_4_id, 2)
        game.score_entered = False
        self.db.session.add(game)
        self.db.session.flush()

        game = self.get_game_by_round(entry_4_id, 2)
        entrants = [x.entrant_id for x in game.entrants.all()]
        Score(category=category_1, game_id=game.id, tournament=tourn,
              entry_id=entry_4_id, score=4).write()
        self.assertTrue(entry_4_id in entrants)
        self.assertTrue(entry_5_id in entrants)
        self.assertFalse(Score.is_score_entered(game))

        # Enter the final score for entry_5
        tourn = Tournament(self.tournament_1)
        Score(category=category_1, game_id=game.id, tournament=tourn,
              entry_id=entry_5_id, score=5).write()
        self.assertTrue(Score.is_score_entered(game))

    @staticmethod
    def get_game_by_round(entry_id, round_num):
        """Get the game an entry played in during a round"""
        entry_dao = TournamentEntry.query.filter_by(id=entry_id).first()

        if entry_dao is None:
            return None
        round_dao = TournamentRound.query.filter_by(
            ordering=round_num, tournament_name=entry_dao.tournament.name).\
            first()

        if round_dao is None:
            return None
        return TournamentGame.query.join(GameEntrant).\
            join(TournamentEntry).filter(
                and_(TournamentGame.tournament_round_id == round_dao.id,
                     TournamentEntry.id == entry_id)).first()

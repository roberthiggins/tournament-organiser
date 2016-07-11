"""
Test entering scores for games in a tournament
"""

from flask_testing import TestCase
from sqlalchemy.sql.expression import and_
from testfixtures import compare

from app import create_app
from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.score import ScoreCategory
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound

from models.tournament import Tournament
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,invalid-name,missing-docstring,undefined-variable
class TestScoreEntered(TestCase):
    """Comes from a range of files"""

    tournament_1 = 'score_entered_tournament'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()
        self.injector.inject(self.tournament_1, rounds=5, num_players=5)
        db.session.add(TournamentRound(self.tournament_1, 1, 'foo_mission_1'))
        db.session.add(TournamentRound(self.tournament_1, 2, 'foo_mission_2'))
        db.session.flush()
        Tournament(self.tournament_1).make_draw(1)
        Tournament(self.tournament_1).make_draw(2)

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

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
        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).is_score_entered,
            game)


    def test_score_entered(self):
        # Add a score category
        category_1 = ScoreCategory(self.tournament_1, 'per_round', 50, False,
                                   0, 100)
        db.session.add(category_1)
        db.session.flush()

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
        tourn.enter_score(entry_2_id, category_1.display_name, 2, game.id)
        tourn.enter_score(entry_4_id, category_1.display_name, 4, game.id)
        entrants = [x.entrant_id for x in game.entrants.all()]
        self.assertTrue(entry_2_id in entrants)
        self.assertTrue(entry_4_id in entrants)
        self.assertTrue(Tournament.is_score_entered(game))

        # A BYE will only have one entrant
        game = self.get_game_by_round(entry_3_id, 1)
        tourn.enter_score(entry_3_id, category_1.display_name, 3, game.id)
        entrants = [x.entrant_id for x in game.entrants.all()]
        compare(len(entrants), 1)
        self.assertTrue(entry_3_id in entrants)
        self.assertTrue(Tournament.is_score_entered(game))

        # Ensure the rd2 game entry_4 vs. entry_5 is listed as not scored. This
        # will force a full check. entry_5's score hasn't been entered.
        game = self.get_game_by_round(entry_4_id, 2)
        game.score_entered = False
        db.session.add(game)
        db.session.flush()

        game = self.get_game_by_round(entry_4_id, 2)
        entrants = [x.entrant_id for x in game.entrants.all()]
        tourn.enter_score(entry_4_id, category_1.display_name, 4, game.id)
        self.assertTrue(entry_4_id in entrants)
        self.assertTrue(entry_5_id in entrants)
        self.assertFalse(Tournament.is_score_entered(game))

        # Enter the final score for entry_5
        tourn = Tournament(self.tournament_1)
        tourn.enter_score(entry_5_id, category_1.display_name, 5, game.id)
        self.assertTrue(Tournament.is_score_entered(game))

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

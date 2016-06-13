"""
Test entering scores for games in a tournament
"""

from flask_testing import TestCase
from sqlalchemy.sql.expression import and_
from testfixtures import compare

from app import create_app
from models.db_connection import db
from models.game_entry import GameEntrant
from models.score import ScoreCategory, ScoreKey, TournamentScore, GameScore, \
Score
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame
from models.tournament_round import TournamentRound

from tournament import Tournament
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,invalid-name,missing-docstring,undefined-variable
class EnterScore(TestCase):

    player = 'enter_score_account'
    tournament_1 = 'enter_score_tournament'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()
        self.injector.inject(self.tournament_1, rounds=5, num_players=5)
        db.session.add(TournamentRound(self.tournament_1, 1, 'foo_mission_1'))
        db.session.add(TournamentRound(self.tournament_1, 2, 'foo_mission_2'))
        self.injector.add_player(self.tournament_1, self.player)

        # per tournament category
        self.category_1 = ScoreCategory(self.tournament_1, 'per_tourn', 50,
                                        True, 0, 100)
        db.session.add(self.category_1)
        db.session.flush()
        self.key_1 = ScoreKey('test_enter_score_key_1', self.category_1.id)
        db.session.add(self.key_1)

        # per round category
        self.category_2 = ScoreCategory(self.tournament_1, 'per_round', 50,
                                        False, 0, 100)
        db.session.add(self.category_2)
        db.session.flush()
        self.key_2 = ScoreKey('test_enter_score_key_2', self.category_2.id)
        db.session.add(self.key_2)
        db.session.commit()

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

    def test_enter_score_bad_games(self):
        """These should all fail for one reason or another"""
        entry = TournamentEntry.query.filter_by(
            player_id=self.player, tournament_id=self.tournament_1).first()

        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            5,
            game_id='foo')
        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            5,
            game_id=1000000)
        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            5,
            game_id=-1)
        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            5,
            game_id=0)

    def test_enter_score_bad_values(self):
        """These should all fail for one reason or another"""
        entry = TournamentEntry.query.filter_by(
            player_id=self.player, tournament_id=self.tournament_1).first()

        # bad entry
        self.assertRaises(
            AttributeError,
            Tournament(self.tournament_1).enter_score,
            10000000,
            self.key_1.key,
            5)
        # bad key
        self.assertRaises(
            TypeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            'not_a_key',
            5)
        # bad score - low
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            -1)
        # bad score - high
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            101)
        # bad score - character
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            'a')

    def test_enter_score(self):
        """
        Enter a score for an entry
        """
        entry = TournamentEntry.query.filter_by(
            player_id=self.player, tournament_id=self.tournament_1).first()
        tourn = Tournament(self.tournament_1)

        # a one-off score
        tourn.enter_score(entry.id, self.key_1.key, 0)
        scores = TournamentScore.query.\
            filter_by(entry_id=entry.id, tournament_id=tourn.get_dao().id).all()
        compare(len(scores), 1)
        compare(scores[0].score.value, 0)

        # a per_round score
        tourn.make_draw(1)
        tourn.make_draw(2)

        round_id = TournamentRound.query.\
            filter_by(tournament_name=self.tournament_1, ordering=2).first().id
        game_id = TournamentGame.query.join(GameEntrant).\
            filter(and_(GameEntrant.entrant_id == entry.id,
                        TournamentGame.tournament_round_id == round_id)).\
                first().id
        tourn.enter_score(entry.id, self.key_2.key, 17, game_id=game_id)
        scores = GameScore.query.\
            filter_by(entry_id=entry.id, game_id=game_id).all()
        compare(len(scores), 1)
        compare(scores[0].score.value, 17)

        # score already entered
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            100)

        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_2.key,
            100,
            game_id=game_id)

    def test_enter_score_cleanup(self):
        """make sure no scores are added accidentally"""
        game_scores = len(GameScore.query.all())
        tournament_scores = len(TournamentScore.query.all())
        scores = len(Score.query.all())

        self.test_enter_score_bad_games()
        self.test_enter_score_bad_values()

        compare(game_scores, len(GameScore.query.all()))
        compare(tournament_scores, len(TournamentScore.query.all()))
        compare(scores, len(Score.query.all()))

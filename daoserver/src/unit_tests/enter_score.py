"""
Test entering scores for games in a tournament
"""

from flask.ext.testing import TestCase
from sqlalchemy.sql.expression import and_
from testfixtures import compare

from app import create_app
from db_connections.db_connection import db_conn
from game import Game
from models.db_connection import db, write_to_db
from models.game_entry import GameEntrant
from models.score import ScoreCategory, ScoreKey, TournamentScore
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame
from models.tournament_round import TournamentRound

from tournament import Tournament
from unit_tests.tournament_injector import TournamentInjector

# pylint: disable=no-member,invalid-name,missing-docstring,undefined-variable
class ScoreEnteringTests(TestCase):
    """Comes from a range of files"""

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_get_game_from_score(self):
        """
        You should be able to determine game from entry_id and the score_key
        """

        # A regular player
        game = self.get_game_by_round(5, 1)
        self.assertTrue(game is not None)

        game = self.get_game_by_round(5, 1)
        entrants = game.get_dao().entrants.all()
        self.assertTrue(entrants[0].entrant_id is not None)
        self.assertTrue(entrants[1].entrant_id is not None)
        self.assertTrue(entrants[0].entrant_id == 5 \
        or entrants[1].entrant_id == 5)
        self.assertTrue(entrants[0].entrant_id == 3 \
        or entrants[1].entrant_id == 3)


        # A player in a bye
        game = self.get_game_by_round(4, 1)
        entrants = game.get_dao().entrants.all()
        self.assertTrue(entrants[0].entrant_id == 4)
        self.assertTrue(len(entrants) == 1)


        # Poor data will return None rather than an error
        game = self.get_game_by_round(15, 1)
        self.assertTrue(game is None)
        game = self.get_game_by_round(1, 12)
        self.assertTrue(game is None)


    @db_conn()
    def test_score_entered(self):

        # A completed game
        game = self.get_game_by_round(5, 1)
        entrants = game.get_dao().entrants.all()
        compare(entrants[0].entrant_id, 3)
        compare(entrants[1].entrant_id, 5)
        self.assertTrue(game.is_score_entered())

        # a bye should be false
        # TODO resolve Bye Scoring
        game = self.get_game_by_round(4, 1)
        entrants = game.get_dao().entrants.all()
        compare(entrants[0].entrant_id, 4)
        self.assertFalse(game.is_score_entered())

        # Ensure the rd2 game bart vs. maggie is listed as not scored. This
        # will force a full check. Maggie's score hasn't been entered.
        cur.execute("UPDATE game SET score_entered = False WHERE id = 5")
        game = self.get_game_by_round(5, 2)

        entrants = game.get_dao().entrants.all()
        compare(entrants[0].entrant_id, 6)
        compare(entrants[1].entrant_id, 5)
        self.assertFalse(game.is_score_entered())

        # Enter the final score for maggie
        cur.execute("INSERT INTO score VALUES(DEFAULT, 6, 4, 2)")
        conn.commit()
        self.assertTrue(game.is_score_entered())

    def test_list_scores_for_game(self):
        """
        Games have a scores_entered which should return all the scores entered
        for by each entrant.
        """
        # Bye
        game = self.get_game_by_round(4, 1)
        compare(
            game.scores_entered(),
            [(4, 'round_1_battle', None), (4, 'sports', 5)])

        # Regular, completed game
        game = self.get_game_by_round(2, 1)
        compare(
            game.scores_entered(),
            [(6, 'round_1_battle', 0), (2, 'round_1_battle', 20),
             (6, 'sports', 5), (2, 'sports', 1)])

        # Game partially filled in
        game = self.get_game_by_round(5, 2)
        compare(
            game.scores_entered(),
            [(5, 'round_2_battle', 5)])

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
        game_dao = TournamentGame.query.join(GameEntrant).\
            join(TournamentEntry).filter(
                and_(TournamentGame.tournament_round_id == round_dao.id,
                     TournamentEntry.id == entry_id)).first()

        if game_dao is None:
            return None
        return Game(game_id=game_dao.id)

class EnterScore(TestCase):

    player = 'enter_score_account'
    tournament_1 = 'enter_score_tournament'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()
        self.injector = TournamentInjector()
        self.injector.inject(self.tournament_1, rounds=5)
        db.session.add(TournamentRound(self.tournament_1, 1, 'foo_mission_1'))
        self.injector.add_player(self.tournament_1, self.player)
        self.category_1 = ScoreCategory(self.tournament_1, 'nonsense', 50,
                                        False, 0, 100)
        write_to_db(self.category_1)
        self.key_1 = ScoreKey('test_enter_score_key', self.category_1.id)
        write_to_db(self.key_1)

    def tearDown(self):
        self.injector.delete()
        db.session.remove()

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

        # score already entered
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            self.key_1.key,
            100)

"""
Test entering scores for games in a tournament
"""

from flask.ext.testing import TestCase
from testfixtures import compare

from app import create_app
from db_connections.db_connection import db_conn
from models.db_connection import db
from game import Game

# pylint: disable=no-member,no-init,invalid-name,missing-docstring,undefined-variable
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
        game = self.get_game_from_score(5, 'sports')
        self.assertTrue(game is not None)

        game = self.get_game_from_score(5, 'round_1_battle')
        self.assertTrue(game is not None)
        self.assertTrue(game.get_dao().entrants[0].entrant_id is not None)
        self.assertTrue(game.get_dao().entrants[1].entrant_id is not None)
        self.assertTrue(game.get_dao().entrants[0].entrant_id == 5 \
        or game.get_dao().entrants[1].entrant_id == 5)
        self.assertTrue(game.get_dao().entrants[0].entrant_id == 3 \
        or game.get_dao().entrants[1].entrant_id == 3)


        # A score that isn't tied to a game
        game = self.get_game_from_score(1, 'number_tassles')
        self.assertTrue(game is None)


        # A player in a bye
        game = self.get_game_from_score(4, 'round_1_battle')
        self.assertTrue(game is not None)
        self.assertTrue(game.get_dao().entrants[0].entrant_id == 4)
        self.assertTrue(len(game.get_dao().entrants) == 1)


        # Poor data will return None rather than an error
        game = self.get_game_from_score(15, 'round_1_battle')
        self.assertTrue(game is None)
        game = self.get_game_from_score(1, 'number_fdssfdtassles')
        self.assertTrue(game is None)


    @db_conn()
    def test_score_entered(self):

        # A completed game
        game = self.get_game_from_score(5, 'round_1_battle')
        compare(game.get_dao().entrants[0].entrant_id, 3)
        compare(game.get_dao().entrants[1].entrant_id, 5)
        self.assertTrue(game.is_score_entered())

        # a bye should be false
        # TODO resolve Bye Scoring
        game = self.get_game_from_score(4, 'round_1_battle')
        compare(game.get_dao().entrants[0].entrant_id, 4)
        self.assertFalse(game.is_score_entered())

        # Ensure the rd2 game bart vs. maggie is listed as not scored. This
        # will force a full check. Maggie's score hasn't been entered.
        cur.execute("UPDATE game SET score_entered = False WHERE id = 5")
        game = self.get_game_from_score(5, 'round_2_battle')

        compare(game.get_dao().entrants[0].entrant_id, 6)
        compare(game.get_dao().entrants[1].entrant_id, 5)
        self.assertFalse(game.is_score_entered())

        # Enter the final score for maggie
        cur.execute("INSERT INTO score VALUES(6, 4, 2)")
        conn.commit()

        self.assertTrue(game.is_score_entered())
        dao = game.get_dao()
        dao.score_entered = True
        dao.write()
        self.assertTrue(game.is_score_entered())

    def test_list_scores_for_game(self):
        """
        Games have a scores_entered which should return all the scores entered
        for by each entrant.
        """
        # Bye
        game = self.get_game_from_score(4, 'round_1_battle')
        compare(
            game.scores_entered(),
            [(4, 'round_1_battle', None), (4, 'sports', 5)])

        # Regular, completed game
        game = self.get_game_from_score(2, 'round_1_battle')
        compare(
            game.scores_entered(),
            [(6, 'round_1_battle', 0), (2, 'round_1_battle', 20),
             (6, 'sports', 5), (2, 'sports', 1)])

        # Game partially filled in
        game = self.get_game_from_score(5, 'round_2_battle')
        compare(
            game.scores_entered(),
            [(5, 'round_2_battle', 5)])

    @staticmethod
    def get_game_from_score(entry_id, score_key):
        """
        Given an entry and score_key, you should be able to work out the game
        """

        from sqlalchemy.sql.expression import and_
        from models.game_entry import GameEntrant
        from models.score import RoundScore, ScoreCategory, ScoreKey, Score, \
        db as score_db
        from models.tournament_entry import TournamentEntry
        from models.tournament_game import TournamentGame

        tournament_round_entry = score_db.session.\
            query(Score, ScoreKey, ScoreCategory, TournamentEntry, RoundScore).\
            join(ScoreKey).join(ScoreCategory).join(TournamentEntry).\
            join(RoundScore).filter(and_(TournamentEntry.id == entry_id,
                                         ScoreKey.key == score_key)).first()

        if tournament_round_entry is None:
            return None

        tournament_round_entry = [
            tournament_round_entry[2].tournament_id,
            tournament_round_entry[4].round_id,
            tournament_round_entry[3].id
        ]

        game = TournamentGame.query.join(GameEntrant).filter(and_(
            TournamentGame.tourn == tournament_round_entry[0],
            TournamentGame.round_num == tournament_round_entry[1],
            GameEntrant.entrant_id == tournament_round_entry[2])).first()

        return Game(game_id=game.id,
                    tournament_id=tournament_round_entry[0],
                    round_id=tournament_round_entry[1])

class EnterScore(TestCase):

    player_1 = 'enter_score_account'
    tournament_1 = 'enter_score_tournament'

    def create_app(self):
        # pass in test configuration
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_enter_score(self):
        """
        Enter a score for an entry
        """

        from models.tournament import Tournament as TournamentDAO
        t = TournamentDAO(self.tournament_1)
        t.date = '2015-07-08'
        t.num_rounds = 5
        t.write()

        from models.score import ScoreCategory, ScoreKey
        cat = ScoreCategory(self.tournament_1, 'nonsense', 50, False)
        cat.tournament = t
        cat.write()

        key = ScoreKey('some_key', cat.id, 0, 100)
        key.score_category = cat
        key.write()

        from models.tournament_round import TournamentRound
        rd = TournamentRound(self.tournament_1, 1, 'foo_mission_1')
        rd.write()

        from models.account import Account
        Account(self.player_1, 'foo@bar.com').write()

        from models.tournament_entry import TournamentEntry
        entry = TournamentEntry(self.player_1, self.tournament_1)
        entry.write()

        from tournament import Tournament
        self.assertRaises(
            TypeError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            'not_a_key',
            5)
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            key.key,
            -1)
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            key.key,
            'a')
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            key.key,
            101)
        Tournament(self.tournament_1).enter_score(entry.id, key.key, 0)
        self.assertRaises(
            ValueError,
            Tournament(self.tournament_1).enter_score,
            entry.id,
            key.key,
            100)


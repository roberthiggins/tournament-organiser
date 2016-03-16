"""
Module for storing games.

A game is simply a match between two entries. It is played on a table.
"""
# pylint: disable=no-member

from sqlalchemy.sql.expression import and_

from models.game_entry import GameEntrant
from models.score import RoundScore, ScoreCategory, ScoreKey, Score, db
from models.tournament_entry import TournamentEntry
from models.tournament_game import TournamentGame

def get_game_from_score(entry_id, score_key):
    """Given an entry and score_key, you should be able to work out the game"""

    tournament_round_entry = db.session.\
        query(Score, ScoreKey, ScoreCategory, TournamentEntry, RoundScore).\
        join(ScoreKey).join(ScoreCategory).join(TournamentEntry).\
        join(RoundScore).filter(and_(
            TournamentEntry.id == entry_id, ScoreKey.key == score_key)).first()

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
                round_id=tournament_round_entry[1],
                table_number=game.table_num,
                protected_object_id=game.protected_object_id)

class Game(object):
    """
    Representation of a single match between entrants.
    This might be a BYE
    """

    # pylint: disable=too-many-arguments
    def __init__(self, game_id=None, tournament_id=None,
                 round_id=None, table_number=None, protected_object_id=None):
        self.game_id = game_id
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.table_number = table_number
        self.protected_object_id = protected_object_id

        entrants = GameEntrant.query.filter_by(game_id=game_id).all()
        self.entry_1 = entrants[0].entrant_id
        self.entry_2 = None if len(entrants) == 1 else entrants[1].entrant_id

    def num_entrants(self):
        """The number of entrants in the game"""
        return 1 if None in [self.entry_1, self.entry_2] else 2

    def get_dao(self):
        """Gaet DAO object for self"""
        return TournamentGame.query.filter_by(id=self.game_id).first()

    def is_score_entered(self):
        """
        Checks if all scores for the game are entered and updates game row if
        True.

        When a score is entered we should check to see if all the scores for
        the game are entered. If yes we can update the game entry
        """

        if self.get_dao() is not None and self.get_dao().score_entered:
            return True

        scores_for_round = len(ScoreKey.query.join(RoundScore).\
            join(ScoreCategory).filter(
                and_(RoundScore.round_id == self.round_id,
                     ScoreCategory.tournament_id == self.tournament_id)).all())
        scores_entered = [x[2] for x in self.scores_entered()]

        return None not in scores_entered \
        and len(scores_entered) == (scores_for_round * self.num_entrants())

    def scores_entered(self):
        """
        Get a list of all scores entered for the game by all entrants.

        Returns:
            - a list of tuples (entry_id, score_key, score_entered)
        """

        scores_and_keys = db.session.query(Score, ScoreKey).join(ScoreKey).\
            join(RoundScore).join(ScoreCategory).filter(and_(
                ScoreCategory.tournament_id == self.tournament_id,
                RoundScore.round_id == self.round_id,
                Score.entry_id.in_((self.entry_1, self.entry_2)))).all()
        return [(x[0].entry_id, x[1].key, x[0].value) for x in scores_and_keys]

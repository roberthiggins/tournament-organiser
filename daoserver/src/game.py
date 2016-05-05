"""
Module for storing games.

A game is simply a match between two entries. It is played on a table.
"""
# pylint: disable=no-member

from sqlalchemy.sql.expression import and_

from models.score import RoundScore, ScoreCategory, ScoreKey, Score, db
from models.tournament_game import TournamentGame

class Game(object):
    """
    Representation of a single match between entrants.
    This might be a BYE
    """

    # pylint: disable=too-many-arguments
    def __init__(self, game_id):
        self.game_id = game_id
        self.tournament_id = self.get_dao().tournament_round.tournament_name

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
                and_(RoundScore.round_id == \
                     self.get_dao().tournament_round.ordering,
                     ScoreCategory.tournament_id == self.tournament_id)).all())
        scores_entered = [x[2] for x in self.scores_entered()]

        scores_by_entrants = scores_for_round * \
        len(self.get_dao().entrants.all())

        return None not in scores_entered \
        and len(scores_entered) == (scores_by_entrants)

    def scores_entered(self):
        """
        Get a list of all scores entered for the game by all entrants.

        Returns:
            - a list of tuples (entry_id, score_key, score_entered)
        """

        entry_ids = (x.entrant_id for x in self.get_dao().entrants)
        scores_and_keys = db.session.query(Score, ScoreKey).join(ScoreKey).\
            join(RoundScore).join(ScoreCategory).filter(and_(
                ScoreCategory.tournament_id == self.tournament_id,
                RoundScore.round_id == self.get_dao().tournament_round.ordering,
                Score.entry_id.in_(entry_ids))).all()
        return [(x[0].entry_id, x[1].key, x[0].value) for x in scores_and_keys]

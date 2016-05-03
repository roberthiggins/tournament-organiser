"""
Model of a round within a tournament

A round can be see, essentially, as a tiny, mini tournament. Therefore it makes
a nice point of separation to reduce the complexity of a tournament.
"""
from sqlalchemy.sql.expression import and_

from models.score import db as score_db, RoundScore, ScoreKey
from models.tournament_round import TournamentRound as DAO

class TournamentRound(object):
    """A round consists of a number of games and a table strategy"""

    def __init__(self, tournament_id, round_num):
        self.draw = None
        self.tournament_id = tournament_id
        self.round_num = int(round_num)

    # pylint: disable=no-member
    def get_dao(self):
        """Get the dao for this round"""
        return DAO.query.filter(
            and_(DAO.tournament_name == self.tournament_id,
                 DAO.ordering == self.round_num)).\
            first()

    def get_mission(self):
        """Return the name of the mission"""
        if self.get_dao() is not None:
            return self.get_dao().mission
        return 'TBA'

    def set_mission(self, mission_name):
        """Set the name of the mission"""
        if self.get_dao() is None:
            DAO(self.tournament_id, self.round_num, mission_name).write()
        else:
            self.get_dao().mission = mission_name
            self.get_dao().write()

    def get_score_keys(self):
        """
        Get all the score keys associated with this round
        Returns a list of tuples:
            (id, key, min, max, category_id, score_key_id, round_id)
        """

        results = score_db.session.query(ScoreKey, RoundScore).\
            join(RoundScore).filter_by(round_id=self.round_num).all()

        if len(results) == 0:
            raise ValueError("Draw not ready. Mission not set. Contact TO")

        return [
            (x[0].id, x[0].key, x[0].min_val, x[0].max_val, x[0].category,
             x[1].score_key_id, x[1].round_id) for x in results]
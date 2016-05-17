"""
Model of a round within a tournament

A round can be see, essentially, as a tiny, mini tournament. Therefore it makes
a nice point of separation to reduce the complexity of a tournament.
"""
from sqlalchemy.sql.expression import and_

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

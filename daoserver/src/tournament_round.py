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

    def get_info(self):
        """
        Returns info about round.
        Returns:
            - dict with three keys {score_keys, draw, mission}
        """
        draw_info = [
            {'table_number': t.table_number,
             'entrants': [x if isinstance(x, str) else x.player_id \
                          for x in t.entrants]
            } for t in list(self.draw)]

        return {
            'draw': draw_info,
            'mission': self.get_mission()
        }

    def get_mission(self):
        """Return the name of the mission"""
        if self.get_dao() is not None and self.get_dao().mission:
            return self.get_dao().mission
        return 'TBA'

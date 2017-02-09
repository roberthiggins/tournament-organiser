"""
Model of a Tournament Round
"""

from sqlalchemy.sql.expression import and_

from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.permissions import ProtObjAction, ProtObjPerm
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound as DAO
from models.permissions import PermissionsChecker, PERMISSIONS
from models.score import Score

class TournamentRound(object):
    """A Collection of TournamentGame that constitute a round"""
    # pylint: disable=no-member

    def __init__(self, tournament, ordering):
        self.ordering = int(ordering)
        self.tournament_name = tournament
        self.draw = None

    def db_remove(self, commit=True):
        """Remove the dao and all associated games, entrants, etc. from db"""
        for game in self.get_dao().games:
            entrants = GameEntrant.query.filter_by(game_id=game.id)
            for entrant in entrants.all():
                PermissionsChecker().remove_permission(
                    entrant.entrant.player_id,
                    PERMISSIONS['ENTER_SCORE'],
                    game.protected_object)
            entrants.delete()
            act_id = ProtObjAction.query.\
                filter_by(description=PERMISSIONS['ENTER_SCORE']).first().id
            ProtObjPerm.query.filter_by(
                protected_object_id=game.protected_object.id,
                protected_object_action_id=act_id).delete()
            db.session.delete(game)
            db.session.delete(game.protected_object)

        db.session.delete(self.get_dao())
        if commit:
            db.session.commit()

    def get_dao(self):
        """Convenience method to get the DAO"""
        return DAO.query.filter_by(tournament_name=self.tournament_name,
                                   ordering=self.ordering).first()

    def get_game_dao(self, table_num):
        """
        Get game_dao given table_num
        """
        return TournamentGame.query.join(DAO).filter(
            and_(DAO.ordering == self.ordering,
                 TournamentGame.table_num == table_num)).first()

    def get_ordering(self):
        """The round number"""
        return self.get_dao().ordering

    def is_complete(self):
        """Are all the games for this round complete"""
        for game in self.get_dao().games.all():
            if not Score.is_score_entered(game):
                return False
        return True

"""
Model of a Tournament Round
"""

from sqlalchemy.sql.expression import and_

from models.dao.db_connection import db
from models.dao.game_entry import GameEntrant
from models.dao.permissions import ProtObjAction, ProtObjPerm
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame
from models.dao.tournament_round import TournamentRound as DAO
from models.permissions import PermissionsChecker, PERMISSIONS

class DrawException(Exception):
    """For when a draw cannot be completed as scores entered already"""
    pass

class TournamentRound(object):
    """A Tournament Round"""
    # pylint: disable=no-member

    def __init__(self, tournament, ordering, matching_strategy, table_strategy):
        self.ordering = int(ordering)
        self.tournament_name = tournament
        self.matching_strategy = matching_strategy
        self.table_strategy = table_strategy
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


    def destroy_draw(self):
        """
        Removes the draw for the round.
        """
        rnd = self.get_dao()

        for game in TournamentGame.query.filter_by(tournament_round_id=rnd.id).\
        all():
            if game.score_entered and len(game.entrants.all()) > 1: # not a BYE
                raise DrawException()

            for game_entrant in game.entrants:
                PermissionsChecker().remove_permission(
                    game_entrant.entrant.player_id,
                    PERMISSIONS['ENTER_SCORE'],
                    game.protected_object)
            game.entrants.delete()

        TournamentGame.query.filter_by(tournament_round_id=rnd.id).delete()
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

    def make_draw(self, entries):
        """Determines the draw for round. This draw is written to the db"""

        rnd = self.get_dao()

        match_ups = self.matching_strategy.match(entries)
        self.draw = self.table_strategy.determine_tables(match_ups)
        for match in self.draw:

            entrants = [None if x == 'BYE' else x for x in match.entrants]

            game = TournamentGame.query.filter_by(
                tournament_round_id=rnd.id,
                table_num=match.table_number).first()
            if game is None:
                game = TournamentGame(rnd.id, match.table_number)
                db.session.add(game)
                db.session.flush()

            for entrant in entrants:
                if entrant is not None:
                    dao = TournamentEntry.query.\
                        filter_by(id=entrant.id).first()
                    game_entrant = GameEntrant.query.filter_by(
                        game_id=game.id, entrant_id=dao.id).first()
                    if game_entrant is None:
                        db.session.add(GameEntrant(game.id, dao.id))
                        PermissionsChecker().add_permission(
                            dao.player_id,
                            PERMISSIONS['ENTER_SCORE'],
                            game.protected_object)
                else:
                    # The person playing the bye gets no points at the time
                    game.score_entered = True
                    db.session.add(game)

        db.session.commit()

"""
A Tournament Draw

This is responsible for allocating players and matchups through a tournament.
"""

from models.dao.game_entry import GameEntrant
from models.dao.db_connection import db
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_game import TournamentGame

from models.matching_strategy import RoundRobin
from models.permissions import PermissionsChecker, PERMISSIONS
from models.table_strategy import ProtestAvoidanceStrategy

class DrawException(Exception):
    """For when a draw cannot be completed as scores entered already"""
    pass

# pylint: disable=no-member
class TournamentDraw(object):
    """Matches players and tables throughout the tournament"""

    def __init__(self, **args):
        # Num tables
        # Table strategy
        self.table_strategy = ProtestAvoidanceStrategy()
        # Draw Strategy
        self.matching_strategy = args.get('matching_strategy', RoundRobin())
        # Players
        self.current_round = None
        self.entries = []

    def destroy_draw(self):
        """
        Removes the draw for current_round.
        """
        rd_dao = self.current_round.get_dao()

        for game in TournamentGame.query.\
                filter_by(tournament_round_id=rd_dao.id).all():
            if game.score_entered and len(game.entrants.all()) > 1: # not a BYE
                raise DrawException()

            for game_entrant in game.entrants:
                PermissionsChecker().remove_permission(
                    game_entrant.entrant.player_id,
                    PERMISSIONS['ENTER_SCORE'],
                    game.protected_object)
            game.entrants.delete()

        TournamentGame.query.filter_by(tournament_round_id=rd_dao.id).delete()
        db.session.commit()

    def make_draws(self, tourn):
        """Makes the draws for all rounds"""
        # If we can we determine all rounds
        for rnd in range(0, tourn.get_dao().rounds.count()):
            try:
                model = tourn.get_round(rnd + 1)
                self.set_round(model)
                self.destroy_draw()
                self.set_entries(self.entries)
                model.draw = self.make_draw()
            except DrawException:
                pass

    def make_draw(self):
        """Finalise the draw, based on current round number"""
        if self.current_round is None:
            raise ValueError
        rd_dao = self.current_round.get_dao()

        match_ups = self.matching_strategy.match(self.entries)
        draw = self.table_strategy.determine_tables(match_ups)
        for match in draw:

            entrants = [None if x == 'BYE' else x for x in match.entrants]

            game = TournamentGame.query.filter_by(
                tournament_round_id=rd_dao.id,
                table_num=match.table_number).first()
            if game is None:
                game = TournamentGame(rd_dao.id, match.table_number)
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
        return draw

    def get_draw(self):
        """
        Return the draw for a given round
        """
        no_draw = AttributeError('No draw is available')
        draw = self.make_draw()
        if draw is None:
            raise no_draw

        draw_info = [
            {'table_number': t.table_number,
             'entrants': [x if isinstance(x, str) else x.player_id \
                          for x in t.entrants]
            } for t in draw]

        if not draw_info and self.current_round.get_dao().mission is None:
            raise no_draw

        return {
            'draw': draw_info,
            'mission': self.current_round.get_dao().get_mission()
        }


    def set_entries(self, entries):
        """Define players available to play. Returns self"""
        self.entries = entries
        return self

    def set_round(self, rnd):
        """Set the round number. Returns self"""
        self.current_round = rnd
        self.matching_strategy.set_round(rnd.ordering)
        return self

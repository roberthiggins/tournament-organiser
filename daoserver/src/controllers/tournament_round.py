"""
Individual rounds in a tournament
"""
from flask import Blueprint, g

from controllers.request_helpers import json_response
from models.tournament import Tournament

TOURNAMENT_ROUND = Blueprint('TOURNAMENT_ROUND', __name__)

@TOURNAMENT_ROUND.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    g.tournament = Tournament(g.tournament_id)
    if g.tournament.get_dao() is None:
        raise ValueError('Tournament {} not found in database'.\
            format(g.tournament_id))

@TOURNAMENT_ROUND.route('/<round_id>', methods=['GET'])
@json_response
def get_round_info(round_id):
    """
    GET the information about a round
    """
    no_draw = AttributeError('No draw is available')
    rnd = g.tournament.get_round(round_id)

    if rnd.draw is None:
        rnd.make_draw(g.tournament.get_entries())
        if rnd.draw is None:
            raise no_draw

    draw_info = [
        {'table_number': t.table_number,
         'entrants': [x if isinstance(x, str) else x.player_id \
                      for x in t.entrants]
        } for t in rnd.draw]

    if not draw_info and rnd.get_dao().mission is None:
        raise no_draw

    # We will return all round info for all requests regardless of method
    return {
        'draw': draw_info,
        'mission': rnd.get_dao().get_mission()
    }

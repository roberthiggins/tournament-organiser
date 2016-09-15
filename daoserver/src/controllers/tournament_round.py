"""
Individual rounds in a tournament
"""
from flask import Blueprint, g

from controllers.request_helpers import enforce_request_variables, \
json_response, text_response, ensure_permission
from models.tournament import Tournament

TOURNAMENT_ROUND = Blueprint('TOURNAMENT_ROUND', __name__)

@TOURNAMENT_ROUND.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    g.tournament = Tournament(g.tournament_id)
    if not g.tournament.exists_in_db:
        raise ValueError('Tournament {} not found in database'.\
            format(g.tournament_id))

@TOURNAMENT_ROUND.route('/<round_id>', methods=['GET'])
@json_response
def get_round_info(round_id):
    """
    GET the information about a round
    """
    no_draw = AttributeError('No draw is available')
    tourn = Tournament(g.tournament_id)
    rnd = tourn.get_round(round_id)
    try:
        draw = tourn.make_draw(round_id)
    except AttributeError:
        raise no_draw

    draw_info = [
        {'table_number': t.table_number,
         'entrants': [x if isinstance(x, str) else x.player_id \
                      for x in t.entrants]
        } for t in draw]

    if not draw_info and not rnd.mission:
        raise no_draw

    # We will return all round info for all requests regardless of method
    return {
        'draw': draw_info,
        'mission': rnd.mission
    }

@TOURNAMENT_ROUND.route('', methods=['POST'])
@text_response
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
@enforce_request_variables('numRounds')
def set_rounds():
    """Set the number of rounds for a tournament"""

    # pylint: disable=undefined-variable
    try:
        rounds = int(numRounds)
        if rounds < 1:
            raise ValueError()
    except ValueError:
        raise ValueError('Set at least 1 round')

    Tournament(g.tournament_id).set_number_of_rounds(rounds)
    return 'Rounds set: {}'.format(rounds)

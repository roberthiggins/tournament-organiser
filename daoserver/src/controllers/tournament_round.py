"""
Individual rounds in a tournament
"""
from flask import Blueprint

from controllers.request_helpers import enforce_request_variables, \
json_response, text_response
from models.tournament import Tournament

TOURNAMENT_ROUND = Blueprint('TOURNAMENT_ROUND', __name__)

@TOURNAMENT_ROUND.route('/<round_id>', methods=['GET'])
@json_response
def get_round_info(tournament_id, round_id):
    """
    GET the information about a round
    """
    tourn = Tournament(tournament_id)
    rnd = tourn.get_round(round_id)
    draw = tourn.make_draw(round_id)

    draw_info = [
        {'table_number': t.table_number,
         'entrants': [x if isinstance(x, str) else x.player_id \
                      for x in t.entrants]
        } for t in draw]

    # We will return all round info for all requests regardless of method
    return {
        'draw': draw_info,
        'mission': rnd.mission
    }

@TOURNAMENT_ROUND.route('', methods=['POST'])
@text_response
@enforce_request_variables('numRounds')
def set_rounds(tournament_id):
    """Set the number of rounds for a tournament"""

    # pylint: disable=undefined-variable
    rounds = int(numRounds)
    if rounds < 1:
        raise ValueError('Set at least 1 round')
    Tournament(tournament_id).set_number_of_rounds(rounds)
    return 'Rounds set: {}'.format(rounds)

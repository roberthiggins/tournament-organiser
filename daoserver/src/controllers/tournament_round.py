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
    g.tournament = Tournament(g.tournament_id).check_exists()

@TOURNAMENT_ROUND.route('/<round_id>', methods=['GET'])
@json_response
def get_round_info(round_id):
    """
    GET draw and mission about a round
    """
    return g.tournament.draw.set_entries(g.tournament.get_entries()).\
        set_round(g.tournament.get_round(round_id)).\
        get_draw()

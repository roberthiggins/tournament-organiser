"""
All tournament interactions.
"""
import jsonpickle

from flask import Blueprint, make_response, Response

from models.dao.tournament_entry import TournamentEntry
from models.tournament import Tournament

TOURNAMENT = Blueprint('TOURNAMENT', __name__, url_prefix='')

@TOURNAMENT.route('/<tournament_id>/entries', methods=['GET'])
def entry_list(tournament_id):
    """
    Return a list of the entrants for the tournament
    """
    # pylint: disable=no-member
    if not Tournament(tournament_id).exists_in_db:
        return make_response(
            'Tournament {} doesn\'t exist'.format(tournament_id), 404)

    entries = [ent.player_id for ent in \
        TournamentEntry.query.filter_by(tournament_id=tournament_id).all()]
    return Response(jsonpickle.encode(entries, unpicklable=False),
                    mimetype='application/json')

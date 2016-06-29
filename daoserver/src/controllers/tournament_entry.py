"""
Controller for entries in tournaments
"""
from flask import Blueprint, make_response, Response
import jsonpickle

from models.dao.tournament_entry import TournamentEntry
from models.tournament import Tournament

ENTRY = Blueprint('ENTRY', __name__)

@ENTRY.route('/', methods=['GET'])
def list_entries(tournament_id):
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

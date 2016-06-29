"""
All tournament interactions.
"""
import jsonpickle

from flask import Blueprint, make_response, Response

from models.dao.tournament import Tournament as TournamentDAO
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

@TOURNAMENT.route('/', methods=['GET'])
def list_tournaments():
    """
    GET a list of tournaments
    Returns json. The only key is 'tournaments' and the value is a list of
    tournament names
    """
    # pylint: disable=no-member
    details = [
        {'name': x.name, 'date': x.date, 'rounds': x.num_rounds}
        for x in TournamentDAO.query.all()]

    return Response(
        jsonpickle.encode({'tournaments' : details}, unpicklable=False),
        mimetype='application/json')

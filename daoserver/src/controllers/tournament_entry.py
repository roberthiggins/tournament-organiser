"""
Controller for entries in tournaments
"""
from decimal import Decimal as Dec
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

@ENTRY.route('/rank', methods=['GET'])
def rank_entries(tournament_id):
    """
    Rank all the entries in a tournament based on the scoring criteria for the
    tournament.
    The structure of the returned JSON blob will be as follows:
    [
        {
            'username': 'homer',
            'entry_id': 1,
            'tournament_id': 'some_tournie',
            'scores': {'round_1': 10, 'round_2': 4 },
            'total_score': 23.50, # always 2dp
            'ranking': 3
        },
    ]
    """
    tourn = Tournament(tournament_id)
    if not tourn.exists_in_db:
        return make_response(
            'Tournament {} doesn\'t exist'.format(tournament_id), 404)

    # pylint: disable=line-too-long
    return Response(
        jsonpickle.encode(
            [
                {
                    'username' : x.player_id,
                    'entry_id' : x.id,
                    'tournament_id' : tourn.tournament_id,
                    'scores' : x.score_info,
                    'total_score' : str(Dec(x.total_score).quantize(Dec('1.00'))),
                    'ranking': x.ranking
                } for x in \
                tourn.ranking_strategy.overall_ranking(tourn.entries())
            ],
            unpicklable=False),
        mimetype='application/json')

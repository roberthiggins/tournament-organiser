"""
Controller for entries in tournaments
"""
from decimal import Decimal as Dec
from flask import Blueprint, make_response, Response, g
import jsonpickle

from models.dao.account import Account
from models.dao.tournament_entry import TournamentEntry
from models.tournament import Tournament

ENTRY = Blueprint('ENTRY', __name__)

@ENTRY.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 400)

@ENTRY.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    g.tournament = Tournament(g.tournament_id)
    if not g.tournament.exists_in_db:
        raise ValueError('Tournament {} doesn\'t exist'.format(g.tournament_id))

@ENTRY.route('/', methods=['GET'])
def list_entries():
    """
    Return a list of the entrants for the tournament
    """
    # pylint: disable=no-member
    entries = [ent.player_id for ent in \
        TournamentEntry.query.filter_by(tournament_id=g.tournament_id).all()]
    return Response(jsonpickle.encode(entries, unpicklable=False),
                    mimetype='application/json')

def get_entry_id(tournament_id, username):
    """Get entry info from tournament and username"""
    if not Account.username_exists(username):
        raise ValueError('Unknown player: {}'.format(username))

    try:
        # pylint: disable=no-member
        return TournamentEntry.query.\
            filter_by(tournament_id=tournament_id, player_id=username).\
            first().id
    except AttributeError:
        raise ValueError('Entry for {} in tournament {} not found'.\
            format(username, tournament_id))

@ENTRY.route('/<username>', methods=['GET'])
def entry_info_from_tournament(username):
    """ Given entry_id, get info about player and tournament"""
    entry_id = get_entry_id(g.tournament_id, username)

    try:
        # pylint: disable=no-member
        entry = TournamentEntry.query.filter_by(id=entry_id).first()

        return Response(
            jsonpickle.encode(
                {
                    'entry_id': entry.id,
                    'username': entry.account.username,
                    'tournament_name': entry.tournament.name,
                }, unpicklable=False),
            mimetype='application/json')
    except AttributeError:
        raise ValueError('Entry ID not valid: {}'.format(entry_id))

@ENTRY.route('/rank', methods=['GET'])
def rank_entries():
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

    # pylint: disable=line-too-long
    return Response(
        jsonpickle.encode(
            [
                {
                    'username' : x.player_id,
                    'entry_id' : x.id,
                    'tournament_id' : g.tournament_id,
                    'scores' : x.score_info,
                    'total_score' : str(Dec(x.total_score).quantize(Dec('1.00'))),
                    'ranking': x.ranking
                } for x in \
                g.tournament.ranking_strategy.overall_ranking(
                    g.tournament.entries())
            ],
            unpicklable=False),
        mimetype='application/json')

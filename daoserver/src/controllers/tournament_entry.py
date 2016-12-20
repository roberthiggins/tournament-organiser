"""
Controller for entries in tournaments
"""
from decimal import Decimal as Dec
from flask import Blueprint, g, request

from controllers.request_helpers import json_response, requires_auth, \
text_response, ensure_permission
from models.dao.tournament_entry import TournamentEntry as TournamentEntryDAO
from models.tournament import Tournament
from models.tournament_entry import TournamentEntry
from models.user import User

ENTRY = Blueprint('ENTRY', __name__)

@ENTRY.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    g.username = values.pop('username', None)
    if g.username:
        g.entry = TournamentEntry(g.tournament_id, g.username)

@ENTRY.route('/', methods=['GET'])
@json_response
def list_entries():
    """
    Return a list of the entrants for the tournament
    """
    Tournament(g.tournament_id).check_exists()
    # pylint: disable=no-member
    return [User(ent.player_id).get_display_name() for ent in \
        TournamentEntryDAO.query.filter_by(tournament_id=g.tournament_id).all()]

@ENTRY.route('/<username>/score', methods=['POST'])
@requires_auth
@text_response
@ensure_permission({'permission': 'ENTER_SCORE'})
def enter_scores():
    """Enter scores for a player in a game."""
    return g.entry.set_scores(request.get_json().get('scores'))

@ENTRY.route('/<username>', methods=['GET'])
@requires_auth
@json_response
def read():
    """ Given entry_id, get info about player and tournament"""
    return g.entry.read()

@ENTRY.route('/<username>/nextgame', methods=['GET'])
@json_response
def next_game():
    """Get the next game for given entry"""
    return g.entry.get_next_game()

@ENTRY.route('/<username>/schedule', methods=['GET'])
@json_response
def schedule():
    """Get the scheule of games for username's entry"""
    return g.entry.get_schedule()

@ENTRY.route('/rank', methods=['GET'])
@json_response
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
    tournament = Tournament(g.tournament_id)
    # pylint: disable=line-too-long
    return [
        {
            'username' : x.player_id,
            'entry_id' : x.id,
            'tournament_id' : g.tournament_id,
            'scores' : x.score_info,
            'total_score' : str(Dec(x.total_score).quantize(Dec('1.00'))),
            'ranking': x.ranking
        } for x in tournament.ranking_strategy.overall_ranking(
            tournament.get_entries())
    ]

@ENTRY.route('/<username>/withdraw', methods=['POST'])
@requires_auth
@text_response
@ensure_permission({'permission': 'MODIFY_APPLICATION'})
def withdraw_entry():
    """
    POST to withdraw entry from the tournament
    """
    g.entry.delete()
    return 'Entry to {} withdrawn successfully'.format(g.tournament_id)

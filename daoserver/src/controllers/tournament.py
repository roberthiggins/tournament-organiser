"""
All tournament interactions.
"""
from decimal import Decimal as Dec
from flask import Blueprint, g, request

from controllers.request_helpers import enforce_request_variables, \
json_response, requires_auth, text_response, ensure_permission
from models.dao.registration import TournamentRegistration
from models.dao.tournament import Tournament as TournamentDAO
from models.tournament import Tournament

TOURNAMENT = Blueprint('TOURNAMENT', __name__)

@TOURNAMENT.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    if g.tournament_id:
        g.tournament = Tournament(g.tournament_id)

    g.username = values.pop('username', None)

@TOURNAMENT.route('', methods=['POST'])
@requires_auth
@json_response
@enforce_request_variables('inputTournamentName', 'inputTournamentDate')
def add_tournament():
    # pylint: disable=undefined-variable

    """
    POST to add a tournament
    Expects:
        - inputTournamentName - Tournament name. Must be unique.
        - inputTournamentDate - Tournament Date. YYYY-MM-DD
    """
    opt_args = request.get_json() if request.get_json() is not None else {}
    tourn = Tournament(inputTournamentName)
    tourn.new(date=inputTournamentDate,
              to_username=request.authorization.username,
              **opt_args)
    return tourn.details()

@TOURNAMENT.route('/<tournament_id>/start', methods=['POST'])
@requires_auth
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
@text_response
def start_tournament():
    """Set the tournament to in-progress manually"""
    g.tournament.set_in_progress()
    return 'Tournament {} now in progress'.format(g.tournament_id)

@TOURNAMENT.route('/<tournament_id>/missions', methods=['GET'])
@json_response
def list_missions():
    """GET list of missions for a tournament."""
    return g.tournament.get_missions()

@TOURNAMENT.route('/<tournament_id>/score_categories', methods=['GET'])
@json_response
def list_score_categories():
    """
    GET the score categories set for the tournament.
    e.g. [{ 'name': 'painting', 'percentage': 20, 'id': 2 }]
    """
    return g.tournament.get_score_categories(serialized=True)

@TOURNAMENT.route('/', methods=['GET'])
@json_response
def list_tournaments():
    """
    GET a list of tournaments
    Returns json. The only key is 'tournaments' and the value is a list of
    dicts - {name: '', date, 'YY-MM-DD', rounds: 1}
    """
    user = getattr(request.authorization, 'username', None)
    # pylint: disable=no-member
    details = [{
        'name': x.name,
        'date': x.date,
        'rounds': x.rounds.count(),
        'entries': x.entries.count(),
        'user_entered': x.entries.filter_by(player_id=user).count() == 1
    } for x in TournamentDAO.query.all()]

    return {'tournaments' : sorted(details, key=lambda to: to['name'])}

@TOURNAMENT.route('/<tournament_id>/rankings', methods=['GET'])
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

    return [
        {
            'username' : x.player_id,
            'entry_id' : x.id,
            'tournament_id' : g.tournament_id,
            'scores' : x.score_info,
            'total_score' : str(Dec(x.total_score).quantize(Dec('1.00'))),
            'ranking': x.ranking
        } for x in g.tournament.ranking_strategy.overall_ranking(
            g.tournament.get_entries())
    ]

@TOURNAMENT.route('/<tournament_id>/register/<username>', methods=['POST'])
@requires_auth
@ensure_permission({'permission': 'MODIFY_APPLICATION'})
@text_response
def register():
    """
    POST to apply for entry to a tournament.
    """
    exists = g.tournament.details() # pylint: disable=unused-variable
    rego = TournamentRegistration(g.username, g.tournament_id)
    rego.add_to_db()
    g.tournament.confirm_entries()
    g.tournament.get_draw().make_draws(g.tournament)

    return 'Application Submitted'


@TOURNAMENT.route('/<tournament_id>', methods=['GET'])
@json_response
def tournament_details():
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    user = getattr(request.authorization, 'username', None)
    details = g.tournament.details()
    if g.tournament.get_dao().entries.filter_by(player_id=user).count() == 1:
        details['user'] = user
    return details

@TOURNAMENT.route('/<tournament_id>', methods=['POST'])
@text_response
@requires_auth
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
def update():
    """POST to update Tournament"""
    g.tournament.update(request.get_json())
    return 'Tournament {} updated'.format(g.tournament_id)

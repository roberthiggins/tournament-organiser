"""
All tournament interactions.
"""
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
    g.tournament.make_draws()

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
    details['user_entered'] = g.tournament.get_dao().entries.\
        filter_by(player_id=user).count() == 1
    return details

@TOURNAMENT.route('/<tournament_id>', methods=['POST'])
@text_response
@requires_auth
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
def update():
    """POST to update Tournament"""
    g.tournament.update(request.get_json())
    return 'Tournament {} updated'.format(g.tournament_id)

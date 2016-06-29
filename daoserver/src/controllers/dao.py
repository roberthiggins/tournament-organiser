"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

from decimal import Decimal as Dec
import json
from functools import wraps
import jsonpickle

from flask import Blueprint, request, make_response, Response

from controllers.request_variables import enforce_request_variables
from models.dao.account import Account
from models.dao.tournament_entry import TournamentEntry
from models.permissions import PERMISSIONS, PermissionsChecker
from models.tournament import Tournament, ScoreCategoryPair

APP = Blueprint('APP', __name__, url_prefix='')

@APP.errorhandler(IndexError)
@APP.errorhandler(TypeError)
@APP.errorhandler(RuntimeError)
@APP.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 400)

@APP.errorhandler(Exception)
def unknown_error(err):
    """All other exceptions are essentially just raised with logging"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 500)

# pylint: disable=E0602
def requires_permission(action, error_msg):
    """
    A decorator that requires a permission check for the function.
    Assumptions:
        - the function scope includes the variables 'username' and 'tournament'
    """
    def decorator(func):                # pylint: disable=missing-docstring
        @wraps(func)
        def wrapped(*args, **kwargs):   # pylint: disable=missing-docstring

            checker = PermissionsChecker()
            if request.authorization is None or not checker.check_permission(
                    action,
                    request.authorization.username,
                    username,
                    tournament):
                # TODO get tournament from the request
                raise ValueError('Permission denied. {}'.format(error_msg))

            return func(*args, **kwargs)
        return wrapped
    return decorator

@APP.route("/")
def main():
    """Index page. Used to verify the server is running."""
    return make_response('daoserver', 200)

# Page actions
@APP.route('/entertournamentscore', methods=['POST'])
@enforce_request_variables('username', 'tournament', 'key', 'value')
@requires_permission(
    PERMISSIONS.get('ENTER_SCORE'),
    'You cannot enter scores for this game. Contact the TO.')
def enter_tournament_score():
    """
    POST to enter a score for a player in a tournament.

    Expects:
        - username - the player_id
        - tournament - the tournament_id
        - key - the category e.g. painting, round_6_battle
        - value - the score. Integer
    """
    # pylint: disable=E0602
    tourn = Tournament(tournament)
    if not tourn.exists_in_db:
        raise ValueError('Unknown tournament: {}'.format(tournament))

    if not Account.username_exists(username):
        raise ValueError('Unknown player: {}'.format(username))

    # pylint: disable=E0602,no-member
    entry_id = TournamentEntry.query.\
            filter_by(tournament_id=tournament, player_id=username).first().id

    # pylint: disable=E0602
    tourn.enter_score(entry_id, key, value)
    return make_response(
        'Score entered for {}: {}'.format(username, value),
        200)

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

@APP.route('/entryId/<tournament_id>/<username>', methods=['GET'])
def get_entry_id_from_tournament(tournament_id, username):
    """Get entry info from tournament and username"""
    return jsonpickle.encode(get_entry_id(tournament_id, username),
                             unpicklable=False)

@APP.route('/entryInfo/<entry_id>', methods=['GET'])
def entry_info_from_id(entry_id):
    """ Given entry_id, get info about player and tournament"""

    try:
        entry_id = int(entry_id)
    except ValueError:
        raise ValueError('Entry ID must be an integer')

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

@APP.route('/entryInfo/<tournament_id>/<username>', methods=['GET'])
def entry_info_from_tournament(tournament_id, username):
    """ Given entry_id, get info about player and tournament"""
    return entry_info_from_id(get_entry_id(tournament_id, username))

@APP.route('/rankEntries/<tournament_id>', methods=['GET'])
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

@APP.route('/roundInfo/<tournament_id>/<round_id>', methods=['GET'])
# pylint: disable=E0602
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
    return jsonpickle.encode(
        {
            'draw': draw_info,
            'mission': rnd.mission
        },
        unpicklable=False)

@APP.route('/setRounds', methods=['POST'])
@enforce_request_variables('numRounds', 'tournamentId')
def set_rounds():
    """Set the number of rounds for a tournament"""
    # pylint: disable=E0602
    rounds = int(numRounds)
    if rounds < 1:
        raise ValueError('Set at least 1 round')
    # pylint: disable=E0602
    Tournament(tournamentId).set_number_of_rounds(rounds)
    return make_response('Rounds set: {}'.format(rounds), 200)

@APP.route('/getScoreCategories/<tournament_id>', methods=['GET'])
def get_score_categories(tournament_id):
    """
    GET the score categories set for the tournament.
    e.g. [{ 'name': 'painting', 'percentage': 20, 'id': 2 }]
    """
    try:
        tourn = Tournament(tournament_id)
        return Response(
            jsonpickle.encode(tourn.list_score_categories(), unpicklable=False),
            mimetype='application/json')
    except ValueError as err:
        return make_response(str(err), 404)

@APP.route('/setScoreCategories', methods=['POST'])
@enforce_request_variables('tournamentId', 'categories')
def set_score_categories():
    """
    POST to set tournament categories en masse
    """
    tourn = Tournament(tournamentId)

    new_categories = []
    try:
        cats = json.loads(categories)
    except TypeError:
        cats = categories

    for json_cat in cats:
        try:
            cat = json.loads(request.values.get(json_cat, []))
        except TypeError:
            cat = request.get_json().get(json_cat)

        new_categories.append(
            ScoreCategoryPair(cat[0], cat[1], cat[2], cat[3], cat[4]))

    tourn.set_score_categories(new_categories)

    return make_response('Score categories set: {}'.format(
        ', '.join([str(cat.display_name) for cat in new_categories])), 200)

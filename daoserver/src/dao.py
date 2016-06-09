"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

from decimal import Decimal as Dec
import json
import re
from functools import wraps
import jsonpickle

from flask import Blueprint, request, make_response, Response

from sqlalchemy.exc import IntegrityError

from authentication import check_auth
from models.account import Account, add_account
from models.db_connection import db
from models.feedback import Feedback
from models.registration import TournamentRegistration
from models.tournament import Tournament as TournamentDAO
from models.tournament_entry import TournamentEntry
from permissions import PERMISSIONS, PermissionsChecker
from tournament import Tournament, ScoreCategoryPair

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

def enforce_request_variables(*vars_to_enforce):
    """ A decorator that requires var exists in the request"""
    def decorator(func):                # pylint: disable=missing-docstring
        @wraps(func)
        def wrapped(*args, **kwargs):   # pylint: disable=missing-docstring

            if request.method == 'GET':
                return func(*args, **kwargs)

            glob = func.func_globals
            sentinel = object()
            old_values = {}

            for var in vars_to_enforce:
                value = request.form[var] if var in request.form \
                    else request.values.get(var, None)

                if value is None and request.get_json() is not None:
                    value = request.get_json().get(var, None)

                if value is None:
                    return make_response('Enter the required fields', 400)

                old_values[var] = glob.get(var, sentinel)
                glob[var] = value

            try:
                res = func(*args, **kwargs)
            finally:
                for var in vars_to_enforce:
                    if old_values[var] is sentinel:
                        del glob[var]
                    else:
                        glob[var] = old_values[var]

            return res
        return wrapped
    return decorator

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
@APP.route('/listTournaments', methods=['GET'])
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

@APP.route('/registerfortournament', methods=['POST'])
@enforce_request_variables('inputTournamentName', 'inputUserName')
def apply_for_tournament():
    """
    POST to apply for entry to a tournament.
    Expects:
        - inputUserName - Username of player applying
        - inputTournamentName - Tournament as returned by GET /listTournaments
    """
    rego = TournamentRegistration(inputUserName, inputTournamentName)
    rego.clashes()

    try:
        db.session.add(rego)
        db.session.commit()
    except IntegrityError:
        raise ValueError("Check username and tournament")

    return make_response('Application Submitted', 200)

@APP.route('/addTournament', methods=['POST'])
@enforce_request_variables('inputTournamentName', 'inputTournamentDate')
def add_tournament():
    """
    POST to add a tournament
    Expects:
        - inputTournamentName - Tournament name. Must be unique.
        - inputTournamentDate - Tournament Date. YYYY-MM-DD
    """
    # pylint: disable=E0602
    tourn = Tournament(
        inputTournamentName,
        creator=request.authorization.username)
    # pylint: disable=E0602
    tourn.add_to_db(inputTournamentDate)
    # pylint: disable=E0602
    return make_response(
        '<p>Tournament Created! You submitted the following fields:</p> \
        <ul><li>Name: {}</li><li>Date: {}</li></ul>'.format(
            inputTournamentName, inputTournamentDate), 200)

def validate_user_email(email):
    """
    Validates email based on django validator
    """
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

@APP.route('/addPlayer', methods=['POST'])
@enforce_request_variables('username', 'email', 'password1', 'password2')
def create_account():
    """
    POST to add an account
    Expects:
        - username
        - email
        - password1
        - password2
    """
    # pylint: disable=E0602
    if not validate_user_email(email):
        return make_response("This email does not appear valid", 400)

    # pylint: disable=E0602
    if password1 != password2:
        return make_response("Please enter two matching passwords", 400)

    if Account.username_exists(username):
        return make_response("A user with the username {} already exists! \
            Please choose another name".format(username), 400)

    add_account(username, email, password1)

    return make_response('<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(username, email), 200)

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

    # pylint: disable=no-member
    return TournamentEntry.query.\
        filter_by(tournament_id=tournament_id, player_id=username).first().id


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

@APP.route('/login', methods=['POST'])
@enforce_request_variables('inputUsername', 'inputPassword')
def login():
    """
    POST to login
    Expects:
        - inputUsername
        - inputPassword
    """
    # pylint: disable=E0602
    return make_response(
        "Login successful" if check_auth(inputUsername, inputPassword) \
        else "Login unsuccessful",
        200)

@APP.route('/getMissions/<tournament_id>', methods=['GET'])
def get_missions(tournament_id):
    """GET list of missions for a tournament."""
    return jsonpickle.encode(
        [x.mission for x in Tournament(tournament_id).get_dao().rounds],
        unpicklable=False)

@APP.route('/setMissions', methods=['POST'])
@enforce_request_variables('tournamentId', 'missions')
def set_missions():
    """POST to set the missions for a tournament.A list of strings expected"""
    # pylint: disable=E0602
    tourn = Tournament(tournamentId)
    # pylint: disable=E0602
    rounds = tourn.details()['rounds']
    try:
        json_missions = json.loads(missions)
    except TypeError:
        json_missions = missions

    if len(json_missions) != int(rounds):
        # pylint: disable=E0602
        raise ValueError('Tournament {} has {} rounds. \
            You submitted missions {}'.format(tournamentId, rounds, missions))

    from models.tournament_round import TournamentRound as TR
    for i, mission in enumerate(json_missions):
        rnd = tourn.get_round(i + 1)
        # pylint: disable=no-member
        rnd.mission = mission if mission else TR.__table__.c.mission.default.arg
        db.session.add(rnd)

    db.session.commit()
    return make_response('Missions set: {}'.format(missions), 200)

@APP.route('/placefeedback', methods=['POST'])
def place_feedback():
    """
    POST to add feedback or submit suggestion.
    Expects:
        - inputFeedback - A string
    """
    _feedback = request.form['inputFeedback'].strip('\n\r\t+')
    if re.match(r'^[\+\s]*$', _feedback) is not None:
        return make_response("Please fill in the required fields", 400)
    try:
        db.session.add(Feedback(_feedback))
        db.session.commit()
    except IntegrityError:
        pass

    return make_response("Thanks for you help improving the site", 200)

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
    POST Expects:
        {
            'mission': a text name,
        }
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

@APP.route('/tournamentDetails/<t_name>', methods=['GET'])
def tournament_details(t_name=None):
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    tourn = Tournament(t_name)
    return Response(
        jsonpickle.encode(tourn.details(), unpicklable=False),
        mimetype='application/json')

@APP.route('/userDetails/<u_name>', methods=['GET'])
def user_details(u_name=None):
    """
    GET to get account details in url form
    TODO security
    """
    # pylint: disable=no-member
    user = Account.query.filter_by(username=u_name).first()
    if user is None:
        raise ValueError('Cannot find user {}'.format(u_name))

    return Response(
        jsonpickle.encode({u_name: user.contact_email}, unpicklable=False),
        mimetype='application/json')

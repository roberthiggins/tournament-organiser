"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

import datetime
import json
import jsonpickle
import os
import re

from flask import Flask, request, make_response, jsonify
from functools import wraps

from entry_db import EntryDBConnection
from feedback_db import FeedbackDBConnection
from player_db import PlayerDBConnection
from tournament import Tournament
from registration_db import RegistrationDBConnection

APP = Flask(__name__)
ENTRY_DB_CONN = EntryDBConnection()
FEEDBACK_DB_CONN = FeedbackDBConnection()
PLAYER_DB_CONN = PlayerDBConnection()
REGISTRATION_DB_CONN = RegistrationDBConnection()

@APP.errorhandler(RuntimeError)
@APP.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
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
    def decorator(func):                                # pylint: disable=C0111
        @wraps(func)
        def wrapped(*args, **kwargs):                   # pylint: disable=C0111

            if request.method == 'GET':
                return func(*args, **kwargs)

            glob = func.func_globals
            sentinel = object()
            old_values = {}

            for var in vars_to_enforce:
                value = request.form[var] if var in request.form \
                    else request.values.get(var, None)
                if not value:
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

@APP.route("/")
def main():
    """Index page. Used to verify the server is running."""
    return make_response('daoserver', 200)

# Page actions
@APP.route('/listtournaments', methods=['GET'])
def list_tournaments():
    """
    GET a list of tournaments
    Returns json. The only key is 'tournaments' and the value is a list of
    tournament names
    """
    return jsonpickle.encode(Tournament.list_tournaments(), unpicklable=False)

@APP.route('/registerfortournament', methods=['POST'])
@enforce_request_variables('inputTournamentName', 'inputUserName')
def apply_for_tournament():
    """
    POST to apply for entry to a tournament.
    Expects:
        - inputUserName - Username of player applying
        - inputTournamentName - Tournament as returned by GET /listtournaments
    """
    # pylint: disable=E0602
    return make_response(
        REGISTRATION_DB_CONN.register_for_tournament(
            inputTournamentName,
            inputUserName),
        200)

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
    tourn = Tournament(inputTournamentName)
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
def add_account():
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

    if PLAYER_DB_CONN.username_exists(username):
        return make_response("A user with the username {} already exists! \
            Please choose another name".format(username), 400)

    PLAYER_DB_CONN.add_account({'user_name': username,
                                'email' : email,
                                'password': password1})
    return make_response('<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {}</li><li>Email: {}\
        </li></ul>'.format(username, email), 200)

@APP.route('/entertournamentscore', methods=['POST'])
@enforce_request_variables('username', 'tournament', 'key', 'value')
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
    entry = ENTRY_DB_CONN.entry_id(tournament, username)

    # pylint: disable=E0602
    ENTRY_DB_CONN.enter_score(entry, key, value)
    return make_response(
        'Score entered for {}: {}'.format(username, value),
        200)

@APP.route('/entryId/<tournament_id>/<username>', methods=['GET'])
def get_entry_id(tournament_id, username):
    """Get entry info from tournament and username"""
    return jsonpickle.encode(
        ENTRY_DB_CONN.entry_id(tournament_id, username), unpicklable=False)

@APP.route('/entryInfo/<entry_id>', methods=['GET'])
def entry_info(entry_id):
    """ Given entry_id, get info about player and tournament"""
    return jsonpickle.encode(
        ENTRY_DB_CONN.entry_info(entry_id), unpicklable=False)

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
        PLAYER_DB_CONN.login(inputUsername, inputPassword),
        200)

@APP.route('/getMissions/<tournament_id>', methods=['GET'])
def get_missions(tournament_id):
    """GET list of missions for a tournament."""
    return jsonpickle.encode(
        Tournament(tournament_id).get_missions(), unpicklable=False)

@APP.route('/setMissions', methods=['POST'])
@enforce_request_variables('tournamentId', 'missions')
def set_missions():
    """POST to set the missions for a tournament.A list of strings expected"""
    # pylint: disable=E0602
    tourn = Tournament(tournamentId)
    # pylint: disable=E0602
    rounds = tourn.details()['details']['rounds']
    json_missions = json.loads(missions)

    if len(json_missions) != int(rounds):
        # pylint: disable=E0602
        raise ValueError('Tournament {} has {} rounds. \
            You submitted missions {}'.format(tournamentId, rounds, missions))

    for i, mission in enumerate(json_missions):
        tourn.set_mission(i + 1, mission)

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
    FEEDBACK_DB_CONN.submit_feedback(_feedback)
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
            'scores': {'round_1': 10, 'round_2': 4 }
        },
    ]
    """
    tourn = Tournament(tournament_id)
    if not tourn.exists_in_db:
        return make_response(
            'Tournament {} doesn\'t exist'.format(tournament_id), 404)
    return jsonpickle.encode(
        tourn.ranking_strategy.overall_ranking(), unpicklable=False)

@APP.route('/roundInfo/<tournament_id>/<round_id>', methods=['GET', 'POST'])
@enforce_request_variables('score_keys', 'mission')
# pylint: disable=E0602
def get_round_info(tournament_id, round_id):
    """
    GET the information about a round
    POST information including the mission, score_keys to be used.
    POST Expects:
        {
            'mission': a text name,
        }
    """
    tourn = Tournament(tournament_id)

    if request.method == 'POST':
        tourn.set_mission(round_id, mission)

    # We will return all round info for all requests regardless of method
    return jsonpickle.encode({
        'score_keys': tourn.get_score_keys_for_round(round_id),
        'draw': tourn.table_strategy.determine_tables(
            tourn.draw_strategy.draw(int(round_id))),
        'mission': tourn.get_mission(int(round_id))
    }, unpicklable=False)

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
        return jsonpickle.encode(
            tourn.list_score_categories(), unpicklable=False)
    except ValueError as err:
        return make_response(str(err), 404)

@APP.route('/setScoreCategory', methods=['POST'])
@enforce_request_variables('tournament', 'category', 'percentage')
def set_score_category():                               # pylint: disable=E0602
    """
    POST to create a score category.
    Expects:
        - tournament - the tournament name
        - category - a human-readable key for the category
        - percentage - the percentage of the overall score that will be
                        comprised from this score.
    """
    # pylint: disable=E0602
    tourn = Tournament(tournament)
    # pylint: disable=E0602
    tourn.create_score_category(category, percentage)
    return make_response('Score category set: {}'.format(category), 200)

@APP.route('/setTournamentScore', methods=['POST'])
@enforce_request_variables('key', 'scoreCategory')
def set_tournament_score():                             # pylint: disable=E0602
    """
    POST to set a score category that a player is eligible for in a tournament.
    """
    tourn = Tournament(request.values.get('tournamentId', None))
    # pylint: disable=E0602
    tourn.set_score(
        key=key,
        min_val=request.values.get('minVal'),
        max_val=request.values.get('maxVal'),
        category=scoreCategory)
    return make_response('Score created', 200)

@APP.route('/tournamentDetails/<t_name>', methods=['GET'])
def tournament_details(t_name=None):
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    tourn = Tournament(t_name)
    return jsonpickle.encode(tourn.details(), unpicklable=False)

@APP.route('/userDetails/<u_name>', methods=['GET'])
def user_details(u_name=None):
    """
    GET to get account details in url form
    TODO security
    """
    return jsonify({u_name: PLAYER_DB_CONN.user_details(u_name)})

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)

    # pylint: disable=W0232
    class DatetimeHandler(jsonpickle.handlers.BaseHandler):
        """Custom handler to get datetimes as ISO dates"""
        def flatten(self, obj, data):   # pylint: disable=C0111,W0613,R0201
            return obj.isoformat()

    jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)
    jsonpickle.handlers.registry.register(datetime.date, DatetimeHandler)

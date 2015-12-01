"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

import os
import re

from flask import Flask, request, make_response, json, jsonify

from datetime_encoder import DateTimeJSONEncoder
from entry_db import EntryDBConnection
from feedback_db import FeedbackDBConnection
from player_db import PlayerDBConnection
from tournament import Tournament
from tournament_db import TournamentDBConnection
from registration_db import RegistrationDBConnection

APP = Flask(__name__)
ENTRY_DB_CONN = EntryDBConnection()
FEEDBACK_DB_CONN = FeedbackDBConnection()
PLAYER_DB_CONN = PlayerDBConnection()
TOURNAMENT_DB_CONN = TournamentDBConnection()
REGISTRATION_DB_CONN = RegistrationDBConnection()

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
    return DateTimeJSONEncoder().encode(
        {'tournaments' : TOURNAMENT_DB_CONN.list_tournaments()})

@APP.route('/registerfortournament', methods=['POST'])
def apply_for_tournament():
    """
    POST to apply for entry to a tournament.
    Expects:
        - inputUserName - Username of player applying
        - inputTournamentName - Tournament as returned by GET /listtournaments
    """
    username = request.form['inputUserName']
    tournament_name = request.form['inputTournamentName']

    if not username or not tournament_name:
        return make_response("Enter the required fields", 400)

    try:
        return make_response(
            REGISTRATION_DB_CONN.register_for_tournament(
                tournament_name,
                username),
            200)
    except RuntimeError as err:
        return make_response(str(err), 400)

@APP.route('/addTournament', methods=['POST'])
def add_tournament():
    """
    POST to add a tournament
    Expects:
        - inputTournamentName - Tournament name. Must be unique.
        - inputTournamentDate - Tournament Date. YYYY-MM-DD
    """
    name = request.form['inputTournamentName']
    date = request.form['inputTournamentDate']

    if not name or not date:
        return make_response("Please fill in the required fields", 400)

    try:
        tourn = Tournament(name)
        tourn.add_to_db(date)
        return make_response('<p>Tournament Created! You submitted the \
            following fields:</p><ul><li>Name: {name}</li><li>Date: {date} \
            </li></ul>'.format(**locals()), 200)
    except ValueError:
        return make_response(str(err), 400)
    except RuntimeError as err:
        return make_response(str(err), 400)

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
def add_account():
    """
    POST to add an account
    Expects:
        - username
        - email
        - password1
        - password2
    """
    username = request.form['username'].strip()
    email = request.form['email'].strip()
    password = request.form['password1'].strip()
    confirm = request.form['password2'].strip()

    if not username:
        return make_response("Please fill in the required fields", 400)

    if not validate_user_email(email):
        return make_response("This email does not appear valid", 400)

    if not password or not confirm or password != confirm:
        return make_response("Please enter two matching passwords", 400)

    if PLAYER_DB_CONN.username_exists(username):
        return make_response("A user with the username %s already exists! \
            Please choose another name" % username, 400)

    PLAYER_DB_CONN.add_account({'user_name': username,
                               'email' : email,
                               'password': password})
    return make_response('<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {username}</li><li>Email: {email}\
        </li></ul>'.format(**locals()), 200)

@APP.route('/entergamescore', methods=['POST'])
def enter_game_score():
    """
    POST to enter the scores for a single game.

    Expects:
        - json blob named 'gamescore' e.g. gamescore={blah}.It should include:
            {
            'scores': { 'username':{}, 'username': {} },
            'tournament_name': 'some_tournament_id',
            'round': '1'
            }
    """
    if not request.args.get('gamescore'):
        return make_response('Enter the required fields', 400)

    data = json.loads(request.args.get('gamescore'))

    if not data \
    or not 'tournament_name' in data \
    or not 'round' in data \
    or not 'scores' in data:
        return make_response('Enter the required fields', 400)

    unknown_players = [x for x in data['scores'].keys() \
                        if not PLAYER_DB_CONN.username_exists(x)]
    if len(unknown_players) > 0:
        return make_response('Unknown player: ' + unknown_players[0], 400)

    try:
        return make_response(
            TOURNAMENT_DB_CONN.enter_game_score(
                data['tournament_name'],
                data['round'],
                data['scores']),
            200)
    except RuntimeError as err:
        return make_response(str(err), 400)

@APP.route('/entertournamentscore', methods=['POST'])
def enter_tournament_score():
    """
    POST to enter a score for a player in a tournament.

    Expects:
        - username - the player_id
        - tournament - the tournament_id
        - key - the category e.g. painting, round_6_battle
        - value - the score. Integer
    """

    user = request.values.get('username', None)
    tournament = request.values.get('tournament', None)
    category = request.values.get('key', None)
    score = request.values.get('value', None)

    if not user or not tournament or not category or not score:
        return make_response('Enter the required fields', 400)

    try:
        entry = ENTRY_DB_CONN.entry_id(tournament, user)

        ENTRY_DB_CONN.enter_score(tournament, entry, category, score)
        return make_response(
            'Score entered for {}: {}'.format(user, score),
            200)
    except ValueError as err:
        return make_response(str(err), 400)
    except RuntimeError as err:
        return make_response(str(err), 400)

@APP.route('/entryId/<tournament_id>/<username>', methods=['GET'])
def entry_id(tournament_id, username):
    """Get entry info from tournament and username"""
    return DateTimeJSONEncoder().encode(
        ENTRY_DB_CONN.entry_id(tournament_id, username))

@APP.route('/entryInfo/<entry_id>', methods=['GET'])
def entry_info(entry_id):
    """ Given entry_id, get info about player and tournament"""
    try:
        return DateTimeJSONEncoder().encode(ENTRY_DB_CONN.entry_info(entry_id))
    except ValueError as err:
        return make_response(str(err), 400)
    except RuntimeError as err:
        return make_response(str(err), 400)

@APP.route('/login', methods=['POST'])
def login():
    """
    POST to login
    Expects:
        - inputUsername
        - inputPassword
    """
    username = request.form['inputUsername'].strip()
    password = request.form['inputPassword'].strip()

    try:
        return make_response(PLAYER_DB_CONN.login(username, password), 200)
    except RuntimeError as err:
        return make_response(str(err), 400)
    except Exception as err:
        print err
        return make_response(str(err), 500)


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

@APP.route('/setTournamentScore', methods=['POST'])
def set_tournament_score():
    """
    POST to set a score category that a player is eligible for in a tournament.
    """
    try:
        tourn = Tournament(request.values.get('tournamentId', None))
        tourn.set_score(
            request.values.get('key', None),
            request.values.get('minVal'),
            request.values.get('maxVal'))
        return make_response('Score created', 200)
    except ValueError as err:
        print err
        return make_response(str(err), 400)
    except RuntimeError as err:
        print err
        return make_response(str(err), 400)
    except Exception as err:
        print err
        return make_response(str(err), 500)

@APP.route('/tournamentDetails/<t_name>', methods=['GET'])
def tournament_details(t_name=None):
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    try:
        tourn = Tournament(t_name)
        return DateTimeJSONEncoder().encode(tourn.details())
    except RuntimeError as err:
        return make_response(str(err), 400)
    except Exception as err:
        print err
        return make_response(str(err), 500)

@APP.route('/userDetails/<u_name>', methods=['GET'])
def user_details(u_name=None):
    """
    GET to get account details in url form
    TODO security
    """

    try:
        return jsonify({u_name: PLAYER_DB_CONN.user_details(u_name)})
    except RuntimeError as err:
        return make_response(str(err), 400)
    except Exception as err:
        print err
        return make_response(str(err), 500)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)


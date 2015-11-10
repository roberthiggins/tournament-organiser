"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

import os
import re

from flask import Flask, request, make_response

from feedback_db import FeedbackDBConnection
from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection
from registration_db import RegistrationDBConnection

APP = Flask(__name__)
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
    from flask import jsonify
    return jsonify({'tournaments' : TOURNAMENT_DB_CONN.listTournaments()})

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

    return make_response(
            REGISTRATION_DB_CONN.registerForTournament(
                tournament_name,
                username),
            200)

@APP.route('/addTournament', methods=['POST'])
def add_tournament():
    """
    POST to add a tournament
    Expects:
        - inputTournamentName - Tournament name. Must be unique.
        - inputTournamentDate - Tournament Date. YYYY-MM-DD
    """
    import datetime
    name = request.form['inputTournamentName']
    date = request.form['inputTournamentDate']

    if not name or not date:
        return make_response("Please fill in the required fields", 400)

    try:
        date = datetime.datetime.strptime(
                    request.form['inputTournamentDate'],
                    "%Y-%m-%d")
        assert date.date() >= datetime.date.today()
    except ValueError:
        return make_response("Enter a valid date", 400)

    if TOURNAMENT_DB_CONN.tournamentExists(name):
        return make_response("A tournament with name %s already exists! \
        Please choose another name" % name, 400)
    TOURNAMENT_DB_CONN.addTournament({'name' : name, 'date' : date})
    return make_response('<p>Tournament Created! You submitted the \
        following fields:</p><ul><li>Name: {name}</li><li>Date: {date} \
        </li></ul>'.format(**locals()), 200)

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
        - inputUsername
        - inputEmail
        - inputPassword
        - inputConfirmPassword
    """
    username = request.form['inputUsername'].strip()
    email = request.form['inputEmail'].strip()
    password = request.form['inputPassword'].strip()
    confirm = request.form['inputConfirmPassword'].strip()

    if not username:
        return make_response("Please fill in the required fields", 400)

    if not validate_user_email(email):
        return make_response("This email does not appear valid", 400)

    if not password or not confirm or password != confirm:
        return make_response("Please enter two matching passwords", 400)

    if PLAYER_DB_CONN.usernameExists(username):
        return make_response("A user with the username %s already exists! \
            Please choose another name" % username, 400)

    PLAYER_DB_CONN.addAccount({'user_name': username,
                               'email' : email,
                               'password': password})
    return make_response('<p>Account created! You submitted the following \
        fields:</p><ul><li>User Name: {username}</li><li>Email: {email}\
        </li></ul>'.format(**locals()), 200)

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
    FEEDBACK_DB_CONN.submitFeedback(_feedback)
    return make_response("Thanks for you help improving the site", 200)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)


import datetime
import os
import re

from flask import Flask, render_template, request, json, make_response, jsonify

from feedback_db import FeedbackDBConnection
from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection
from registration_db import RegistrationDBConnection

app                     = Flask(__name__)
feedback_db_conn        = FeedbackDBConnection()
player_db_conn          = PlayerDBConnection()
tournament_db_conn      = TournamentDBConnection()
registration_db_conn    = RegistrationDBConnection()

@app.route("/")
def main():
    return make_response('daoserver', 200)

# Page actions
@app.route('/listtournaments', methods=['GET'])
def listTournaments():
    return jsonify({'tournaments' : tournament_db_conn.listTournaments()})

@app.route('/registerfortournament', methods=['POST'])
def applyForTournament():
    _userName = request.form['inputUserName']
    _tournamentName = request.form['inputTournamentName']

    if not _userName or not _tournamentName:
        return make_response("Enter the required fields", 400)

    try:
        return make_response(
                registration_db_conn.registerForTournament(
                    _tournamentName,
                    _userName),
                200)
    except Error as e:
        return make_response(e, 200)


@app.route('/addTournament', methods=['POST'])
def addTournament():
    _name = request.form['inputTournamentName']
    _date = request.form['inputTournamentDate']

    if not _name or not _date:
        return make_response("Please fill in the required fields", 400)

    try:
        _date = datetime.datetime.strptime(
                    request.form['inputTournamentDate'],
                    "%Y-%m-%d")
        assert _date.date() >= datetime.date.today()
    except Exception as e:
        return make_response("Enter a valid date", 400)

    try:
        if tournament_db_conn.tournamentExists(_name):
            return make_response("A tournament with name %s already exists! Please choose another name" % _name, 400)
        tournament_db_conn.addTournament({'name' : _name, 'date' : _date})
        return make_response('<p>Tournament Created! You submitted the following fields:</p><ul><li>Name: {_name}</li><li>Date: {_date}</li></ul>'.format(**locals()), 200)
    except Error as e:
        return make_response(e, 500)

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    _user_name = request.form['inputUsername'].strip()
    _email = request.form['inputEmail'].strip()
    _password = request.form['inputPassword'].strip()
    _confirmPassword = request.form['inputConfirmPassword'].strip()

    if not _user_name:
        return make_response("Please fill in the required fields", 400)

    if not validateEmail(_email):
        return make_response("This email does not appear valid", 400)

    if not _password or not _confirmPassword or _password != _confirmPassword:
        return make_response("Please enter two matching passwords", 400)

    try:
        if player_db_conn.usernameExists(_user_name):
            return make_response("A user with the username %s already exists! Please choose another name" % _user_name, 400)

        player_db_conn.addAccount({'user_name': _user_name, 'email' : _email, 'password': _password})
        return make_response('<p>Account created! You submitted the following fields:</p><ul><li>User Name: {_user_name}</li><li>Email: {_email}</li></ul>'.format(**locals()), 200)
    except Error as e:
        return make_response(e, 500)

@app.route('/placefeedback', methods=['POST'])
def placeFeedback():
    _feedback = request.form['inputFeedback'].strip('\s\n\r\t\+')
    if re.match( r'^[\+\s]*$', _feedback) is not None:
        return make_response("Please fill in the required fields", 400)
    try:
        feedback_db_conn.submitFeedback(_feedback)
        return make_response("Thanks for you help improving the site", 200)
    except Error as e:
        return make_response(e, 200)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


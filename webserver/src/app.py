import os
import yaml

from flask import Flask, render_template, request, json, make_response

from player_db import PlayerDBConnection

app     = Flask(__name__)
conn = PlayerDBConnection()

# Page rendering
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showRegisterForTournament')
def showRegisterForTournament():
    return render_template('register-for-tournament.html')

@app.route('/showPlayerSignUp')
def showAddPlayer():
    return render_template('player-sign-up.html')

# Page actions
@app.route('/registerForTournament', methods=['POST'])
def applyForTournament():
    _name = request.form['inputName']
    _email = request.form['inputEmail']

    if _name and _email:
        return json.dumps({'html':'<p>You submitted the following fields:</p><ul><li>Name: {_name}</li><li>Email: {_email}</li></ul>'.format(**locals())})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    _user_name = request.form['inputUserName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _user_name and _email and _password:
        try:
            if conn.usernameExists(_user_name):
                return make_response("A user with the username %s already exists! Please choose another name" % _user_name, 400)

            conn.addAccount({'user_name': _user_name, 'email' : _email, 'password': _password})
            return make_response('<p>Account Created! You submitted the following fields:</p><ul><li>User Name: {_user_name}</li><li>Email: {_email}</li></ul>'.format(**locals()), 200)
        except Error as e:
            return make_response(e, 500)
    else:
        return make_response("Please enter the required fields", 400)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


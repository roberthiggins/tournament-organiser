"""
Entrypoint for Webserver.

The webserver provides a website for interacting with the Tournament Organiser.
"""

import os
import urllib2
import urllib

from flask import Flask, render_template, request, make_response, json

APP = Flask(__name__)
DAO_URL = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])


# Page rendering
@APP.route("/")
def main():
    """The index"""
    return render_template('index.html')

@APP.route('/createtournament')
def show_create_tournament():
    """Page for creating a tournament"""
    return render_template('create-a-tournament.html')

@APP.route('/feedback')
def show_place_feedback():
    """ Page for user to place feedback"""
    return render_template('feedback.html',
        title='Place Feedback',
        intro='Please give us feedback on your experience on the site')

@APP.route('/login')
def show_login():
    """Login page"""
    return render_template('login.html')

@APP.route('/registerforatournament')
def show_register_for_tournament():
    """Page to register for tournament"""
    t_list = json.load(get_from_dao('/listtournaments'))['tournaments']
    return render_template('register-for-tournament.html', tournaments=t_list)

@APP.route('/signup')
def show_create_account():
    """Page to create a new account"""
    return render_template('create-a-player.html')

@APP.route('/suggestimprovement')
def show_suggest_improvement():
    """Page to suggest improvements to the site"""
    return render_template('feedback.html',
        title='Suggest Improvement',
        intro='Suggest a feature you would like to see on the site')

# Page actions
def get_from_dao(url):
    """
    Proxies a GET to the daoserver. This helps keep input handling in the DAO \
    api
    """
    try:
        return urllib2.urlopen(urllib2.Request(DAO_URL + url))
    except Exception as err:
        print err
        raise

def post_to_dao(url):
    """
    Proxies a POST to the daoserver. This helps keep input handling in the DAO \
    api
    """
    try:
        req = urllib2.urlopen(urllib2.Request(
                                DAO_URL + url,
                                urllib.urlencode(request.form)))
        return make_response(req.read(), 200)
    except urllib2.HTTPError, err:
        if err.code == 400:
            return make_response(err.read(), 400)
        else:
            raise

@APP.route('/registerfortournament', methods=['POST'])
def apply_for_tournament():
    """Page for player to apply to a tournament"""
    return post_to_dao('/registerfortournament')

@APP.route('/addTournament', methods=['POST'])
def add_tournament():
    """Page to add a tournament"""
    return post_to_dao('/addTournament')

@APP.route('/addPlayer', methods=['POST'])
def add_player():
    """POST target for player creation. This will get proxied to DAO server"""
    return post_to_dao('/addPlayer')

@APP.route('/loginAccount', methods=['POST'])
def login_account():
    """POST target for login attempts. This will get proxied to DAO server"""
    return post_to_dao('/login')

@APP.route('/placefeedback', methods=['POST'])
def place_feedback():
    """POST target for feedback. This will get proxied to DAO server"""
    return post_to_dao('/placefeedback')


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=PORT)


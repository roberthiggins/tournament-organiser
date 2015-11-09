import datetime
import os
import re
import urllib2
import urllib

from flask import Flask, render_template, request, make_response, json

app     = Flask(__name__)
dao_url = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])


# Page rendering
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/createtournament')
def showCreateTournament():
    return render_template('create-a-tournament.html')

@app.route('/feedback')
def showPlaceFeedback():
    return render_template('feedback.html',
        title='Place Feedback',
        intro='Please give us feedback on your experience on the site')

@app.route('/login')
def showLogin():
    return render_template('login.html')

@app.route('/registerforatournament')
def showRegisterForTournament():
    tList = json.load(getFromDao('/listtournaments'))['tournaments']
    return render_template('register-for-tournament.html', tournaments=tList)

@app.route('/signup')
def showAddPlayer():
    return render_template('create-a-player.html')

@app.route('/suggestimprovement')
def showSuggestImprovement():
    return render_template('feedback.html', title='Suggest Improvement', intro='Suggest a feature you would like to see on the site')

# Page actions
def getFromDao(url):
    try:
        return urllib2.urlopen(urllib2.Request(dao_url + url))
    except Exception as e:
        print e
        raise

def postToDao(url):
    try:
        r = urllib2.urlopen(urllib2.Request(
                                dao_url + url,
                                urllib.urlencode(request.form)))
        return make_response(r.read(), 200)
    except urllib2.HTTPError, err:
        if err.code == 400:
            return make_response(err.read(), 400)
        else:
            raise

@app.route('/registerfortournament', methods=['POST'])
def applyForTournament():
    return postToDao('/registerfortournament')

@app.route('/addTournament', methods=['POST'])
def addTournament():
    return postToDao('/addTournament')

@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    return postToDao('/addPlayer')

@app.route('/loginAccount', methods=['POST'])
def loginAccount():
    return postToDao('/login')

@app.route('/placefeedback', methods=['POST'])
def placeFeedback():
    return postToDao('/placefeedback')


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


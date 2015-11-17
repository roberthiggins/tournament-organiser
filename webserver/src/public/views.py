""" Basic URL mappings for the webserver """
import json
import os
import urllib
import urllib2

from forms import AddTournamentForm, ApplyForTournamentForm, \
CreateAccountForm, FeedbackForm, LoginForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

DAO_URL = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])

def index(request):                                     # pylint: disable=W0613
    """The index"""
    return render_to_response('index.html')

def create_account(request):
    """Page to create a new account"""
    return render_to_response(
        'create-a-player.html',
        {'form': CreateAccountForm()},
        RequestContext(request)
    )

def create_tournament(request):
    """Page for creating a tournament"""
    return render_to_response(
        'create-a-tournament.html',
        {'form': AddTournamentForm()},
        RequestContext(request)
    )

def feedback(request):
    """ Page for user to place feedback"""
    context_dict = {
        'title': 'Place Feedback',
        'intro': 'Please give us feedback on your experience on the site',
        'form': FeedbackForm()
    }
    return render_to_response(
        'feedback.html',
        context_dict,
        RequestContext(request)
    )

def login(request):
    """Login page"""
    return render_to_response(
        'login.html',
        {'form': LoginForm()},
        RequestContext(request)
    )

def get_tournament_list():
    """ Get a list of tournaments; tupled for your convenience"""
    t_list = json.load(get_from_dao('/listtournaments'))['tournaments']
    return [(x, x) for x in t_list]

def register_for_tournament(request):
    """Page to register for tournament"""
    return render_to_response(
        'register-for-tournament.html',
        {'form': ApplyForTournamentForm(tournament_list=get_tournament_list())},
        RequestContext(request)
    )

def suggest_improvement(request):
    """Page to suggest improvements to the site"""
    context_dict = {
        'title': 'Suggest Improvement',
        'intro': 'Suggest a feature you would like to see on the site',
        'form': FeedbackForm()
    }
    return render_to_response(
        'feedback.html',
        context_dict,
        RequestContext(request)
    )

### Some helper methods

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

def post_to_dao(url, form):
    """
    Proxies a POST to the daoserver. This helps keep input handling in the DAO \
    api
    """
    try:
        if not form.is_valid():
            return HttpResponse(form.error_code(), status=400)

        response = urllib2.urlopen(urllib2.Request(
            DAO_URL + url,
            urllib.urlencode(form.cleaned_data)))
        return HttpResponse(response)
    except urllib2.HTTPError, err:
        if err.code == 400:
            return HttpResponse(err.read(), status=400)
        else:
            raise

### Wrappers to Dao
def apply_for_tournament(request):
    """Page for player to apply to a tournament"""
    return post_to_dao(
        '/registerfortournament',
        ApplyForTournamentForm(
            request.POST,
            tournament_list=get_tournament_list())
    )

def add_tournament(request):
    """Page to add a tournament"""
    return post_to_dao('/addTournament', AddTournamentForm(request.POST))

def add_player(request):
    """POST target for player creation. This will get proxied to DAO server"""
    return post_to_dao('/addPlayer', CreateAccountForm(request.POST))

def login_account(request):
    """POST target for login attempts. This will get proxied to DAO server"""
    return post_to_dao('/login', LoginForm(request.POST))

def place_feedback(request):
    """POST target for feedback. This will get proxied to DAO server"""
    return post_to_dao('/placefeedback', FeedbackForm(request.POST))


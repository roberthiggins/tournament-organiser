""" Basic URL mappings for the webserver """
import json
import os
import urllib
import urllib2

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import AddTournamentForm, ApplyForTournamentForm, \
CreateAccountForm, FeedbackForm, LoginForm

DAO_URL = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])

def index(request):                                     # pylint: disable=W0613
    """The index"""
    return render_to_response('index.html')

def create_account(request):
    """Page to create a new account"""

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()

        return from_dao('/addPlayer', form)

    return render_to_response(
        'create-a-player.html',
        {'form': CreateAccountForm()},
        RequestContext(request)
    )

@login_required
def create_tournament(request):
    """Page for creating a tournament"""

    if request.method == 'POST':
        return from_dao('/addTournament', AddTournamentForm(request.POST))

    return render_to_response(
        'create-a-tournament.html',
        {'form': AddTournamentForm()},
        RequestContext(request)
    )

@login_required
def feedback(request):
    """ Page for user to place feedback"""

    if request.method == 'POST':
        return from_dao('/placefeedback', FeedbackForm(request.POST))

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

def render_login(request, form):
    return render_to_response(
        'login.html',
        {'form': form,
        'title': 'Tournament Organiser Login',
        'intro': 'You can add/change your details here:'
        },
        RequestContext(request)
    )

def create_or_update_user(login_creds):
    """
    Create a new local user or update from db.

    A failure to authenticate locally could be because the user details have
    been updated on the db but not on this webserver

    TODO security to ensure the user is actually in the db
    """
    u_name = login_creds.cleaned_data['inputUsername']
    p_word = login_creds.cleaned_data['inputPassword']
    user = json.load(from_dao('/userDetails/%s' % u_name)).get(u_name)

    try:
        local_user = User.objects.get(username=u_name)
        local_user.set_password(p_word)
        local_user.email = user[0]
        local_user.save()
    except User.DoesNotExist as err:
        User.objects.create_user(
            username=u_name,
            email=user[0],
            password=p_word)

def login(request):
    """Login page"""

    login_creds = LoginForm()
    if request.user.is_authenticated():
        return make_response('You are already logged in')

    if request.method == 'POST':
        login_creds = LoginForm(request.POST)

        username = request.POST.get('inputUsername', '')
        password = request.POST.get('inputPassword', '')
        if username == '' or password == '':
            return render_login(request, login_creds)

        response = from_dao('/login', login_creds)
        if  response.status_code == 200:
            # The user might exist in the db but not on this webserver.
            create_or_update_user(login_creds)
            user = auth.authenticate(username = username, password=password)
            auth.login(request, user)
        else:
            login_creds.add_error(None, 'Username or password incorrect') # pylint: disable=E1103
            return render_login(request, login_creds)

        return HttpResponseRedirect(request.REQUEST.get('next', '/'))

    return render_login(request, login_creds)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def get_tournament_list():
    """ Get a list of tournaments; tupled for your convenience"""
    t_list = json.load(from_dao('/listtournaments'))['tournaments']
    return [(x, x) for x in t_list]

@login_required
def register_for_tournament(request):
    """Page to register for tournament"""

    if request.method == 'POST':
        return from_dao(
            '/registerfortournament',
            ApplyForTournamentForm(
                request.POST,
                tournament_list=get_tournament_list())
        )

    return render_to_response(
        'register-for-tournament.html',
        {'form': ApplyForTournamentForm(tournament_list=get_tournament_list())},
        RequestContext(request)
    )

@login_required
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

def from_dao(url, form=None):
    """
    Proxies a GET/POST to the daoserver. This helps keep input handling in \
    the DAO API
    """
    try:

        if form is None:
            return urllib2.urlopen(urllib2.Request(DAO_URL + url))

        if form.is_valid():
            return HttpResponse(
                urllib2.urlopen(urllib2.Request(DAO_URL + url,
                urllib.urlencode(form.cleaned_data))))

        return HttpResponse(form.error_code(), status=400)

    except urllib2.HTTPError as err:
        if err.code == 400:
            return HttpResponse(err.read(), status=400)
        else:
            raise
    except Exception as err:
        print err
        raise

"""
Basic URL mappings for the webserver
"""

import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import CreateAccountForm, LoginForm
from public.view_helpers import from_dao

def index(request):                                     # pylint: disable=W0613
    """The index"""
    return render_to_response('index.html')

def create_account(request):
    """Page to create a new account"""

    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():                             # pylint: disable=E1101
            form.save()

        response = from_dao('/addPlayer', form)

        if  response.status_code == 200:
            return HttpResponse(response)
        else:
            form.add_error(None, response.content)      # pylint: disable=E1103

    return render_to_response(
        'create-a-player.html',
        {'form': form},
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
    except User.DoesNotExist:                           # pylint: disable=E1101
        User.objects.create_user(
            username=u_name,
            email=user[0],
            password=p_word)

def list_tournaments(request):
    """ Get a list of tournaments"""
    t_list = json.load(from_dao('/listtournaments'))['tournaments']
    return render_to_response(
        'tournament-list.html',
        {'tournaments': t_list},
        RequestContext(request)
    )

def login(request):
    """Login page"""

    login_creds = LoginForm()
    if request.user.is_authenticated():
        return render_to_response('You are already logged in')

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
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
        else:
            login_creds.add_error(None, 'Username or password incorrect') # pylint: disable=E1103
            return render_login(request, login_creds)

        return HttpResponseRedirect(request.REQUEST.get('next', '/'))

    return render_login(request, login_creds)

def render_login(request, form):
    """ Render the login page from the template """
    return render_to_response(
        'login.html',
        {'form': form},
        RequestContext(request)
    )

def tournament(request, tournament_id):
    """ See information about a single tournament"""
    if tournament_id is None:
        return list_tournaments(request)
    if request.method == 'POST':
        return HttpResponseRedirect('/registerforatournament')

    response = from_dao('/tournamentDetails/%s' % tournament_id)
    try:
        t_info = json.load(response)
        return render_to_response(
            'tournament-info.html',
            {'id': tournament_id, 'info': t_info},
            RequestContext(request)
        )
    except AttributeError:
        return HttpResponse(response)

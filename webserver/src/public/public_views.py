"""
Basic URL mappings for the webserver
"""

import json
from ratelimit.decorators import ratelimit

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from public.forms import CreateAccountForm, LoginForm
from public.view_helpers import from_dao

@ratelimit(key='ip', rate='100/m', block=True)
def index(request):                                     # pylint: disable=W0613
    """The index"""
    return render_to_response('index.html')

def dev_index(request):                 # pylint: disable=unused-argument
    """Some more tasks, used for dev only"""
    return render_to_response('dev-index.html')

@ratelimit(key='ip', rate='50/h', block=True)
def create_account(request):
    """Page to create a new account"""

    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():                             # pylint: disable=no-member
            form.save()

            response = from_dao('/addPlayer', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

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
    user = json.loads(from_dao('/userDetails/%s' % u_name).content).get(u_name)

    try:
        # pylint: disable=no-member
        local_user = User.objects.get(username=u_name)
        local_user.set_password(p_word)
        local_user.email = user[0]
        local_user.save()
    except User.DoesNotExist:                           # pylint: disable=no-member
        User.objects.create_user(
            username=u_name,
            email=user[0],
            password=p_word)

@ratelimit(key='ip', rate='100/m', block=True)
def list_tournaments(request):
    """ Get a list of tournaments"""
    t_list = json.loads(from_dao('/listtournaments').content)['tournaments']
    return render_to_response(
        'tournament-list.html',
        {'tournaments': t_list},
        RequestContext(request)
    )

@ratelimit(key='ip', rate='100/m', block=True)
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

        if login_creds.is_valid():
            request.user = auth.authenticate(
                username=username,
                password=password)

        response = from_dao('/login', form=login_creds, request=request)
        if  response.status_code == 200:
            # The user might exist in the db but not on this webserver.
            create_or_update_user(login_creds)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
        else:
            login_creds.add_error(None, 'Username or password incorrect') # pylint: disable=E1103
            return render_login(request, login_creds)

        return HttpResponseRedirect(request.GET.get('next', '/devindex'))

    return render_login(request, login_creds)

@ratelimit(key='ip', rate='100/m', block=True)
def render_login(request, form):
    """ Render the login page from the template """
    return render_to_response(
        'login.html',
        {'form': form},
        RequestContext(request)
    )

@ratelimit(key='ip', rate='100/m', block=True)
def tournament(request, tournament_id):
    """ See information about a single tournament"""
    if tournament_id is None:
        return list_tournaments(request)
    if request.method == 'POST':
        return HttpResponseRedirect('/registerforatournament')

    try:
        response = from_dao('/tournamentDetails/%s' % tournament_id).content
        t_info = json.loads(response)
        return render_to_response(
            'tournament-info.html',
            {'id': tournament_id, 'info': t_info},
            RequestContext(request)
        )
    except AttributeError:
        return HttpResponse(response)
    except ValueError:
        return HttpResponse(response)

@ratelimit(key='ip', rate='100/m', block=True)
def tournament_draw(request, tournament_id, round_id):
    """Get the entire tournament draw for a single round of a tournament"""
    if tournament_id is None or round_id is None:
        return HttpResponseNotFound()

    try:
        response = from_dao(
            '/roundInfo/{}/{}'.format(tournament_id, round_id)
        ).content
        json_data = json.loads(response)
    except ValueError:
        return HttpResponse(response)

    return render_to_response(
        'draw.html',
        {
            'tournament_id': tournament_id,
            'round': round_id,
            'draw': json_data['draw'],
            'mission': json_data['mission'],
        },
        RequestContext(request)
    )

@ratelimit(key='ip', rate='100/m', block=True)
def tournament_rankings(request, tournament_id):
    """Get placings for the entries in the tournament"""
    if tournament_id is None:
        return HttpResponseNotFound()
    try:
        json_data = json.loads(
            from_dao('/rankEntries/%s' % tournament_id).content)

        return render_to_response(
            'tournament-rankings.html',
            {
                'tournament_id': tournament_id,
                'placings': json_data,
            },
            RequestContext(request)
            )
    except ValueError:
        return HttpResponseNotFound()


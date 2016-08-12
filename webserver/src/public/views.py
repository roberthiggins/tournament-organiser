"""
Basic URL mappings for the webserver
"""

import os
import json
import urllib2

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, \
HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from public.forms import ApplyForTournamentForm, \
EnterScoreForm, EnterGameScoreForm, SetMissionsForm
from public.view_helpers import from_dao

NODE_URL = 'http://{}:{}'.format(
    os.environ['NODE_PORT_8000_TCP_ADDR'],
    os.environ['NODE_PORT_8000_TCP_PORT']
)

def entry_info(tournament_id, username):
    """Get information about an entry"""
    resp = from_dao('/tournament/{}/entry/{}'.format(tournament_id, username))
    if resp.status_code != 200:
        raise ValueError(resp.content)
    return json.loads(resp.content)

def categories_info(tournament_id):
    """Get the score_categories info for a tournament"""
    resp = from_dao('/tournament/{}/score_categories'.format(tournament_id))
    if resp.status_code != 200:
        raise ValueError('Tournament {} not found'.format(tournament_id))
    return json.loads(resp.content)

@login_required
def enter_score(request, tournament_id, username):      # pylint: disable=W0613
    """Enter score for entry"""

    try:
        entry_info(tournament_id, username)
        cats = [(x['name'], x['name']) for x in categories_info(tournament_id) \
                if x['per_tournament']]
    except ValueError as err:
        return HttpResponseNotFound(err)

    form = EnterScoreForm(username=username,
                          tournament=tournament_id,
                          poster=request.user.username,
                          categories=cats)

    if request.method == 'POST':
        form = EnterScoreForm(data=request.POST,
                              username=username,
                              tournament=tournament_id,
                              poster=request.user.username,
                              categories=cats)

        if form.is_valid():                     # pylint: disable=no-member
            url = '/tournament/{}/entry/{}/entertournamentscore'.\
                format(tournament_id, username)
            response = from_dao(url, form, request)
            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'enter-score.html',
        {'form': form, 'username': username},
        RequestContext(request)
    )

def get_next_game_info(t_id, user):
    """Get the next game for entry"""
    try:
        resp = from_dao('/tournament/{}/entry/{}/nextgame'.format(t_id, user))
        next_game_info = json.loads(resp.content)
        if not next_game_info:
            raise ValueError

        return next_game_info
    except ValueError:
        raise ValueError('No current game found! please contact TO.')

@login_required
def enter_score_for_game(request, t_id, user):
    """ Enter a score for a single game"""
    try:
        entry_info(t_id, user)
        next_game_info = get_next_game_info(t_id, user)
    except ValueError as err:
        return HttpResponseNotFound(err)

    cats = [(x['name'], x['name']) for x in categories_info(t_id) \
            if not x['per_tournament']]
    form = EnterGameScoreForm(game_id=next_game_info['game_id'],
                              poster=request.user.username,
                              categories=cats)

    if request.method == 'POST':
        form = EnterGameScoreForm(data=request.POST,
                                  game_id=next_game_info['game_id'],
                                  poster=request.user.username,
                                  categories=cats)

        if form.is_valid():                     # pylint: disable=no-member
            url = '/tournament/{}/entry/{}/entergamescore'.format(t_id, user)
            response = from_dao(url, form, request)
            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'enter-game-score.html',
        {
            'categories': cats,
            'form': form,
            'tournament': t_id,
            'tournament_round': next_game_info['round'],
            'username': user
        },
        RequestContext(request)
    )

@login_required
def entry_list(request, tournament_id):
    """List entrants for a tournament"""
    response = from_dao('/tournament/{}/entry/'.format(tournament_id))
    if response.status_code != 200:
        return HttpResponse(response, status=response.status_code)

    return render_to_response(
        'entry-list.html',
        {
            'tournament': tournament_id,
            'entries': json.loads(response.content)
        },
        RequestContext(request)
    )

def logout(request):
    """ logout the user from current request """
    auth.logout(request)
    return HttpResponseRedirect('/')

# pylint: disable=unused-argument
def set_categories(request, tournament_id):
    """Set the scoring categories for a tournament"""
    return HttpResponseRedirect('{}/tournament/{}/categories'.\
        format(NODE_URL, tournament_id))

@login_required
def set_missions(request, tournament_id):
    """Set the number of rounds for a competition"""
    tourn_path = '/tournament/{}'.format(tournament_id)
    t_details = from_dao(tourn_path)
    if t_details.status_code != 200:
        return HttpResponseNotFound(
            'Tournament {} not found'.format(tournament_id))
    rounds = int(json.loads(t_details.content)['rounds'])

    existing_missions = json.loads(
        from_dao('{}/missions'.format(tourn_path)).content)

    form = SetMissionsForm(
        tournament_id=tournament_id,
        initial_missions=existing_missions,
        rounds=rounds)

    if request.method == 'POST':
        form = SetMissionsForm(
            request.POST,
            tournament_id=tournament_id,
            rounds=rounds)

        if form.is_valid():                     # pylint: disable=no-member
            response = from_dao('{}/missions'.format(tourn_path), form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'set-missions.html',
        {
            'form': form,
            'tournament': tournament_id,
        },
        RequestContext(request)
    )

@login_required
def register_for_tournament(request):
    """Page to register for tournament"""

    t_list = json.loads(from_dao('/tournament/').content)['tournaments']
    t_list = [(x['name'], x['name']) for x in t_list]
    form = ApplyForTournamentForm(tournament_list=t_list)

    if request.method == 'POST':
        form = ApplyForTournamentForm(request.POST, tournament_list=t_list)
        if form.is_valid():                     # pylint: disable=no-member
            t_name = form.cleaned_data['inputTournamentName']
            response = from_dao('/tournament/{}/register'.format(t_name), form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'register-for-tournament.html',
        {'form': form},
        RequestContext(request)
    )

#pylint: disable=unused-argument
def set_rounds(request, tournament_id):
    """Set the number of rounds for a competition"""
    return HttpResponseRedirect('{}/tournament/{}/rounds'.\
        format(NODE_URL, tournament_id))

def score_categories(tournament_id):
    """
    Get a list of score categories for a tournament. THey should be ready for
    insertion into a select.
    """
    try:
        response = from_dao(
            '/tournament/{}/score_categories'.format(tournament_id))
        return [
            (x['id'], '{} ({}%)'.format(x['name'], int(x['percentage'])))
            for x in json.loads(response.content)
        ]
    except urllib2.HTTPError:
        return []

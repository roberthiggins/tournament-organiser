"""
Basic URL mappings for the webserver
"""

import json
import urllib2

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, \
HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from public.forms import AddTournamentForm, ApplyForTournamentForm, \
EnterScoreForm, FeedbackForm, SetRoundsForm, \
SetCategoriesForm, SetMissionsForm
from public.view_helpers import from_dao

@login_required
def create_tournament(request):
    """Page for creating a tournament"""

    form = AddTournamentForm()

    if request.method == 'POST':
        form = AddTournamentForm(request.POST)
        if form.is_valid():                     # pylint: disable=no-member
            response = from_dao('/tournament', form, request)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103


    return render_to_response(
        'create-a-tournament.html',
        {'form': form},
        RequestContext(request)
    )

@login_required
def enter_score(request, tournament_id, username):      # pylint: disable=W0613
    """Enter score page when the entry_id isn't known"""
    try:
        response = from_dao('/entryId/{}/{}'.format(tournament_id, username))
        entry_id = json.loads(response.content)
        return HttpResponseRedirect('/enterscore/{}'.format(entry_id))
    except ValueError:
        return HttpResponseNotFound(response.content)

@login_required
def enter_score_by_entry(request, entry_id):
    """Enter score page"""
    try:
        entry_id = int(entry_id)
    except ValueError:
        return HttpResponseNotFound()

    response = from_dao('/entryInfo/{}'.format(entry_id))
    if response.status_code != 200:
        return HttpResponse(response, status=response.status_code)

    user_info = json.loads(response.content)
    form = EnterScoreForm(
        username=user_info['username'],
        tournament=user_info['tournament_name'])

    if request.method == 'POST':
        form = EnterScoreForm(
            data=request.POST,
            username=user_info['username'],
            tournament=user_info['tournament_name'])

        if form.is_valid():                             # pylint: disable=no-member
            response = from_dao('/entertournamentscore', form, request)
            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'enter-score.html',
        {'form': form, 'username': user_info['username']},
        RequestContext(request)
    )

@login_required
# pylint: disable=W0613
def enter_score_for_game(tournament_id, username, round_id):
    """ Enter a score for a single game"""
    return
    # form = EnterScoreForm()
    # if request.method == 'POST':
    #     pass
    # work out what game we're talking about
    # get the scores that need to be filled in for this game
    # make a form

    # if the request is a post:
    #   validate the form
    #   send the info back to the db

    # render the form and pass back to the browser

@login_required
def entry_list(request, tournament_id):
    """List entrants for a tournament"""
    response = from_dao('/tournament/{}/entries'.format(tournament_id))
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

@login_required
def feedback(request):
    """ Page for user to place feedback"""

    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():                             # pylint: disable=no-member
            response = from_dao('/feedback', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    context_dict = {
        'title': 'Place Feedback',
        'intro': 'Please give us feedback on your experience on the site',
        'form': form
    }
    return render_to_response(
        'feedback.html',
        context_dict,
        RequestContext(request)
    )

def logout(request):
    """ logout the user from current request """
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def set_categories(request, tournament_id):
    """Set the scoring categories for a tournament"""
    cats_request = from_dao('/getScoreCategories/{}'.format(tournament_id))
    if cats_request.status_code != 200:
        return HttpResponseNotFound(
            'Tournament {} not found'.format(tournament_id))
    cats = [[x['name'], x['percentage'], x['per_tournament'], x['min_val'], \
        x['max_val']] for x in json.loads(cats_request.content)]
    form = SetCategoriesForm(tournament_id=tournament_id, categories=cats)

    if request.method == 'POST':

        form = SetCategoriesForm(request.POST,
                                 tournament_id=tournament_id,
                                 categories=cats)

        if form.is_valid():
            # We need to do some mangling. I suppose it could be built into the
            # form but simpler to do it here.
            form.cleaned_data['categories'] = json.dumps([
                k for k, v in form.cleaned_data.iteritems() \
                if k.startswith('categories_') and v != form.empty_field()])

            response = from_dao('/setScoreCategories', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)

    return render_to_response(
        'set-categories.html',
        {
            'form': form,
            'tournament': tournament_id,
        },
        RequestContext(request)
    )

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

@login_required
def set_rounds(request, tournament_id):
    """Set the number of rounds for a competition"""
    t_details = from_dao('/tournament/{}'.format(tournament_id))
    if t_details.status_code != 200:
        return HttpResponseNotFound(
            'Tournament {} not found'.format(tournament_id))
    rounds = int(json.loads(t_details.content)['rounds'])
    rounds = 5 if rounds < 1 else rounds

    form = SetRoundsForm(
        initial={'numRounds': rounds}, tournament_id=tournament_id)

    if request.method == 'POST':
        form = SetRoundsForm(request.POST, tournament_id=tournament_id)
        if form.is_valid():                             # pylint: disable=no-member
            response = from_dao('/setRounds', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'set-rounds.html',
        {
            'form': form,
            'tournament': tournament_id
        },
        RequestContext(request)
    )

@login_required
def suggest_improvement(request):
    """Page to suggest improvements to the site"""

    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():                             # pylint: disable=no-member
            response = from_dao('/feedback', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    context_dict = {
        'title': 'Suggest Improvement',
        'intro': 'Suggest a feature you would like to see on the site',
        'form': form
    }
    return render_to_response(
        'feedback.html',
        context_dict,
        RequestContext(request)
    )

def score_categories(tournament_id):
    """
    Get a list of score categories for a tournament. THey should be ready for
    insertion into a select.
    """
    try:
        response = from_dao('/getScoreCategories/{}'.format(tournament_id))
        return [
            (x['id'], '{} ({}%)'.format(x['name'], int(x['percentage'])))
            for x in json.loads(response.content)
        ]
    except urllib2.HTTPError:
        return []

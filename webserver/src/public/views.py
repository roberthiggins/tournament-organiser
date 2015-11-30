"""
Basic URL mappings for the webserver
"""

import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, \
HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import AddTournamentForm, ApplyForTournamentForm, \
EnterScoreForm, FeedbackForm, TournamentSetupForm
from public.view_helpers import from_dao

@login_required
def create_tournament(request):
    """Page for creating a tournament"""

    form = AddTournamentForm()

    if request.method == 'POST':
        form = AddTournamentForm(request.POST)
        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/addTournament', form)

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
def enter_score_by_entry(request, entry_id):
    """Enter score page"""
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

        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/entertournamentscore', form)
            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    return render_to_response(
        'enter-score.html',
        {'form': form,
        'username': user_info['username'],
        },
        RequestContext(request)
    )

@login_required
def feedback(request):
    """ Page for user to place feedback"""

    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/placefeedback', form)

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
def register_for_tournament(request):
    """Page to register for tournament"""

    t_list = json.loads(from_dao('/listtournaments').content)['tournaments']
    t_list = [(x['name'], x['name']) for x in t_list]
    form = ApplyForTournamentForm(tournament_list=t_list)

    if request.method == 'POST':
        form = ApplyForTournamentForm(request.POST, tournament_list=t_list)
        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/registerfortournament', form)

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
def suggest_improvement(request):
    """Page to suggest improvements to the site"""

    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/placefeedback', form)

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

@login_required
def tournament_setup(request, tournament_id):
    """Adda score to a tournament"""
    form = TournamentSetupForm(tournament_id=tournament_id)

    if request.method == 'POST':
        form = TournamentSetupForm(request.POST, tournament_id=tournament_id)
        if form.is_valid():                             # pylint: disable=E1101
            response = from_dao('/setTournamentScore', form)

            if  response.status_code == 200:
                return HttpResponse(response)
            else:
                form.add_error(None, response.content)  # pylint: disable=E1103

    tournament_details = from_dao('/tournamentDetails/%s' % tournament_id)
    if tournament_details.status_code != 200:
        return HttpResponseNotFound('Tournament %s not found' % tournament_id)

    return render_to_response(
        'tournament-setup.html',
        {
            'form': form,
            'name': tournament_id
        },
        RequestContext(request)
    )

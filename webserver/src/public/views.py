"""
Basic URL mappings for the webserver
"""

import os
import json
import urllib2

from django.contrib import auth
from django.http import HttpResponseRedirect
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

# pylint: disable=unused-argument
def enter_score(request, tournament_id, username):      # pylint: disable=W0613
    """Enter score for entry"""
    return HttpResponseRedirect('{}/tournament/{}/entry/{}/enterscore'.\
        format(NODE_URL, tournament_id, username))

# pylint: disable=unused-argument
def enter_score_for_game(request, t_id, user):
    """ Enter a score for a single game"""
    return HttpResponseRedirect('{}/tournament/{}/entry/{}/entergamescore'.\
        format(NODE_URL, t_id, user))

# pylint: disable=unused-argument
def entry_list(request, tournament_id):
    """List entrants for a tournament"""
    return HttpResponseRedirect('{}/tournament/{}/entries'.\
        format(NODE_URL, tournament_id))

def logout(request):
    """ logout the user from current request """
    auth.logout(request)
    return HttpResponseRedirect('/')

# pylint: disable=unused-argument
def set_categories(request, tournament_id):
    """Set the scoring categories for a tournament"""
    return HttpResponseRedirect('{}/tournament/{}/categories'.\
        format(NODE_URL, tournament_id))

# pylint: disable=unused-argument
def set_missions(request, tournament_id):
    """Set the number of rounds for a competition"""
    return HttpResponseRedirect('{}/tournament/{}/missions'.\
        format(NODE_URL, tournament_id))

# pylint: disable=unused-argument
def register_for_tournament(request, tournament_id):
    """Page to register for tournament"""
    return HttpResponseRedirect('{}/tournament/{}'.\
        format(NODE_URL, tournament_id))

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

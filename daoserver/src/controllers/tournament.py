"""
All tournament interactions.
"""
import json
from flask import Blueprint, g, request
from sqlalchemy.exc import IntegrityError

from controllers.request_helpers import enforce_request_variables, \
json_response, requires_auth, text_response, ensure_permission
from models.dao.db_connection import db
from models.dao.registration import TournamentRegistration
from models.dao.tournament import Tournament as TournamentDAO
from models.tournament import Tournament

TOURNAMENT = Blueprint('TOURNAMENT', __name__)

@TOURNAMENT.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    if g.tournament_id:
        g.tournament = Tournament(g.tournament_id)

    g.username = values.pop('username', None)

@TOURNAMENT.route('', methods=['POST'])
@requires_auth
@text_response
@enforce_request_variables('inputTournamentName', 'inputTournamentDate')
def add_tournament():
    # pylint: disable=undefined-variable

    """
    POST to add a tournament
    Expects:
        - inputTournamentName - Tournament name. Must be unique.
        - inputTournamentDate - Tournament Date. YYYY-MM-DD
    """
    tourn = Tournament(inputTournamentName)
    tourn.set_date(inputTournamentDate)
    tourn.creator_username = request.authorization.username
    tourn.add_to_db()
    return '<p>Tournament Created! You submitted the following fields:</p> \
        <ul><li>Name: {}</li><li>Date: {}</li></ul>'.\
        format(inputTournamentName, inputTournamentDate)

@TOURNAMENT.route('/<tournament_id>/missions', methods=['GET'])
@json_response
def list_missions():
    """GET list of missions for a tournament."""
    return g.tournament.get_missions()

@TOURNAMENT.route('/<tournament_id>/score_categories', methods=['GET'])
@json_response
def list_score_categories():
    """
    GET the score categories set for the tournament.
    e.g. [{ 'name': 'painting', 'percentage': 20, 'id': 2 }]
    """
    return [{
        'id':             x.id,
        'name':           x.name,
        'percentage':     x.percentage,
        'per_tournament': x.per_tournament,
        'min_val':        x.min_val,
        'max_val':        x.max_val
    } for x in g.tournament.list_score_categories()]

@TOURNAMENT.route('/', methods=['GET'])
@json_response
def list_tournaments():
    """
    GET a list of tournaments
    Returns json. The only key is 'tournaments' and the value is a list of
    tournament names
    """
    # pylint: disable=no-member
    details = [
        {'name': x.name, 'date': x.date, 'rounds': x.num_rounds}
        for x in TournamentDAO.query.all()]

    return {'tournaments' : details}

@TOURNAMENT.route('/<tournament_id>/register/<username>', methods=['POST'])
@requires_auth
@ensure_permission({'permission': 'MODIFY_APPLICATION'})
@text_response
def register():
    """
    POST to apply for entry to a tournament.
    """
    rego = TournamentRegistration(g.username, g.tournament_id)
    rego.clashes()

    try:
        db.session.add(rego)
        db.session.commit()
    except IntegrityError:
        raise ValueError("Check username and tournament")

    g.tournament.confirm_entries()

    return 'Application Submitted'

@TOURNAMENT.route('/<tournament_id>/missions', methods=['POST'])
@text_response
@requires_auth
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
@enforce_request_variables('missions')
def set_missions():
    """POST to set the missions for a tournament. A list of strings expected"""
    # pylint: disable=undefined-variable
    try:
        new_missions = json.loads(missions)
    except TypeError:
        new_missions = missions

    return g.tournament.set_missions(new_missions)

@TOURNAMENT.route('/<tournament_id>/score_categories', methods=['POST'])
@text_response
@requires_auth
@ensure_permission({'permission': 'MODIFY_TOURNAMENT'})
@enforce_request_variables('categories')
def set_score_categories():
    # pylint: disable=undefined-variable

    """
    POST to set tournament categories en masse
    """
    new_categories = []
    try:
        cats = json.loads(categories)
    except TypeError:
        cats = categories

    for json_cat in cats:
        try:
            cat = json.loads(request.values.get(json_cat, []))
        except TypeError:
            cat = request.get_json().get(json_cat)

        new_categories.append({
            'name':       cat[0],
            'percentage': cat[1],
            'per_tourn':  cat[2],
            'min_val':    cat[3],
            'max_val':    cat[4]})

    g.tournament.set_score_categories(new_categories)

    return 'Score categories set: {}'.\
        format(', '.join([str(cat['name']) for cat in new_categories]))

@TOURNAMENT.route('/<tournament_id>', methods=['GET'])
@json_response
def tournament_details():
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    return g.tournament.details()

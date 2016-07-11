"""
All tournament interactions.
"""
import json
import jsonpickle
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from controllers.request_helpers import enforce_request_variables, \
json_response, text_response
from models.dao.db_connection import db
from models.dao.registration import TournamentRegistration
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_round import TournamentRound
from models.tournament import Tournament, ScoreCategoryPair

TOURNAMENT = Blueprint('TOURNAMENT', __name__)

@TOURNAMENT.route('', methods=['POST'])
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
    tourn = Tournament(
        inputTournamentName,
        creator=request.authorization.username)
    tourn.add_to_db(inputTournamentDate)
    return '<p>Tournament Created! You submitted the following fields:</p> \
        <ul><li>Name: {}</li><li>Date: {}</li></ul>'.\
        format(inputTournamentName, inputTournamentDate)

@TOURNAMENT.route('/<tournament_id>/missions', methods=['GET'])
def list_missions(tournament_id):
    """GET list of missions for a tournament."""
    return jsonpickle.encode(
        [x.mission for x in Tournament(tournament_id).get_dao().rounds],
        unpicklable=False)

@TOURNAMENT.route('/<tournament_id>/score_categories', methods=['GET'])
@json_response
def list_score_categories(tournament_id):
    """
    GET the score categories set for the tournament.
    e.g. [{ 'name': 'painting', 'percentage': 20, 'id': 2 }]
    """
    return Tournament(tournament_id).list_score_categories()

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

@TOURNAMENT.route('/<tournament_id>/register', methods=['POST'])
@text_response
@enforce_request_variables('inputUserName')
def register(tournament_id):
    # pylint: disable=undefined-variable

    """
    POST to apply for entry to a tournament.
    Expects:
        - inputUserName - Username of player applying
    """
    rego = TournamentRegistration(inputUserName, tournament_id)
    rego.clashes()

    try:
        db.session.add(rego)
        db.session.commit()
    except IntegrityError:
        raise ValueError("Check username and tournament")

    return 'Application Submitted'

@TOURNAMENT.route('/<tournament_id>/missions', methods=['POST'])
@text_response
@enforce_request_variables('missions')
def set_missions(tournament_id):
    # pylint: disable=undefined-variable

    """POST to set the missions for a tournament.A list of strings expected"""
    tourn = Tournament(tournament_id)
    rounds = tourn.details()['rounds']
    try:
        json_missions = json.loads(missions)
    except TypeError:
        json_missions = missions

    if len(json_missions) != int(rounds):
        raise ValueError('Tournament {} has {} rounds. \
            You submitted missions {}'.format(tournament_id, rounds, missions))

    for i, mission in enumerate(json_missions):
        rnd = tourn.get_round(i + 1)
        # pylint: disable=no-member
        rnd.mission = mission if mission else \
            TournamentRound.__table__.c.mission.default.arg
        db.session.add(rnd)

    db.session.commit()
    return 'Missions set: {}'.format(missions)

@TOURNAMENT.route('/<tournament_id>/score_categories', methods=['POST'])
@text_response
@enforce_request_variables('categories')
def set_score_categories(tournament_id):
    # pylint: disable=undefined-variable

    """
    POST to set tournament categories en masse
    """
    tourn = Tournament(tournament_id)

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

        new_categories.append(
            ScoreCategoryPair(cat[0], cat[1], cat[2], cat[3], cat[4]))

    tourn.set_score_categories(new_categories)

    return 'Score categories set: {}'.\
        format(', '.join([str(cat.display_name) for cat in new_categories]))

@TOURNAMENT.route('/<tournament_id>', methods=['GET'])
@json_response
def tournament_details(tournament_id=None):
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    return Tournament(tournament_id).details()

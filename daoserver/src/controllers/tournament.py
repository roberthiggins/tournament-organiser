"""
All tournament interactions.
"""
import jsonpickle
from flask import Blueprint, request, make_response, Response
from sqlalchemy.exc import IntegrityError

from controllers.request_variables import enforce_request_variables
from models.dao.db_connection import db
from models.dao.registration import TournamentRegistration
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_entry import TournamentEntry
from models.tournament import Tournament

TOURNAMENT = Blueprint('TOURNAMENT', __name__, url_prefix='')


@TOURNAMENT.errorhandler(RuntimeError)
@TOURNAMENT.errorhandler(ValueError)
def input_error(err):
    """Input errors"""
    print type(err).__name__
    print err
    import traceback
    traceback.print_exc()
    return make_response(str(err), 400)

# pylint: disable=undefined-variable
@TOURNAMENT.route('', methods=['POST'])
@enforce_request_variables('inputTournamentName', 'inputTournamentDate')
def add_tournament():
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
    return make_response(
        '<p>Tournament Created! You submitted the following fields:</p> \
        <ul><li>Name: {}</li><li>Date: {}</li></ul>'.format(
            inputTournamentName, inputTournamentDate), 200)

@TOURNAMENT.route('/<tournament_id>/entries', methods=['GET'])
def list_entries(tournament_id):
    """
    Return a list of the entrants for the tournament
    """
    # pylint: disable=no-member
    if not Tournament(tournament_id).exists_in_db:
        return make_response(
            'Tournament {} doesn\'t exist'.format(tournament_id), 404)

    entries = [ent.player_id for ent in \
        TournamentEntry.query.filter_by(tournament_id=tournament_id).all()]
    return Response(jsonpickle.encode(entries, unpicklable=False),
                    mimetype='application/json')

@TOURNAMENT.route('/<tournament_id>/missions', methods=['GET'])
def list_missions(tournament_id):
    """GET list of missions for a tournament."""
    return jsonpickle.encode(
        [x.mission for x in Tournament(tournament_id).get_dao().rounds],
        unpicklable=False)

@TOURNAMENT.route('/', methods=['GET'])
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

    return Response(
        jsonpickle.encode({'tournaments' : details}, unpicklable=False),
        mimetype='application/json')

# pylint: disable=undefined-variable
@TOURNAMENT.route('/<tournament_id>/register', methods=['POST'])
@enforce_request_variables('inputUserName')
def register(tournament_id):
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

    return make_response('Application Submitted', 200)

@TOURNAMENT.route('/<tournament_id>', methods=['GET'])
def tournament_details(tournament_id=None):
    """
    GET to get details about a tournament. This includes entrants and format
    information
    """
    tourn = Tournament(tournament_id)
    return Response(
        jsonpickle.encode(tourn.details(), unpicklable=False),
        mimetype='application/json')

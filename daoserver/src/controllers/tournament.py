"""
All tournament interactions.
"""
import json
import jsonpickle
from flask import Blueprint, request, make_response, Response
from sqlalchemy.exc import IntegrityError

from controllers.request_variables import enforce_request_variables
from models.dao.db_connection import db
from models.dao.registration import TournamentRegistration
from models.dao.tournament import Tournament as TournamentDAO
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament_round import TournamentRound
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

@TOURNAMENT.route('', methods=['POST'])
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
    return make_response(
        '<p>Tournament Created! You submitted the following fields:</p> \
        <ul><li>Name: {}</li><li>Date: {}</li></ul>'.format(
            inputTournamentName, inputTournamentDate), 200)

@TOURNAMENT.route('/<tournament_id>/rounds/<round_id>', methods=['GET'])
def get_round_info(tournament_id, round_id):
    """
    GET the information about a round
    """
    tourn = Tournament(tournament_id)
    rnd = tourn.get_round(round_id)
    draw = tourn.make_draw(round_id)

    draw_info = [
        {'table_number': t.table_number,
         'entrants': [x if isinstance(x, str) else x.player_id \
                      for x in t.entrants]
        } for t in draw]

    # We will return all round info for all requests regardless of method
    return jsonpickle.encode(
        {
            'draw': draw_info,
            'mission': rnd.mission
        },
        unpicklable=False)

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

@TOURNAMENT.route('/<tournament_id>/register', methods=['POST'])
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

    return make_response('Application Submitted', 200)

@TOURNAMENT.route('/<tournament_id>/missions', methods=['POST'])
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
    return make_response('Missions set: {}'.format(missions), 200)

@TOURNAMENT.route('/<tournament_id>/rounds', methods=['POST'])
@enforce_request_variables('numRounds')
def set_rounds(tournament_id):
    """Set the number of rounds for a tournament"""

    # pylint: disable=undefined-variable
    rounds = int(numRounds)
    if rounds < 1:
        raise ValueError('Set at least 1 round')
    Tournament(tournament_id).set_number_of_rounds(rounds)
    return make_response('Rounds set: {}'.format(rounds), 200)

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

"""
Controller for entries in tournaments
"""
from decimal import Decimal as Dec
from flask import Blueprint, g

from controllers.request_helpers import json_response, \
enforce_request_variables, text_response
from models.dao.account import Account
from models.dao.tournament_entry import TournamentEntry
from models.permissions import PERMISSIONS, PermissionsChecker
from models.score import is_score_entered
from models.tournament import Tournament

ENTRY = Blueprint('ENTRY', __name__)

@ENTRY.url_value_preprocessor
# pylint: disable=unused-argument
def get_tournament(endpoint, values):
    """Retrieve tournament_id from URL and ensure the tournament exists"""
    g.tournament_id = values.pop('tournament_id', None)
    g.tournament = Tournament(g.tournament_id)
    if not g.tournament.exists_in_db:
        raise ValueError('Tournament {} doesn\'t exist'.format(g.tournament_id))

    g.username = values.pop('username', None)
    if g.username:
        entry_id = get_entry_id(g.tournament_id, g.username)
        # pylint: disable=no-member
        g.entry = TournamentEntry.query.filter_by(id=entry_id).first()


@ENTRY.route('/', methods=['GET'])
@json_response
def list_entries():
    """
    Return a list of the entrants for the tournament
    """
    # pylint: disable=no-member
    return [ent.player_id for ent in \
        TournamentEntry.query.filter_by(tournament_id=g.tournament_id).all()]

def get_entry_id(tournament_id, username):
    """Get entry info from tournament and username"""
    if not Account.username_exists(username):
        raise ValueError('Unknown player: {}'.format(username))

    try:
        # pylint: disable=no-member
        return TournamentEntry.query.\
            filter_by(tournament_id=tournament_id, player_id=username).\
            first().id
    except AttributeError:
        raise ValueError('Entry for {} in tournament {} not found'.\
            format(username, tournament_id))


@ENTRY.route('/<username>/entergamescore', methods=['POST'])
@text_response
@enforce_request_variables('scorer', 'key', 'value', 'game_id')
def enter_game_score():
    """
    POST to enter a score for a player in a game.

    Expects:
        - game_id - The id of the game that the score is for
        - scorer - username of the user entering the escore
        - key - the category e.g. painting, round_6_battle
        - value - the score. Integer
    """
    checker = PermissionsChecker()
    # pylint: disable=undefined-variable
    if not checker.check_permission(
            PERMISSIONS.get('ENTER_SCORE'),
            scorer,
            g.username,
            g.tournament_id):
        raise ValueError('Permission denied. {}'.\
            format('You cannot enter scores for this game. Contact the TO.'))

    if not g.entry:
        raise ValueError('Unknown player: {}'.format(g.username))

    # pylint: disable=undefined-variable
    g.tournament.enter_score(g.entry.id, key, value, game_id)
    return 'Score entered for {}: {}'.format(g.username, value)

@ENTRY.route('/<username>/entertournamentscore', methods=['POST'])
@text_response
@enforce_request_variables('scorer', 'key', 'value')
def enter_tournament_score():
    """
    POST to enter a score for a player in a tournament.

    Expects:
        - scorer - username of the user entering the escore
        - key - the category e.g. painting, round_6_battle
        - value - the score. Integer
    """
    checker = PermissionsChecker()
    # pylint: disable=undefined-variable
    if not checker.check_permission(
            PERMISSIONS.get('ENTER_SCORE'),
            scorer,
            g.username,
            g.tournament_id):
        raise ValueError('Permission denied. {}'.\
            format('You cannot enter scores for this game. Contact the TO.'))

    if not g.entry:
        raise ValueError('Unknown player: {}'.format(g.username))

    # pylint: disable=undefined-variable
    g.tournament.enter_score(g.entry.id, key, value)
    return 'Score entered for {}: {}'.format(g.username, value)


@ENTRY.route('/<username>', methods=['GET'])
@json_response
def entry_info_from_tournament():
    """ Given entry_id, get info about player and tournament"""

    try:
        return {
            'entry_id': g.entry.id,
            'username': g.entry.account.username,
            'tournament_name': g.entry.tournament.name,
        }
    except AttributeError:
        raise ValueError('Entry not valid: {}'.format(g.username))

def get_opponent(game, entry):
    """Work out the opponent of username in the game"""
    entrants = [x.entrant.player_id for x in game.entrants \
                if x.entrant.player_id != entry.player_id]
    return entrants[0] if len(entrants) else "BYE"

@ENTRY.route('/<username>/nextgame', methods=['GET'])
@json_response
def get_next_game():
    """Get the next game for given entry"""

    games = [gent.game for gent in g.entry.game_entries]
    games = sorted(games, key=lambda game: game.tournament_round.ordering)

    for game in games:
        if not is_score_entered(game):
            return {
                'game_id': game.id,
                'mission': game.tournament_round.mission,
                'round': game.tournament_round.ordering,
                'opponent': get_opponent(game, g.entry),
                'table': game.table_num,
            }
    raise ValueError("Next game not scheduled. Check with the TO.")

@ENTRY.route('/<username>/schedule', methods=['GET'])
@json_response
def get_schedule():
    """Get the scheule of games for username's entry"""
    games = [gent.game for gent in g.entry.game_entries]

    return [
        {
            'game_id': game.id,
            'round': game.tournament_round.ordering,
            'opponent': get_opponent(game, g.entry),
            'table': game.table_num,
        } for game in games]

@ENTRY.route('/rank', methods=['GET'])
@json_response
def rank_entries():
    """
    Rank all the entries in a tournament based on the scoring criteria for the
    tournament.
    The structure of the returned JSON blob will be as follows:
    [
        {
            'username': 'homer',
            'entry_id': 1,
            'tournament_id': 'some_tournie',
            'scores': {'round_1': 10, 'round_2': 4 },
            'total_score': 23.50, # always 2dp
            'ranking': 3
        },
    ]
    """

    # pylint: disable=line-too-long
    return [
        {
            'username' : x.player_id,
            'entry_id' : x.id,
            'tournament_id' : g.tournament_id,
            'scores' : x.score_info,
            'total_score' : str(Dec(x.total_score).quantize(Dec('1.00'))),
            'ranking': x.ranking
        } for x in \
        g.tournament.ranking_strategy.overall_ranking(g.tournament.entries())
    ]

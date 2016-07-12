"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

from flask import Blueprint, request

from controllers.request_helpers import enforce_request_variables, text_response
from models.dao.account import Account
from models.dao.tournament_entry import TournamentEntry
from models.permissions import PERMISSIONS, PermissionsChecker
from models.tournament import Tournament

APP = Blueprint('APP', __name__, url_prefix='')

@APP.route("/")
@text_response
def main():
    """Index page. Used to verify the server is running."""
    return 'daoserver'

# Page actions
@APP.route('/entertournamentscore', methods=['POST'])
@text_response
@enforce_request_variables('username', 'tournament', 'key', 'value')
def enter_tournament_score():
    """
    POST to enter a score for a player in a tournament.

    Expects:
        - username - the player_id
        - tournament - the tournament_id
        - key - the category e.g. painting, round_6_battle
        - value - the score. Integer
    """
    checker = PermissionsChecker()
    # pylint: disable=undefined-variable
    if request.authorization is None or not checker.check_permission(
            PERMISSIONS.get('ENTER_SCORE'),
            request.authorization.username,
            username,
            tournament):
        raise ValueError('Permission denied. {}'.\
            format('You cannot enter scores for this game. Contact the TO.'))

    # pylint: disable=E0602
    tourn = Tournament(tournament)
    if not tourn.exists_in_db:
        raise ValueError('Unknown tournament: {}'.format(tournament))

    if not Account.username_exists(username):
        raise ValueError('Unknown player: {}'.format(username))

    # pylint: disable=E0602,no-member
    entry_id = TournamentEntry.query.\
            filter_by(tournament_id=tournament, player_id=username).first().id

    # pylint: disable=E0602
    tourn.enter_score(entry_id, key, value)
    return 'Score entered for {}: {}'.format(username, value)

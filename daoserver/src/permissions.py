"""
Module to handle permissions for accounts trying to modify a tournament.
"""

from db_connections.db_connection import db_conn
from db_connections.entry_db import EntryDBConnection

PERMISSIONS = {
    'ENTER_SCORE': 'enter_score',
}

def check_action_valid(action):
    """Only actions found in PERMISSIONS are allowed"""
    if action is None or not action in PERMISSIONS.values():
        raise ValueError(
            'Illegal action passed to check_permission {}'.format(action))

# pylint: disable=E0602
class PermissionsChecker(object):
    """
    Organisers and admins can add/remove players.
    Players in relevant game, admins, and organisers of relevant tournament can
    add scores.
    Organisers and admins can modify scores.
    Etc.
    """

    def __init__(self):
        self.entry_db = EntryDBConnection()

    @db_conn(commit=True)
    def add_permission(self, user, action, protected_obj_id):
        """
        Give user permission to perform action on protected_obj

        Assumptions:
            action must be a permissions.PERMISSIONS
            protected_obj should be a protected_object id

        e.g. - to_of_southcon, enter_score, southcon
             - player_of_game_3, enter_score, game_3
        """
        check_action_valid(action)

        cur.execute(
            "SELECT id FROM protected_object_action \
            WHERE description = %s LIMIT 1",
            [action])
        action_id = cur.fetchone()[0]

        try:
            cur.execute(
                "SELECT id FROM protected_object_permission \
                WHERE protected_object_id = %s \
                AND protected_object_action_id = %s",
                [protected_obj_id, action_id])
            permission_id = cur.fetchone()[0]
        except TypeError:
            cur.execute(
                "INSERT INTO protected_object_permission \
                VALUES (DEFAULT, %s, %s) RETURNING id",
                [protected_obj_id, action_id])
            permission_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO account_protected_object_permission VALUES (%s, %s)",
            [user, permission_id])

    def check_permission(self, action, user, tournament, game_id=None):
        """
        Entry point method for checking permissions.
        Check that a user is entitled to perform action for tournament
        """

        check_action_valid(action)

        if action == PERMISSIONS['ENTER_SCORE']:
            return self.is_admin(user) or self.is_organiser(user, tournament) \
                or self.is_player(user, tournament, game_id)

        return False

    @db_conn()
    def is_admin(self, user):
        """User is superuser"""
        if user is None:
            return False

        cur.execute(
            "SELECT count(*) > 0 FROM account \
            WHERE username = %s AND is_superuser = TRUE",
            [user])
        return cur.fetchone()[0]

    @db_conn()
    def is_organiser(self, user, tournament):
        """user is an organiser of tournament"""
        cur.execute(
            "SELECT count(*) > 0 FROM tournament_organiser_permissions \
            WHERE tournament_name = %s AND username = %s",
            [tournament, user])
        return cur.fetchone()[0]

    @db_conn()
    def is_player(self, user, tournament, game_id=None):
        """user is a player in game."""
        try:
            entry_id = self.entry_db.entry_id(tournament, user)
        except TypeError:
            return False # The user is not entered into anything

        # Eventually this will be expanded to be any player in a tournament
        if game_id is None:
            return False

        cur.execute(
            "SELECT count(*) > 0 FROM game_permissions \
            WHERE game_id = %s AND entry_id = %s",
            [game_id, entry_id])
        return cur.fetchone()[0]

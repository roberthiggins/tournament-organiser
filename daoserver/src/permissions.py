"""
Module to handle permissions for accounts trying to modify a tournament.
"""

from db_connection import db_conn

PERMISSIONS = {
    'ENTER_SCORE': 'enter_score',
}

def check_action_valid(action):
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

    def check_permission(self, action, user, tournament):
        """
        Entry point method for checking permissions.
        Check that a user is entitled to perform action for tournament
        """

        check_action_valid(action)

        if action == PERMISSIONS['ENTER_SCORE']:
            return self.is_admin(user) or self.is_organiser(user, tournament)

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

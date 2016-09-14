"""
Module to handle permissions for accounts trying to modify a tournament.
"""
# pylint: disable=no-member

from sqlalchemy.sql.expression import and_

from models.authentication import PermissionDeniedException
from models.dao.db_connection import db
from models.dao.account import Account
from models.dao.permissions import AccountProtectedObjectPermission, \
ProtObjAction, ProtObjPerm, ProtectedObject
from models.dao.tournament_entry import TournamentEntry
from models.dao.tournament import Tournament

PERMISSIONS = {
    'ENTER_SCORE'       : 'enter_score',
    'MODIFY_TOURNAMENT' : 'modify_tournament'
}

def set_up_permissions(commit=False):
    """
    Add all the permissions listed in PERMISSIONS to the db
    These are all the action you can take.
    """
    # pylint: disable=unused-variable
    for key, value in PERMISSIONS.iteritems():
        if ProtObjAction.query.filter_by(description=value).first() is None:
            db.session.add(ProtObjAction(value))
    db.session.flush()
    if commit:
        db.session.commit()

# pylint: disable=E0602
class PermissionsChecker(object):
    """
    Organisers and admins can add/remove players.
    Players in relevant game, admins, and organisers of relevant tournament can
    add scores.
    Organisers and admins can modify scores.
    Etc.
    """


    @staticmethod
    def check_action_valid(action):
        """Only actions found in PERMISSIONS are allowed"""
        if action is None or action not in PERMISSIONS.values():
            raise ValueError(
                'Illegal action passed to check_permission {}'.format(action))

    def add_permission(self, user, action, prot_obj):
        """
        Give user permission to perform action on protected_obj

        Assumptions:
            action must be a permissions.PERMISSIONS
            protected_obj should be a protected_object id

        e.g. - to_of_southcon, enter_score, southcon
             - player_of_game_3, enter_score, game_3
        """
        self.check_action_valid(action)

        act_id = ProtObjAction.query.filter_by(description=action).first().id

        permission = ProtObjPerm.query.filter(
            and_(
                ProtObjPerm.protected_object_id == prot_obj.id,
                ProtObjPerm.protected_object_action_id == act_id)
            ).first()

        if permission is None:
            permission = ProtObjPerm(prot_obj.id, act_id)
            db.session.add(permission)
            db.session.flush()

        db.session.add(AccountProtectedObjectPermission(user, permission.id))
        db.session.commit()

    def check_permission(self, action, user, for_user, tournament):
        """
        Entry point method for checking permissions.
        Check that a user is entitled to perform action for tournament
        """

        self.check_action_valid(action)

        perm_denied = PermissionDeniedException(
            'Permission denied for {} to perform {} on tournament {}'.\
            format(user, action, tournament))

        if action == PERMISSIONS['ENTER_SCORE']:
            if Account.query.filter_by(username=user, is_superuser=True).\
                first() is not None or self.is_organiser(user, tournament):
                return True
            if user != for_user:
                raise perm_denied

            if TournamentEntry.query.\
                    filter_by(tournament_id=tournament, player_id=user).first()\
                    is not None:
                return True
        elif action == PERMISSIONS['MODIFY_TOURNAMENT']:
            if Account.query.filter_by(username=user, is_superuser=True).\
                first() is not None or self.is_organiser(user, tournament):
                return True

        raise perm_denied

    def remove_permission(self, user, action, prot_obj):
        """
        Remove user permission to perform action on protected_obj

        Assumptions:
            action must be a permissions.PERMISSIONS
            protected_obj should be a protected_object id

        e.g. - player_of_game_3, enter_score, game_3
        """
        self.check_action_valid(action)

        act_id = ProtObjAction.query.filter_by(description=action).first().id

        permission_id = ProtObjPerm.query.\
            filter_by(protected_object_id=prot_obj.id,
                      protected_object_action_id=act_id).first().id

        AccountProtectedObjectPermission.query.\
            filter_by(account_username=user,
                      protected_object_permission_id=permission_id).delete()

        db.session.commit()

    def is_organiser(self, user, tournament):
        """user is an organiser of tournament"""
        return Tournament.query.join(ProtectedObject).join(ProtObjPerm).\
            join(AccountProtectedObjectPermission).\
            filter(and_(
                Tournament.name == tournament,
                AccountProtectedObjectPermission.account_username == user
            )).count() > 0

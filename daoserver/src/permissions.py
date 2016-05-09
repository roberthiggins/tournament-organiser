"""
Module to handle permissions for accounts trying to modify a tournament.
"""
# pylint: disable=invalid-name,no-member

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import and_

from db_connections.db_connection import db_conn
from models.account import Account
from models.permissions import ProtectedObject
from models.tournament_entry import TournamentEntry

PERMISSIONS = {
    'ENTER_SCORE': 'enter_score',
}

db = SQLAlchemy()

def check_action_valid(action):
    """Only actions found in PERMISSIONS are allowed"""
    if action is None or action not in PERMISSIONS.values():
        raise ValueError(
            'Illegal action passed to check_permission {}'.format(action))

# pylint: disable=no-init
class ProtObjAction(db.Model):
    """An action you can perform on a protected object, e.g. enter score"""
    __tablename__ = 'protected_object_action'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<ProtObjAction ({}, {})>'.format(
            self.id,
            self.description)

# pylint: disable=no-init
class ProtObjPerm(db.Model):
    """
    Gain a permission to do a something ProtObjAction on a protected
    object
    """
    __tablename__ = 'protected_object_permission'
    id = db.Column(db.Integer, primary_key=True)
    protected_object_id = db.Column(
        db.Integer,
        db.ForeignKey(ProtectedObject.id),
        nullable=False)
    protected_object_action_id = db.Column(
        db.Integer,
        db.ForeignKey(ProtObjAction.id),
        nullable=False)

    def __init__(self, prot_obj_id, action_id):
        self.protected_object_id = prot_obj_id
        self.protected_object_action_id = action_id

    def __repr__(self):
        return '<ProtObjPerm ({}, {}, {})>'.format(
            self.id,
            self.protected_object_id,
            self.protected_object_action_id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


# pylint: disable=E0602
class PermissionsChecker(object):
    """
    Organisers and admins can add/remove players.
    Players in relevant game, admins, and organisers of relevant tournament can
    add scores.
    Organisers and admins can modify scores.
    Etc.
    """

    @db_conn(commit=True)
    # pylint: disable=no-member
    def add_permission(self, user, action, prot_obj_id):
        """
        Give user permission to perform action on protected_obj

        Assumptions:
            action must be a permissions.PERMISSIONS
            protected_obj should be a protected_object id

        e.g. - to_of_southcon, enter_score, southcon
             - player_of_game_3, enter_score, game_3
        """
        check_action_valid(action)

        act_id = ProtObjAction.query.filter_by(description=action).first().id

        try:
            permission_id = ProtObjPerm.query.filter(
                and_(
                    ProtObjPerm.protected_object_id == prot_obj_id,
                    ProtObjPerm.protected_object_action_id == act_id)
                ).first().id
        except AttributeError:
            permission = ProtObjPerm(prot_obj_id, act_id)
            permission.write()
            permission_id = permission.id

        cur.execute(
            "INSERT INTO account_protected_object_permission VALUES (%s, %s)",
            [user, permission_id])

    def check_permission(self, action, user, for_user, tournament):
        """
        Entry point method for checking permissions.
        Check that a user is entitled to perform action for tournament
        """

        check_action_valid(action)

        if action == PERMISSIONS['ENTER_SCORE']:
            if self.is_admin(user) or self.is_organiser(user, tournament):
                return True
            if user != for_user:
                return False
            return self.is_tournament_player(user, tournament)

        return False

    def is_admin(self, user):
        """User is superuser"""
        if user is None:
            return False

        return Account.query.filter_by(username=user, is_superuser=True).\
            first() is not None

    @db_conn()
    def is_organiser(self, user, tournament):
        """user is an organiser of tournament"""
        cur.execute(
            "SELECT count(*) > 0 FROM tournament_organiser_permissions \
            WHERE tournament_name = %s AND username = %s",
            [tournament, user])
        return cur.fetchone()[0]

    def is_tournament_player(self, user, tournament):
        """User playing in tournament."""

        if not Account.username_exists(user):
            raise ValueError('Unknown player: {}'.format(user))

        return TournamentEntry.query.\
            filter_by(tournament_id=tournament, player_id=user).first() \
            is not None


    @db_conn()
    def is_game_player(self, user, game_id):
        """user is a player in game."""

        try:
            cur.execute(
                "SELECT count(*) > 0 FROM game_permissions \
                WHERE game_id = %s AND username = %s",
                [game_id, user])
            return cur.fetchone()[0]
        except ValueError:
            return False

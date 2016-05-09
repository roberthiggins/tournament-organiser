"""
ORM module for permissions
"""
# pylint: disable=invalid-name

from models.account import Account
from models.db_connection import db

class ProtectedObject(db.Model):
    """
    A ProtectedObject is an object that can have access to it restricted by
    permissions
    """
    __tablename__ = 'protected_object'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<ProtectedObject {}>'.format(self.id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

class ProtObjAction(db.Model):
    """An action you can perform on a protected object, e.g. enter score"""
    __tablename__ = 'protected_object_action'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<ProtObjAction ({}, {})>'.format(
            self.id,
            self.description)

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

class AccountProtectedObjectPermission(db.Model):
    """ Join table for account and protected_object_permission"""
    __tablename__ = 'account_protected_object_permission'
    account_username = db.Column(db.String(50),
                                 db.ForeignKey(Account.username),
                                 primary_key=True)
    protected_object_permission_id = db.Column(db.Integer(),
                                               db.ForeignKey(ProtObjPerm.id),
                                               primary_key=True)
    def __init__(self, username, perm_id):
        self.account_username = username
        self.protected_object_permission_id = perm_id

    def __repr__(self):
        return '<AccountProtectedObjectPermission ({}, {})>'.format(
            self.account_username,
            self.protected_object_permission_id)

    def write(self):
        """To the DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

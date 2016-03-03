"""
ORM module for protected_object table
"""
# pylint: disable=invalid-name

from models.db_connection import db

# pylint: disable=no-init
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

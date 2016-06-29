"""
ORM module for a table, allocated to some players
"""

# pylint: disable=invalid-name

from models.dao.db_connection import db
from models.dao.tournament_entry import TournamentEntry

class TableAllocation(db.Model):
    """ Entries need a place to play their games."""

    __tablename__ = 'table_allocation'
    entry_id = db.Column(db.Integer,
                         db.ForeignKey(TournamentEntry.id),
                         primary_key=True)
    table_no = db.Column(db.Integer, nullable=False)
    round_no = db.Column(db.Integer, primary_key=True)

    def __init__(self, entry_id, table_no, round_no):
        self.entry_id = entry_id
        self.table_no = table_no
        self.round_no = round_no

    def __repr__(self):
        return '<TableAllocation ({}, {}, {})>'.format(
            self.entry_id,
            self.table_no,
            self.round_no)

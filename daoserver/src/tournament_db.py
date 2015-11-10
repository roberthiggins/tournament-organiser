"""
This file contains code to connect to the tournament_db
"""

import psycopg2

from db_connection import DBConnection

class TournamentDBConnection(object):
    """
    Connection class to the tournament database
    """
    def __init__(self):
        self.db_conn = DBConnection()
        self.con = self.db_conn.con


    def tournament_exists(self, name):
        """Check if a tournament exists with the passed name"""
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM tournament WHERE name = %s",
                        [name])
            existing = cur.fetchone()
            return existing[0] > 0
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

    def add_tournament(self, tournament):
        """
        Add a tournament.
        Expects:
            - tournament - dict {
                            'name' - unique name,
                            'date' - YY-MM-DD}
        """
        try:
            cur = self.con.cursor()
            cur.execute(
                "INSERT INTO tournament VALUES (default, %s, %s)",
                [tournament['name'], tournament['date']])
            self.con.commit()

        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            raise err

    def list_tournaments(self):
        """Get a list of tournaments"""
        try:
            cur = self.con.cursor()
            cur.execute("SELECT name FROM tournament")
            return [x[0] for x in cur.fetchall()]
        except psycopg2.DatabaseError as err:
            print 'Database Error %s' % err
            raise err

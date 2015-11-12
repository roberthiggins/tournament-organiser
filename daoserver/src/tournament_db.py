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

    def enter_game_score(self, tournament, round_num, scores):
        """
        Enters a score for a game into tournament for all entries involved

        Expects: All fields required

        Assumption: That the entries in scores exist
        """
        if not tournament or not round_num or len(scores) < 2:
            raise RuntimeError('Enter the required fields')

        if not self.tournament_exists(tournament):
            raise RuntimeError('Unknown tournament: ' + tournament)

        raise NotImplementedError("enter game score not implemented")

    def enter_score(self, tournament_id, player_id, category, score):
        """
        Enters a score for category into tournament for player

        Expects: All fields required

        Assumption: That the player exists
        """
        if not player_id or not tournament_id or not category or not score:
            raise RuntimeError('Enter the required fields')

        if not self.tournament_exists(tournament_id):
            raise RuntimeError('Unknown tournament: ' + tournament_id)

        raise NotImplementedError("enter score not implemented")

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

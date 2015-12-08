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

    def create_score_category(self, category, tournament_id, percentage):
        """
        Create a score category for a tournament.
        Expects:
            category - A human-readable name for the category
            tournament_id - the tournament the category will be used for
            pecentage - The percentage of the total score taken up by scores
                in this category. For example, if you wanted battle to be 60
                percent of the total tournament score, percentage would be 60
        """
        try:
            percentage = int(percentage)
        except ValueError:
            raise ValueError('percentage must be an integer')

        try:
            cur = self.con.cursor()

            cur.execute(
                "SELECT SUM(percentage) FROM score_category \
                WHERE tournament_id = %s", [tournament_id])
            existing = cur.fetchone()
            existing_total = existing[0] if existing[0] is not None else 0
            if (existing_total + percentage) > 100:
                raise ValueError('percentage too high: {}'.format(category))

            cur.execute(
                "INSERT INTO score_category VALUES(DEFAULT, %s, %s, %s)",
                [tournament_id, category, percentage]
            )
            self.con.commit()

        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            raise err

    def list_score_categories(self, tournament_id):
        """
        Get score_categories associated with a tournament.
        e.g. [{ 'name': 'painting', 'percentage': 20 }]
        """
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT id, display_name, percentage FROM score_category \
                WHERE tournament_id = %s", [tournament_id])
            raw_list = cur.fetchall()
            return [{'id': x[0],
                    'name': x[1],
                    'percentage': x[2]} for x in raw_list]
        except psycopg2.DatabaseError as err:
            print 'Database Error %s' % err
            raise err

    def list_tournaments(self):
        """Get a list of tournaments"""
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT name, date, num_rounds, score_id FROM tournament")
            raw_list = cur.fetchall()

            return [{'name': x[0],
                    'date': x[1],
                    'rounds': x[2],
                    'scoring': x[3]} for x in raw_list]
        except psycopg2.DatabaseError as err:
            print 'Database Error %s' % err
            raise err

    def tournament_details(self, name):
        """
        Get information about a tournament.
        Returns none if tournie non-existent
        """
        if not self.tournament_exists(name):
            raise RuntimeError('No information is available on "%s" ' % name)

        try:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM tournament WHERE name = %s",
                [name])
            return cur.fetchone()

        except psycopg2.DatabaseError as err:
            print 'Database Error %s' % err
            raise err

    def set_score_key(self, t_id, key, category, min_val, max_val):
        """
        Create a score that entries can get in the tournament. This should be
        called for all scores you want, e.g. round_1_battle, round_2_battle

        Expects:
            - a varchar candidate. The key will need to be unique and should
            be a varchar.
            - min_val. Integer. nin val for the score. Default 0
            - max_val. Integer. max val for the score. Default 20

        Returns: throws ValueError and psycopg2.DatabaseError as appropriate
        """
        if not t_id or not key:
            raise ValueError('Arguments missing from set_score_category call')
        try:
            min_val = int(min_val)
        except ValueError:
            raise ValueError('Minimum Score must be an integer')

        try:
            max_val = int(max_val)
        except ValueError:
            raise ValueError('Maximum Score must be an integer')

        try:
            cur = self.con.cursor()
            cur.execute(
                "INSERT INTO score_key VALUES(default, %s, %s, %s, %s, %s)",
                [key, t_id, max_val, min_val, category])
            self.con.commit()

        except psycopg2.IntegrityError:
            self.con.rollback()
            raise RuntimeError('Score already set')
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            raise RuntimeError(err)

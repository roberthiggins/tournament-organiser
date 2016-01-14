"""
This file contains code to connect to the tournament_db
"""

import psycopg2

from db_connection import db_conn

# pylint: disable=E0602,R0201
class TournamentDBConnection(object):
    """
    Connection class to the tournament database
    """
    @db_conn()
    def get_mission(self, tournament, round_id):
        """Get mission for given round"""
        cur.execute("SELECT mission FROM tournament_round \
                    WHERE tournament_name = %s AND ordering = %s",
                    [tournament, round_id])
        return cur.fetchone()[0]

    @db_conn()
    def get_missions(self, tournament):
        """Get mission for given round"""
        cur.execute("SELECT mission FROM tournament_round \
                    WHERE tournament_name = %s",
                    [tournament])
        return [x[0] for x in cur.fetchall()]

    @db_conn(commit=True)
    def set_mission(self, tournament, round_id, mission):
        """Set mission for given round"""
        cur.execute("SELECT COUNT(*) > 0 FROM tournament_round \
                    WHERE tournament_name = %s AND ordering = %s",
                    [tournament, round_id])
        if cur.fetchone()[0]:
            cur.execute("UPDATE tournament_round SET mission = %s \
                        WHERE tournament_name = %s AND ordering = %s",
                        [mission, tournament, round_id])
        else:
            cur.execute("INSERT INTO tournament_round \
                        VALUES(DEFAULT, %s, %s, %s)",
                        [tournament, round_id, mission])

    @db_conn()
    def tournament_exists(self, name):
        """Check if a tournament exists with the passed name"""
        cur.execute("SELECT COUNT(*) > 0 FROM tournament WHERE name = %s",
                    [name])
        return cur.fetchone()[0]

    @db_conn(commit=True)
    def add_tournament(self, tournament):
        """
        Add a tournament.
        Expects:
            - tournament - dict {
                            'name' - unique name,
                            'date' - YY-MM-DD}
        """
        cur.execute(
            "INSERT INTO tournament VALUES (default, %s, %s)",
            [tournament['name'], tournament['date']])

    @db_conn(commit=True)
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

    @db_conn()
    def list_score_categories(self, tournament_id):
        """
        Get score_categories associated with a tournament.
        e.g. [{ 'name': 'painting', 'percentage': 20 }]
        """
        cur.execute(
            "SELECT id, display_name, percentage FROM score_category \
            WHERE tournament_id = %s", [tournament_id])
        raw_list = cur.fetchall()
        return [{'id': x[0],
                 'name': x[1],
                 'percentage': x[2]} for x in raw_list]

    @db_conn()
    def list_tournaments(self):
        """Get a list of tournaments"""
        cur.execute(
            "SELECT name, date, num_rounds, score_id FROM tournament")
        raw_list = cur.fetchall()

        return [{'name': x[0],
                 'date': x[1],
                 'rounds': x[2],
                 'scoring': x[3]} for x in raw_list]

    @db_conn(commit=True)
    def set_rounds(self, tournament_id, num_rounds):
        """Set the number of rounds for a tournament"""
        cur.execute(
            "UPDATE tournament SET num_rounds = %s WHERE name = %s",
            [num_rounds, tournament_id])
        cur.execute("DELETE FROM tournament_round \
                    WHERE tournament_name = %s AND ordering > %s",
                    [tournament_id, num_rounds])

    @db_conn()
    def tournament_details(self, name):
        """
        Get information about a tournament.
        Returns none if tournie non-existent
        """
        if not self.tournament_exists(name):
            raise RuntimeError('No information is available on "%s" ' % name)

        cur.execute("SELECT * FROM tournament WHERE name = %s", [name])
        return cur.fetchone()

    @db_conn(commit=True)
    def set_score_key(self, key, category, min_val, max_val):
        """
        Create a score that entries can get in the tournament. This should be
        called for all scores you want, e.g. round_1_battle, round_2_battle

        Expects:
            - a varchar candidate. The key will need to be unique and should
            be a varchar.
            - category - the score_category id
            - min_val. Integer. nin val for the score. Default 0
            - max_val. Integer. max val for the score. Default 20

        Returns: throws ValueError and psycopg2.DatabaseError as appropriate
        """
        if not category or not key:
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
            cur.execute(
                "INSERT INTO score_key VALUES(default, %s, %s, %s, %s)",
                [key, max_val, min_val, category])

        except psycopg2.IntegrityError:
            raise psycopg2.DatabaseError('Score already set')

    @db_conn()
    def get_score_keys_for_round(self, tournament_id, round_id):
        """
        Get all the score keys, and the information from their rows, for a
        particular round
        """
        try:
            round_id = int(round_id)
        except ValueError:
            raise ValueError('Round ID must be an integer')

        cur.execute(
            "SELECT COUNT(*) FROM tournament_round \
            WHERE tournament_name = %s AND id = %s",
            [tournament_id, round_id]
        )
        if cur.fetchone()[0] == 0:
            raise ValueError("Round {} doesn't exist in {}".format(
                round_id, tournament_id))
        cur.execute(
            "SELECT * FROM score_key k \
            INNER JOIN round_score s ON s.score_key_id = k.id \
            WHERE s.round_id = %s", [round_id])
        return cur.fetchall()

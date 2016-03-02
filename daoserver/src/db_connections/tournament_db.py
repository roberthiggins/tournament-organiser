"""
This file contains code to connect to the tournament_db
"""

import psycopg2

from db_connections.db_connection import db_conn

# pylint: disable=E0602,R0201
class TournamentDBConnection(object):
    """
    Connection class to the tournament database
    """
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
            WHERE tournament_name = %s AND ordering = %s",
            [tournament_id, round_id]
        )

        # It may be that the mission has not been set for that round.
        if cur.fetchone()[0] == 0:
            raise ValueError("Draw not ready. Mission not set. Contact TO")
        cur.execute(
            "SELECT * FROM score_key k \
            INNER JOIN round_score s ON s.score_key_id = k.id \
            WHERE s.round_id = %s", [round_id])
        return cur.fetchall()

    @db_conn(commit=True)
    def set_score_key_for_round(self, score_key_id, round_id):
        """
        Attach the score_key to the round. Will then be accessible through
        get_score_keys_for_round
        """
        cur.execute("INSERT INTO round_score VALUES( %s, %s)",
                    [score_key_id, round_id])


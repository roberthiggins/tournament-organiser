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
    @db_conn(commit=True)
    def set_score_key_for_round(self, score_key_id, round_id):
        """
        Attach the score_key to the round. Will then be accessible through
        get_score_keys_for_round
        """
        cur.execute("INSERT INTO round_score VALUES( %s, %s)",
                    [score_key_id, round_id])


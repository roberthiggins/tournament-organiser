"""
This file contains code to connect to the entry_db
"""

from flask import json
from psycopg2.extras import DictCursor

from db_connections.db_connection import db_conn

class Entry(json.JSONEncoder):
    """
    A tournament is composed of entries who play each other. This is distinct
    from users or accounts as there may be multiple players on a team, etc.
    """

    #pylint: disable=R0913
    def __init__(
            self,
            entry_id=None,
            username=None,
            tournament_id=None,
            game_history=None,
            scores=None):
        self.entry_id = entry_id
        self.username = username
        self.tournament_id = tournament_id
        self.game_history = game_history
        self.ranking = None
        self.scores = scores
        self.total_score = 0

    def __repr__(self):
        return self.entry_id

# pylint: disable=no-member
class EntryDBConnection(object):
    """
    Connection class to the entry database
    """

    @db_conn(cursor_factory=DictCursor)
    # pylint: disable=E0602
    def entry_list(self, tournament_id):
        """
        Get the list of entries for the specified tournament.
        This simply returns a dump of entries and their info in a big list.
        """
        cur.execute(
            "SELECT \
                e.id                                    AS entry_id, \
                a.username                              AS username, \
                t.name                                  AS tournament_id, \
                (SELECT array(SELECT table_no \
                    FROM table_allocation \
                    WHERE entry_id = e.id))             AS game_history \
            FROM entry e \
            INNER JOIN account a on e.player_id = a.username \
            INNER JOIN tournament t on e.tournament_id = t.name \
            WHERE t.name = %s",
            [tournament_id])
        entries = cur.fetchall()

        unranked_list = [
            Entry(
                entry_id=entry['entry_id'],
                username=entry['username'],
                tournament_id=entry['tournament_id'],
                game_history=entry['game_history'],
                scores=self.get_scores_for_entry(entry['entry_id']),
            ) for entry in entries
        ]

        return unranked_list

    @db_conn()
    # pylint: disable=E0602
    def get_scores_for_entry(self, entry_id):
        """ Get all the score_key:score pairs for an entry"""
        cur.execute("SELECT key, score, category, min_val, max_val \
            FROM player_score WHERE entry_id = %s", [entry_id])
        return [
            {
                'key': x[0],
                'score':x[1],
                'category': x[2],
                'min_val': x[3],
                'max_val': x[4],
            } for x in cur.fetchall()
        ]

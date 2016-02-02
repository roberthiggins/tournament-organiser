"""
Module for storing games.

A game is simply a match between two entries. It is played on a table.
"""

from db_connections.db_connection import db_conn

# pylint: disable=E0602
class Game(object):
    """
    Representation of a single match between entrants.
    This might be a BYE
    """

    def __init__(self, entrants, tournament_id=None, round_id=None,
                 table_number=None):
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.table_number = table_number
        self.entry_1 = None if entrants[0] == 'BYE' else entrants[0].entry_id
        self.entry_2 = None if entrants[1] == 'BYE' else entrants[1].entry_id

        self.game_id = None
        self.protected_object_id = None

    @db_conn(commit=True)
    def write_to_db(self):
        """Write a game to db"""

        # Get a protected_object_id
        cur.execute("INSERT INTO protected_object VALUES(DEFAULT) RETURNING id")
        protected_object_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO game \
            VALUES(DEFAULT, %s, %s, %s, %s) RETURNING *",
            [
                self.round_id,
                self.tournament_id,
                self.table_number,
                protected_object_id
            ]
        )
        game = cur.fetchone()
        self.game_id = game[0]
        self.protected_object_id = game[4]

        if self.entry_1 is not None:
            cur.execute(
                "INSERT INTO game_entrant VALUES(%s, %s)",
                [self.game_id, self.entry_1])
        if self.entry_2 is not None:
            cur.execute(
                "INSERT INTO game_entrant VALUES(%s, %s)",
                [self.game_id, self.entry_2])

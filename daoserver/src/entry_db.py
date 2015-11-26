"""
This file contains code to connect to the entry_db
"""

import psycopg2

from db_connection import DBConnection
from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection

class EntryDBConnection(object):
    """
    Connection class to the entry database
    """
    def __init__(self):
        self.tournament_db_conn = TournamentDBConnection()
        self.player_db_conn = PlayerDBConnection()
        self.db_conn = DBConnection()
        self.con = self.db_conn.con

    def enter_score(self, tournament_id, entry_id, score_key, score):
        """
        Enters a score for category into tournament for player.

        Expects: All fields required
            - entry_id - of the entry
            - score_key - e.g. round_3_battle
            - score - integer

        Returns: Nothing on success. Throws ValueErrors and RuntimeErrors when
            there is an issue inserting the score.
        """
        if not entry_id or not score_key or not score:
            raise ValueError('Enter the required fields')

        try:
            cur = self.con.cursor()

            # score_key should mean something in the context of the tournie
            cur.execute(
                "SELECT id from score_key \
                WHERE key = %s AND tournament_id = %s",
                [score_key, tournament_id])
            try:
                score_id = cur.fetchone()[0]
            except TypeError:
                raise RuntimeError('Unknown category: %s' % score_key)


            cur.execute("INSERT INTO score VALUES(%s, %s, %s)",
                [entry_id, score_id, score])
            self.con.commit()

        except psycopg2.DataError:
            self.con.rollback()
            raise RuntimeError('Invalid score: %s' % score)
        except psycopg2.IntegrityError as err:
            self.con.rollback()
            raise RuntimeError('Score already set')
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise RuntimeError(err)

    def entry_id(self, tournament_id, player_id):
        """
        Get the entry_id for the player in the tournament

        Returns: Integer. The entry_id of entry, if one exists. Throws
            ValueErrors and RuntimeError if tournament or player don't exist.
        """
        if not tournament_id or not player_id:
            raise ValueError('Missing required fields to entry_id')
        if not self.player_db_conn.username_exists(player_id):
            raise ValueError('Unknown player: %s' % player_id)
        if not self.tournament_db_conn.tournament_exists(tournament_id):
            raise ValueError('Unknown tournament: %s' % tournament_id)

        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT id FROM entry \
                WHERE player_id = %s AND tournament_id = %s",
                [player_id, tournament_id])
            return cur.fetchone()[0]
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

    def entry_info(self, entry_id):
        """ Given an entry, get information about the user and tournament"""
        if not entry_id:
            raise ValueError('Missing required fields to entry_info')
        try:
            entry_id = int(entry_id)
        except ValueError:
            raise ValueError('Entry ID must be an integer')

        try:
            cur = self.con.cursor()
            cur.execute("SELECT p.username, t.name \
                FROM entry e INNER JOIN player p on e.player_id = p.username \
                INNER JOIN tournament t on e.tournament_id = t.name \
                WHERE e.id = %s", [entry_id])
            row = cur.fetchone()
            if row is None:
                raise ValueError('Entry ID not valid: {}'.format(entry_id))
            return {
                'entry_id': entry_id,
                'username': row[0],
                'tournament_name': row[1],
            }
        except psycopg2.DatabaseError as err:
            raise RuntimeError(err)

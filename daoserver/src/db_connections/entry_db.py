"""
This file contains code to connect to the entry_db
"""

from flask import json
import psycopg2
from psycopg2.extras import DictCursor

from db_connections.db_connection import DBConnection
from db_connections.player_db import PlayerDBConnection

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

class EntryDBConnection(object):
    """
    Connection class to the entry database
    """
    def __init__(self):
        self.db_conn = DBConnection()
        self.con = self.db_conn.con

    def enter_score(self, entry_id, score_key, score):
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

            cur.execute(
                "SELECT tournament_id FROM entry WHERE id = %s", [entry_id])
            tournament_id = cur.fetchone()[0]

            # score_key should mean something in the context of the tournie
            cur.execute(
                "SELECT k.id, min_val, max_val FROM score_key k \
                INNER JOIN score_category c ON k.category = c.id \
                WHERE k.key = %s AND c.tournament_id = %s",
                [score_key, tournament_id])
            row = cur.fetchone()
            try:
                score_id = row[0]
            except TypeError:
                raise RuntimeError('Unknown category: {}'.format(score_key))

            try:
                score = int(score)
            except ValueError:
                raise psycopg2.DataError()

            if score < int(row[1]) or score > int(row[2]):
                raise psycopg2.DataError()

            cur.execute(
                "INSERT INTO score VALUES(%s, %s, %s)",
                [entry_id, score_id, score])
            self.con.commit()

        except psycopg2.DataError:
            self.con.rollback()
            raise RuntimeError('Invalid score: %s' % score)
        except psycopg2.IntegrityError as err:
            self.con.rollback()
            raise RuntimeError(
                '{} not entered. Score is already set'.format(score))
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise RuntimeError(err)

    def entry_list(self, tournament_id):
        """
        Get the list of entries for the specified tournament.
        This simply returns a dump of entries and their info in a big list.
        """
        cur = self.con.cursor(cursor_factory=DictCursor)
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

    def entry_id(self, tournament_id, username):
        """
        Get the entry_id for the player in the tournament

        Returns: Integer. The entry_id of entry, if one exists. Throws
            ValueErrors and RuntimeError if tournament or player don't exist.
        """
        if tournament_id is None or username is None:
            raise ValueError('Missing required fields to entry_id')
        if not PlayerDBConnection().username_exists(username):
            raise ValueError('Unknown player: %s' % username)

        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT id FROM entry \
                WHERE player_id = %s AND tournament_id = %s",
                [username, tournament_id])
            return cur.fetchone()[0]
        except psycopg2.DatabaseError as err:
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
            cur.execute("SELECT a.username, t.name \
                FROM entry e INNER JOIN account a on e.player_id = a.username \
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

    def get_scores_for_entry(self, entry_id):
        """ Get all the score_key:score pairs for an entry"""
        cur = self.con.cursor(cursor_factory=DictCursor)
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

"""
This file contains code to connect to the tournament registrations
"""

import psycopg2

from db_connection import DBConnection
from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection

class RegistrationDBConnection(object):
    """
    Connection class for registrations to tournaments
    """
    def __init__(self):
        self.player_db_conn = PlayerDBConnection()
        self.tournament_db_conn = TournamentDBConnection()
        self.db_conn = DBConnection()
        self.con = self.db_conn.con

    def register_for_tournament(self, tournament_id, player_id):
        """
        Register a player for a tournament
        Expects:
            - tournament_id - existing tounament name as per listtournaments
            - player_id - existing username
        """
        if not self.tournament_db_conn.tournament_exists(tournament_id) \
        or not self.player_db_conn.username_exists(player_id):
            raise RuntimeError("Check username and tournament")

        clash = self.registration_clashes(tournament_id, player_id)
        if clash is not None and clash[0] == tournament_id:
            raise RuntimeError("You've already applied to %s" % tournament_id)
        elif clash is not None:
            raise RuntimeError("%s clashes with %s that you are registered \
                for already" % (tournament_id, clash[0]))

        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO registration VALUES(%s, %s)",
                        [player_id, tournament_id])
            self.con.commit()
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

        return "Application Submitted"

    def registration_clashes(self, tournament_id, player_id):
        """
        Check if the date of the tournament overlaps with another tournament
        that has been registered for by the player
        Expects:
            - tournament_id - existing tounament name as per listtournaments
            - player_id - existing username
        """
        if not tournament_id or not player_id:
            raise ValueError(
                "Parameter missing for registration_clashes(self, \
                tournament_id, player_id)",
                tournament_id,
                player_id)
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT t.name \
                FROM registration r INNER JOIN tournament t \
                    on r.tournament_id = t.name \
                WHERE player_id = %s \
                AND date = (SELECT date FROM tournament WHERE name = %s)",
                [player_id, tournament_id])
            existing = cur.fetchone()
            print existing
            return existing
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

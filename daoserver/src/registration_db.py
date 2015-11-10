# This file contains code to connect to the tournament registrations

import os
import psycopg2

from db_connection import DBConnection
from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection

class RegistrationDBConnection:
    def __init__(self):
        self.player_db_conn     = PlayerDBConnection()
        self.tournament_db_conn = TournamentDBConnection()
        self.db_conn            = DBConnection()
        self.con                = self.db_conn.con

    def registerForTournament(self, tournamentId, playerId):
        if not self.tournament_db_conn.tournamentExists(tournamentId) \
        or not self.player_db_conn.username_exists(playerId):
            raise RuntimeError("Check username and tournament")

        clash = self.clashesWithAnotherRegistration(tournamentId, playerId)
        if clash is not None and clash[0] == tournamentId:
            raise RuntimeError("You've already applied to %s" % tournamentId)
        elif clash is not None:
            raise RuntimeError("%s clashes with %s that you are registered \
                for already" % (tournamentId, clash[0]))

        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO registration VALUES(%s, %s)",
                        [playerId, tournamentId])
            self.con.commit()
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            raise e

        return "Application Submitted"

    def clashesWithAnotherRegistration(self, tournamentId, playerId):
        if not tournamentId or not playerId:
            raise ValueError(
                "Parameter missing for clashesWithAnotherRegistration(self, tournamentId, playerId)",
                playerId,
                date)
        try:
            cur = self.con.cursor()
            cur.execute("SELECT t.name FROM registration r INNER JOIN tournament t on r.tournament_id = t.name WHERE player_id = %s AND date = (SELECT date FROM tournament WHERE name = %s)", [playerId, tournamentId])
            existing = cur.fetchone()
            print existing
            return existing
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            raise e

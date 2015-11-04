# This file contains code to connect to the tournament registrations

import os
import psycopg2

from player_db import PlayerDBConnection
from tournament_db import TournamentDBConnection

class RegistrationDBConnection:
    def __init__(self):

        self.player_db_conn     = PlayerDBConnection()
        self.tournament_db_conn = TournamentDBConnection()
        self.con = None
        self.config  = {
            'db_host': os.environ['DB_PORT_5432_TCP_ADDR'],
            'db_port': os.environ['DB_PORT_5432_TCP_PORT'],
            'db_pass': os.environ['DB_PASSWORD']
        }
        try:
             self.con = psycopg2.connect(
                            database='docker',
                            user='docker',
                            host=self.config['db_host'],
                            port=self.config['db_port'],
                            password=self.config['db_pass'])
        except psycopg2.Error as e:
            print 'psycopg Error %s' % e     
        except Exception as e:
            print 'Error %s' % e

    def registerForTournament(self, tournamentId, playerId):
        if not self.tournament_db_conn.tournamentExists(tournamentId) \
        or not self.player_db_conn.usernameExists(playerId):
            return "Check username and tournament"

        clash = self.clashesWithAnotherRegistration(tournamentId, playerId)
        if clash is not None and clash[0] == tournamentId:
            return "You've already applied to %s" % tournamentId
        elif clash is not None:
            return "%s clashes with %s that you are registered for already" % (tournamentId, clash[0])

        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO registration VALUES(%s, %s)", [playerId, tournamentId])
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

    def __del__(self):
        if self.con:
            self.con.close()

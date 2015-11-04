# This file contains code to connect to the tournament_db

import os
import psycopg2

from db_connection import DBConnection

class TournamentDBConnection:
    def __init__(self):
        self.db_conn            = DBConnection()
        self.con                = self.db_conn.con


    def tournamentExists(self, name):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM tournament WHERE name = %s", [name])
            existing = cur.fetchone()
            return existing[0] > 0
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            raise e

    def addTournament(self, tournament):
        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO tournament VALUES (default, %s, %s) RETURNING id", [tournament['name'],tournament['date'] ])
            id = cur.fetchone()
            self.con.commit()

        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print 'Database Error %s' % e
            return e

    def listTournaments(self):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM tournament")
            return cur.fetchall()
        except psycopg2.DatabaseError as e:
            print 'Database Error %s' % e
            return e

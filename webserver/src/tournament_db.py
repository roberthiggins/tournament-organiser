# This file contains code to connect to the tournament_db

import os
import psycopg2

class TournamentDBConnection:
    def __init__(self):

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

    def __del__(self):
        if self.con:
            self.con.close()

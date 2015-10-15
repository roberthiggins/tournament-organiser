# This file contains code to connect to the player_db

import os
import psycopg2

class PlayerDBConnection:
    def __init__(self):

        self.con = None
        self.config  = {
            'db_host': os.environ['PLAYER_DB_PORT_5432_TCP_ADDR'],
            'db_port': os.environ['PLAYER_DB_PORT_5432_TCP_PORT'],
            'db_pass': os.environ['PLAYER_DB_PASSWORD']
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

    def addPlayer(self, player):
        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO player VALUES (default, %s)", [player['user_name']])
            self.con.commit()

        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print 'Database Error %s' % e
            return e

    def __del__(self):
        if self.con:
            self.con.close()

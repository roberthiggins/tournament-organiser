# This file contains code to connect to the player_db

import os
import psycopg2

class PlayerDBConnection:
    def __init__(self):

        self.con = None
        self.config  = {
            'db_host': os.environ['PLAYER_DB_PORT_5432_TCP_ADDR'],
            'db_port': os.environ['PLAYER_DB_PORT_5432_TCP_PORT']
        }
        try:
             self.con = psycopg2.connect(
                            database='docker',
                            user='docker',
                            host=self.config['db_host'],
                            port=self.config['db_port'],
                            password='FuEm7l003bfd6zM') 
        except psycopg2.Error as e:
            print 'psycopg Error %s' % e     
        except Exception as e:
            print 'Error %s' % e

    def __del__(self):
        if self.con:
            self.con.close()

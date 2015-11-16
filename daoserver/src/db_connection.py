"""
Class to make a connection to the db
"""

import os
import psycopg2

class DBConnection(object):
    """
    Class to make a connection to the db
    """
    def __init__(self):

        self.con = None
        self.config = {
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
        except psycopg2.Error as err:
            print 'psycopg Error %s' % err
        except Exception as err:
            print 'Error %s' % err

    def __del__(self):
        if self.con:
            self.con.close()

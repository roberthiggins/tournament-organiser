import os
import psycopg2

class DBConnection:
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

    def __del__(self):
        if self.con:
            self.con.close()

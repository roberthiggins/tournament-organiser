"""
Class to make a connection to the db
"""

from functools import wraps

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

    def __del__(self):
        if self.con:
            self.con.close()

def db_conn(commit=False):
    """A decorator that gives the function a db_conn to use (cur)"""
    def decorator(func):                            # pylint: disable=C0111
        @wraps(func)
        def wrapped(*args, **kwargs):               # pylint: disable=C0111

            glob = func.func_globals
            sentinel = object()
            old_values = {}

            old_values['conn'] = glob.get('conn', sentinel)
            old_values['cur'] = glob.get('cur', sentinel)

            conn = DBConnection()
            glob['conn'] = conn.con
            glob['cur'] = glob['conn'].cursor()

            try:
                res = func(*args, **kwargs)
                if commit:
                    glob['conn'].commit()
            except psycopg2.DatabaseError as err:
                try:
                    glob['conn'].rollback()
                except AttributeError:
                    pass
                raise ValueError(err)
            finally:
                glob['cur'].close()
                glob['conn'].close()
                for var in ['cur', 'conn']:
                    if old_values[var] is sentinel:
                        del glob[var]
                    else:
                        glob[var] = old_values[var]

            return res
        return wrapped
    return decorator

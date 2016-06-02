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
            'db_host': os.environ['DATABASE_PORT_5432_TCP_ADDR'],
            'db_name': os.environ['DATABASE_NAME'],
            'db_port': os.environ['DATABASE_PORT_5432_TCP_PORT'],
            'db_pass': os.environ['DATABASE_PASSWORD']
        }
        try:
            self.con = psycopg2.connect(
                database=self.config['db_name'],
                user='docker',
                host=self.config['db_host'],
                port=self.config['db_port'],
                password=self.config['db_pass'])
        except psycopg2.Error as err:
            print 'psycopg Error %s' % err

    def __del__(self):
        if self.con:
            self.con.close()

def db_conn(commit=False, cursor_factory=None):
    """A decorator that gives the function a db_conn to use (cur)"""
    def decorator(func):                            # pylint: disable=missing-docstring
        @wraps(func)
        def wrapped(*args, **kwargs):               # pylint: disable=missing-docstring

            glob = func.func_globals
            sentinel = object()
            old_values = {}

            old_values['conn'] = glob.get('conn', sentinel)
            old_values['cur'] = glob.get('cur', sentinel)

            conn = DBConnection()
            glob['conn'] = conn.con
            glob['cur'] = glob['conn'].cursor(cursor_factory=cursor_factory)

            try:
                res = func(*args, **kwargs)
                if commit:
                    glob['conn'].commit()
            except psycopg2.DatabaseError as err:
                rollback(glob)
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

def rollback(glob):
    """
    Rollback the db transaction.

    If glob has a 'conn' db connection it will be closed.
    """
    if glob['conn'] is None:
        return

    try:
        glob['conn'].rollback()
    except AttributeError:
        pass

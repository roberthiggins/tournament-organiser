"""
This file handles inserting feedback into the db
"""

import psycopg2

from db_connection import DBConnection

class FeedbackDBConnection(object):
    """
    Connection class to allow feedback on the website to be stored in DB
    """
    def __init__(self):
        self.db_conn = DBConnection()
        self.con = self.db_conn.con

    def submit_feedback(self, feedback):
        """Store feedback string in db"""
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM feedback WHERE feedback ILIKE %s",
                [feedback])
            if cur.fetchone()[0] > 0:
                return
            cur.execute("INSERT INTO feedback VALUES(DEFAULT, %s, DEFAULT)",
                        [feedback])
            self.con.commit()
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

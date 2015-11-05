# This file handles inserting feedback into the db

import os
import psycopg2

from db_connection import DBConnection

class FeedbackDBConnection:
    def __init__(self):
        self.db_conn            = DBConnection()
        self.con                = self.db_conn.con

    def submitFeedback(self, feedback):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM feedback WHERE feedback ILIKE %s", [feedback])
            if cur.fetchone()[0] > 0:
                return
            cur.execute("INSERT INTO feedback VALUES(DEFAULT, %s, DEFAULT)", [feedback])
            self.con.commit()
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            raise e

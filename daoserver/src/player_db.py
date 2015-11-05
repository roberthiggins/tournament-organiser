# This file contains code to connect to the player_db

import os
import psycopg2

from db_connection import DBConnection

class PlayerDBConnection:
    def __init__(self):
        self.db_conn            = DBConnection()
        self.con                = self.db_conn.con

    def usernameExists(self, username):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM player WHERE username = %s", [username])
            existing = cur.fetchone()
            return existing[0] > 0
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            raise e

    def addAccount(self, account):
        try:
            cur = self.con.cursor()
            cur.execute("INSERT INTO account VALUES (default, %s) RETURNING id", [account['email']])
            id = cur.fetchone()
            cur.execute("INSERT INTO player VALUES (%s, %s)", [id, account['user_name']])
            self.con.commit()

        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print 'Database Error %s' % e
            return e


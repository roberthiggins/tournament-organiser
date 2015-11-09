# This file contains code to connect to the player_db

import os
import psycopg2
from passlib.hash import sha256_crypt

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
            cur.execute("INSERT INTO account_security VALUES (%s, %s)",
                        [id, sha256_crypt.encrypt(account['password']) ] )
            cur.execute("INSERT INTO player VALUES (%s, %s)", [id, account['user_name']])
            self.con.commit()

        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print 'Database Error %s' % e
            return e
        except Exception as e:
            print "Exception in addAccount: " + e

    def login(self, username, password):
        if not username or not password:
            raise RuntimeError("Enter username and password")
        try:
            cur = self.con.cursor()
            cur.execute("SELECT s.password FROM account_security s INNER JOIN player p ON s.id = p.id WHERE p.username = %s",
                        [username] )
            creds = cur.fetchone()
            if not creds or not sha256_crypt.verify(password, creds[0]):
                raise RuntimeError("Username or password incorrect")
            return "Login successful"
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print 'Database Error %s' % e
            raise e
        except RuntimeError:
            raise
        except Exception as e:
            print e
            raise


"""
This file contains code to connect to the player_db
"""

import psycopg2
from passlib.hash import sha256_crypt

from db_connection import DBConnection

class PlayerDBConnection(object):
    """ A connection class for accessing player/account info from the db"""
    def __init__(self):
        self.db_conn = DBConnection()
        self.con = self.db_conn.con

    def username_exists(self, username):
        """Check if a username exists for a player"""
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM player WHERE username = %s",
                        [username])
            existing = cur.fetchone()
            return existing[0] > 0
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            raise err

    def add_account(self, account):
        """Add an account. Username cannot exist"""
        try:
            cur = self.con.cursor()
            cur.execute(
                "INSERT INTO account VALUES (default, %s) RETURNING id",
                [account['email']])
            account_id = cur.fetchone()
            cur.execute("INSERT INTO account_security VALUES (%s, %s)",
                        [account_id, sha256_crypt.encrypt(account['password'])])
            cur.execute("INSERT INTO player VALUES (%s, %s)",
                        [account_id, account['user_name']])
            self.con.commit()

        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            return err

    def authenticate_user(self, username, password):
        """
        Authenticates the uanme and pword.
        Expects:
            - username
            - password - may be encrypted as per standard practice
        Return True on success
        """
        if not username or not password:
            raise RuntimeError("Enter username and password")
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT s.password \
                 FROM account_security s INNER JOIN player p ON s.id = p.id \
                 WHERE p.username = %s",
                [username])
            creds = cur.fetchone()
            if not creds or not sha256_crypt.verify(password, creds[0]):
                raise RuntimeError("Username or password incorrect")
            return True
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            raise err
        except RuntimeError:
            raise
        except Exception as err:
            print err
            raise

    def login(self, username, password):
        """Attempt to log a player in"""
        if self.authenticate_user(username, password):
            return "Login successful"
        else:
            return "Login unsuccessful"

    def user_details(self, username):
        """ get the user details asa a json blob """
        try:
            cur = self.con.cursor()
            cur.execute(
                "SELECT a.contact_email, p.settings \
                FROM account a INNER JOIN player p ON a.id = p.id \
                WHERE p.username = %s",
                [username])
            return cur.fetchone()
        except psycopg2.DatabaseError as err:
            self.con.rollback()
            print 'Database Error %s' % err
            raise err

"""
This file contains code to connect to the player_db
"""

from passlib.hash import sha256_crypt

from db_connections.db_connection import db_conn
from models.account import Account

# pylint: disable=E0602
class PlayerDBConnection(object):
    """ A connection class for accessing player/account info from the db"""

    @db_conn(commit=True)
    def add_account(self, account):
        """Add an account. Username cannot exist"""
        Account(account['user_name'], account['email']).write()

        cur.execute(
            "INSERT INTO account_security VALUES (%s, %s)",
            [account['user_name'],
             sha256_crypt.encrypt(account['password'])])

    @db_conn()
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
            cur.execute(
                "SELECT password FROM account_security \
                INNER JOIN account ON id = username \
                WHERE username = %s",
                [username])
            creds = cur.fetchone()
            if not creds or not sha256_crypt.verify(password, creds[0]):
                raise RuntimeError("Username or password incorrect")
            return True
        except RuntimeError:
            raise

    def login(self, username, password):
        """Attempt to log a player in"""
        if self.authenticate_user(username, password):
            return "Login successful"
        else:
            return "Login unsuccessful"

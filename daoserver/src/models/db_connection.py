"""
This sets up a connection to a database.

Currently there is only one db so all connections can come through here.
"""


from flask.ext.sqlalchemy import SQLAlchemy

# pylint: disable=invalid-name
db = SQLAlchemy()


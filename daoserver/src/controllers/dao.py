"""
Entrypoint for the DAO

This is the public API for the Tournament Organiser. The website, and apps
should talk to this for functionality wherever possible.
"""

from flask import Blueprint

from controllers.request_helpers import text_response

APP = Blueprint('APP', __name__, url_prefix='')

@APP.route("/")
@text_response
def main():
    """Index page. Used to verify the server is running."""
    return 'daoserver'

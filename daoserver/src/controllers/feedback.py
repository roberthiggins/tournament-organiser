"""
Feedback from users
"""

import re

from flask import Blueprint, request, make_response
from sqlalchemy.exc import IntegrityError

from models.dao.db_connection import db
from models.dao.feedback import Feedback

FEEDBACK = Blueprint('FEEDBACK', __name__)

@FEEDBACK.route('', methods=['POST'])
def place_feedback():
    """
    POST to add feedback or submit suggestion.
    Expects:
        - inputFeedback - A string
    """
    _feedback = request.form['inputFeedback'].strip('\n\r\t+')
    if re.match(r'^[\+\s]*$', _feedback) is not None:
        return make_response("Please fill in the required fields", 400)
    try:
        db.session.add(Feedback(_feedback))
        db.session.commit()
    except IntegrityError:
        pass

    return make_response("Thanks for you help improving the site", 200)

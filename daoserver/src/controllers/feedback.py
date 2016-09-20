"""
Feedback from users
"""

import re

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from controllers.request_helpers import requires_auth, text_response
from models.dao.db_connection import db
from models.dao.feedback import Feedback

FEEDBACK = Blueprint('FEEDBACK', __name__)

@FEEDBACK.route('', methods=['POST'])
@requires_auth
@text_response
def place_feedback():
    """
    POST to add feedback or submit suggestion.
    Expects:
        - inputFeedback - A string
    """
    _feedback = request.form['inputFeedback'].strip('\n\r\t+')
    if re.match(r'^[\+\s]*$', _feedback) is not None:
        raise ValueError('Please fill in the required fields')
    try:
        db.session.add(Feedback(_feedback))
        db.session.commit()
    except IntegrityError:
        pass

    return 'Thanks for you help improving the site'

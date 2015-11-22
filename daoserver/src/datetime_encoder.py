"""
A date/datetime serialiser for JSON

json doesn't encode dates well so we override the default method.
"""

from flask import json
import datetime

class DateTimeJSONEncoder(json.JSONEncoder):    # pylint: disable=C0111,W0232
    def default(self, obj):                     # pylint: disable=C0111,E1002
        if isinstance(obj, datetime.datetime) \
        or isinstance(obj, datetime.date):
            return obj.isoformat()
        else:
            return super(DateTimeJSONEncoder, self).default(obj)

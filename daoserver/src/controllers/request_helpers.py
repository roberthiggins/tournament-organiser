"""
Basic decorator for enforcing request elements
"""

from flask import Response, request, make_response
from functools import wraps
import jsonpickle

def enforce_request_variables(*vars_to_enforce):
    """ A decorator that requires var exists in the request"""
    def decorator(func):                # pylint: disable=missing-docstring
        @wraps(func)
        def wrapped(*args, **kwargs):   # pylint: disable=missing-docstring

            if request.method == 'GET':
                return func(*args, **kwargs)

            glob = func.func_globals
            sentinel = object()
            old_values = {}

            for var in vars_to_enforce:
                value = request.form[var] if var in request.form \
                    else request.values.get(var, None)

                if value is None and request.get_json() is not None:
                    value = request.get_json().get(var, None)

                if value is None:
                    return make_response('Enter the required fields', 400)

                old_values[var] = glob.get(var, sentinel)
                glob[var] = value

            try:
                res = func(*args, **kwargs)
            finally:
                for var in vars_to_enforce:
                    if old_values[var] is sentinel:
                        del glob[var]
                    else:
                        glob[var] = old_values[var]

            return res
        return wrapped
    return decorator

def json_response(func):
    """Wrap the return value of func with jsonpickle and return as Response"""
    @wraps(func)
    def wrapped(*args, **kwargs):       # pylint: disable=missing-docstring

        return Response(
            jsonpickle.encode(func(*args, **kwargs), unpicklable=False),
            mimetype='application/json')

    return wrapped

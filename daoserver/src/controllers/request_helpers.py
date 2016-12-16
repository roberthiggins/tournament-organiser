"""
Basic decorator for enforcing request elements
"""

from functools import wraps
from flask import g, Response, request
import jsonpickle
from models.authentication import check_auth
from models.permissions import PERMISSIONS, PermissionsChecker

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
                value = request.get_json().get(var, None)

                if value is None:
                    raise ValueError('Enter the required fields')

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

def ensure_permission(permission):
    """
    Check that the user in the request authorization has appropriate
    permissions
    A permission should be a dict:
        {
            permission: String PERMISSION,
        }
    """
    def decorator(func):                # pylint: disable=missing-docstring
        @wraps(func)
        def wrapped(*args, **kwargs):   # pylint: disable=missing-docstring

            user = getattr(request.authorization, 'username', None)
            target = getattr(g, 'username', None)

            checker = PermissionsChecker()
            # pylint: disable=undefined-variable
            checker.check_permission(
                PERMISSIONS.get(permission.get('permission')),
                user,
                target,
                getattr(g, 'tournament_id', None))

            return func(*args, **kwargs)
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

def requires_auth(func):
    """Checks the authorization of the request for a valid user password"""
    @wraps(func)
    def wrapped(*args, **kwargs):       # pylint: disable=missing-docstring

        if not check_auth(getattr(request.authorization, 'username', None),
                          getattr(request.authorization, 'password', None)):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})

        return func(*args, **kwargs)

    return wrapped

def text_response(func):
    """Wrap the return value of func in a Response"""
    @wraps(func)
    def wrapped(*args, **kwargs):       # pylint: disable=missing-docstring

        text = func(*args, **kwargs)
        if isinstance(text, basestring):
            return Response(text, mimetype='text/html')
        else:
            return text # Probably an error response

    return wrapped

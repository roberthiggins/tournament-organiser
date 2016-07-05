"""
Connector to perform requests to the DAO
"""
# pylint: disable=no-member

import os
import requests

from django.http import HttpResponse

### Some helper methods

DAO_NAME = os.environ['DAO_CONTAINER']
DAO_URL = 'http://{}:{}'.format(
    os.environ['{}_PORT_5000_TCP_ADDR'.format(DAO_NAME)],
    os.environ['{}_PORT_5000_TCP_PORT'.format(DAO_NAME)]
)

def from_dao(url, form=None, request=None):
    """
    Proxies a GET/POST to the daoserver. This helps keep input handling in \
    the DAO API
    """
    try:
        api = DAO_URL + url
        auth = None
        if request is not None and request.user is not None \
        and request.user.is_authenticated():
            auth = (request.user.username, request.user.password)

        if form is None:
            return requests.get(api, auth=auth)

        return requests.post(api, auth=auth, data=form.cleaned_data)

    except requests.exceptions.HTTPError as err:
        if err.code == 400:
            return HttpResponse(err.read(), status=400)
        else:
            raise

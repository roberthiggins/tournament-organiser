"""
Connector to perform requests to the DAO
"""
import os
import requests

from django.http import HttpResponse

### Some helper methods

DAO_URL = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])

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

        if form.is_valid():
            return requests.post(api, auth=auth, data=form.cleaned_data)

        return HttpResponse(form.error_code(), status=400)

    except requests.exceptions.HTTPError as err:
        if err.code == 400:
            return HttpResponse(err.read(), status=400)
        else:
            raise

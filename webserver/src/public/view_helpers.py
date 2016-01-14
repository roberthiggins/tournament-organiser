"""
Connector to perform requests to the DAO
"""
import os
import urllib
import urllib2

from django.http import HttpResponse

### Some helper methods

DAO_URL = "http://%s:%s" % (
    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])

def from_dao(url, form=None):
    """
    Proxies a GET/POST to the daoserver. This helps keep input handling in \
    the DAO API
    """
    try:

        if form is None:
            return HttpResponse(
                urllib2.urlopen(urllib2.Request(DAO_URL + url))
            )

        if form.is_valid():
            return HttpResponse(
                urllib2.urlopen(urllib2.Request(
                    DAO_URL + url,
                    urllib.urlencode(form.cleaned_data))))

        return HttpResponse(form.error_code(), status=400)

    except urllib2.HTTPError as err:
        if err.code == 400:
            return HttpResponse(err.read(), status=400)
        else:
            raise
    except Exception as err:
        print err
        raise

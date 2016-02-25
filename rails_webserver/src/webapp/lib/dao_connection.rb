=begin

    If you want to talk to the DAO Server you should use this module for all
    your connection needs.
=end
module DaoConnection

@@DAO_URL ="http://%s:%s" % [
    ENV['DAOSERVER_PORT_5000_TCP_ADDR'],
    ENV['DAOSERVER_PORT_5000_TCP_PORT']]

=begin
    Use a GET request to the daoserver. The return value will be passed
    back to the caller.
=end
    def dao_get(url)
        return HTTParty.get "%s/%s" % [@@DAO_URL, url]

        # TODO auth
        # TODO form crap
    end



#DAO_URL = "http://%s:%s" % (
#    os.environ['DAOSERVER_PORT_5000_TCP_ADDR'],
#    os.environ['DAOSERVER_PORT_5000_TCP_PORT'])
#
#def from_dao(url, form=None, request=None):
#    """
#    Proxies a GET/POST to the daoserver. This helps keep input handling in \
#    the DAO API
#    """
#    try:
#        api = DAO_URL + url
#        auth = None
#        if request is not None and request.user is not None \
#        and request.user.is_authenticated():
#            auth = (request.user.username, request.user.password)
#
#        if form is None:
#            return requests.get(api, auth=auth)
#
#        if form.is_valid():
#            return requests.post(api, auth=auth, data=form.cleaned_data)
#
#        return HttpResponse(form.error_code(), status=400)
#
#    except requests.exceptions.HTTPError as err:
#        if err.code == 400:
#            return HttpResponse(err.read(), status=400)
#        else:
#            raise

end

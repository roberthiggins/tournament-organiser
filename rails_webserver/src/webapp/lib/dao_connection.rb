=begin

    If you want to talk to the DAO Server you should use this module for all
    your connection needs.
=end
module DaoConnection

require 'net/http'
require 'uri'

@@DAO_URL ="http://%s:%s" % [
    ENV['DAOSERVER_PORT_5000_TCP_ADDR'],
    ENV['DAOSERVER_PORT_5000_TCP_PORT']]

# TODO This is only until logins get set up on webserver
@@AUTH = { :username => 'superman',
    :password => '$5$rounds=535000$YgBRpraLjej03Wm0$52r5LDk9cx0ioGSI.6rW/d1l2d5wo1Qn7tyTxm8e26D' } # superuser permissions initially


=begin
    Interact with the DAOServer
=end
    def from_dao(url, form=nil, use_auth=false)

        uri = URI("%s/%s" % [@@DAO_URL, url])
        http = Net::HTTP.new(uri.host, uri.port)
        request = Net::HTTP::Get.new(uri.request_uri)

        if form
            request = Net::HTTP::Post.new(uri.request_uri)
            request.set_form_data(form)
        end

        request.basic_auth(@@AUTH[:username], @@AUTH[:password])

        return http.request(request)
    end

end

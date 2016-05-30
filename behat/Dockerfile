# This will build the behat testing container. The intention is that we test
# the website by building a version of the real thing, insert a bunch of fake
# data, and then run this container to run some functional testing. Unit tests will also be run from another container

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>
RUN apt-get install -y php5 php5-curl

# Get Composer
RUN apt-get install -y curl
RUN curl -sS https://getcomposer.org/installer | php
ADD composer.json /
RUN php /composer.phar install

ADD src/ /

# Install and setup behat
RUN bin/behat --init

CMD export BEHAT_PARAMS='{"extensions": { "Behat\\MinkExtension\\Extension": {"goutte": {}, "selenium2": {"wd_host":"http://'$SELENIUM_PORT_4444_TCP_ADDR':'$SELENIUM_PORT_4444_TCP_PORT'/wd/hub"}, "base_url": "http://'$WEBSERVER_PORT_8000_TCP_ADDR':'$WEBSERVER_PORT_8000_TCP_PORT'"}}, "context": {"parameters": {"api_url": "http://'$DAOSERVER_PORT_5000_TCP_ADDR':'$DAOSERVER_PORT_5000_TCP_PORT'"}}}' && \
behat

# This will build the behat testing container. The intention is that we test
# the website by building a version of the real thing, insert a bunch of fake
# data, and then run this container to run some functional testing.

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>
RUN apt-get install -y php5 php5-curl

# Get Composer
RUN apt-get install -y curl
RUN curl -sS https://getcomposer.org/installer | php
ADD composer.json /
RUN php /composer.phar install

ADD src/ src/
WORKDIR src/

# Install and setup behat
RUN /bin/behat --init

CMD behat

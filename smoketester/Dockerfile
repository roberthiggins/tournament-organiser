# This will fire up the webserver. It is a flask app on ubuntu 14.04

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

RUN apt-get install -y curl postgresql
ENV PLAYER_DB_PASSWORD FuEm7l003bfd6zM

ADD src/ tests/

CMD tests/run_tests

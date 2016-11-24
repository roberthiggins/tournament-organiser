# This will create an image for frisby API tests.

FROM node
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

RUN npm install -g frisby
RUN npm install -g jasmine-node

WORKDIR /opt/frisby/

ENV NODE_PATH /usr/local/lib/node_modules/

ADD src/ /opt/frisby/tests

CMD jasmine-node \
    --config API_ADDR "http://${SYSTEMTESTWEBSERVER_PORT_8000_TCP_ADDR}:${SYSTEMTESTWEBSERVER_PORT_8000_TCP_PORT}/" \
    tests

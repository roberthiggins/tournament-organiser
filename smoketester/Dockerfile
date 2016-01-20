# Smoketester for the tournament builder ecosystem. This is only intended for
# use with the webapp stack.

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

RUN apt-get install -y curl postgresql
ENV DB_NAME to-db
ENV DB_PASSWORD FuEm7l003bfd6zM

ADD src/ tests/

CMD tests/run_tests

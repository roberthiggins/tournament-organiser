# Smoketester for the tournament builder ecosystem. This is only intended for
# use with the webapp stack.

FROM ubuntu
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

RUN apt-get update && apt-get install -y curl postgresql

ADD src/ tests/

CMD tests/run_tests

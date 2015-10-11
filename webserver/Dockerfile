# This will fire up the webserver. It is a flask app on ubuntu 14.04

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>
RUN apt-get update && apt-get install -y python

# Getting pip.
# For some reason I can get it via apt-get. So we do it the hard way.
RUN apt-get install -y curl
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
# End getting pip

# Install flask
# This is the python tool that will run the webserver
RUN pip install flask

# We need to attach to the player db
RUN apt-get install -y postgresql

ADD src/ webapp/

CMD python webapp/app.py

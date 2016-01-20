# This will fire up the webserver. It is a django app on ubuntu 14.04

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

# Python and build essentials
RUN apt-get update && apt-get install -y curl python python-setuptools python-dev libpq-dev build-essential

# Getting pip.
# For some reason I can get it via apt-get. So we do it the hard way.
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

# Set up Django
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Content
# The original src of the src/ dir used here can be found on github
# https://github.com/roberthiggins/Tournament_Organizer-
# in the webserver directory.
ADD src/ webapp/
ADD ./init.sh webapp/
ADD ./bash_aliases /root/.bash_aliases

# Config
WORKDIR webapp/

CMD bash ./init.sh && python manage.py runserver 0.0.0.0:8000

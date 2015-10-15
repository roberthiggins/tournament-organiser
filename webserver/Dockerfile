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

# Yaml for the configuration file
RUN pip install pyyaml

# We need to attach to the player db
RUN apt-get install -y postgresql

# Docker suggests that normally you shouldn't run update manually. However it
# is the only way to get python-dev to install.
RUN apt-get update && apt-get install -y python-dev
RUN apt-get install -y libpq-dev
RUN pip install psycopg2 Flask-SQLAlchemy Flask-Migrate
ENV PLAYER_DB_PASSWORD FuEm7l003bfd6zM
ADD src/bash_aliases /root/.bash_aliases

# Add the source dir
ADD src/ webapp/

# Run the app by default
CMD python -u webapp/app.py

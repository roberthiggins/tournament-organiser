# This will fire up the daoserver. It is a flask app on ubuntu 14.04
# The daoserver is the (eventually) public api server for operations on players
# and tournaments. In the mean time it is intended to be run privately; user
# authentication and permissions are only being added now.

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

# Python
RUN apt-get update && apt-get install -y python

# Getting pip.
# For some reason I can get it via apt-get. So we do it the hard way.
RUN apt-get install -y curl
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

# Install flask
RUN pip install flask

# passlib for passwords
RUN pip install passlib

# We need to attach to the db. Docker suggests that normally you
# shouldn't run update manually. However it is the only way to get
# python-dev or postgresql to install
RUN apt-get update && apt-get install -y postgresql python-dev libpq-dev
RUN pip install psycopg2 Flask-SQLAlchemy Flask-Migrate Flask-Testing

# jsonpickle is used for serializing objects into JSON
RUN pip install jsonpickle

# Django is used for email validation
RUN pip install django

# Unit tests only
RUN pip install testfixtures
# End Unit test installs

# Add the source dir
ADD src/ webapp/
ADD bash_aliases /root/.bash_aliases

# This should only work in the dev environment. Staging/Prod dbs will have
# their passwords set separately. However this is an issue for Orchestration.
# For now a default password will do.
ENV DB_NAME to-db
ENV DB_PASSWORD FuEm7l003bfd6zM

# Config
WORKDIR webapp/

CMD python -u app.py

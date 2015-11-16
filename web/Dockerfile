# This will fire up the webserver. It is a flask app on ubuntu 14.04

FROM ubuntu:14.04
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

RUN apt-get update && apt-get install -y python python-django python-dev libpq-dev build-essential

# Getting pip.
# For some reason I can get it via apt-get. So we do it the hard way.
RUN apt-get install -y curl
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
# End getting pip

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Setup Django
ADD src/ webapp/
WORKDIR webapp/

ADD ./init.sh ./
CMD bash ./init.sh && python manage.py runserver 0.0.0.0:8000

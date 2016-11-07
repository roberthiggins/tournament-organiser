# A node webserver

FROM node:4
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

# Create a nonroot user named app
RUN useradd --user-group --create-home --shell /bin/false appuser &&\
  npm install --global npm
ENV HOME=/home/appuser

# Prepare app directory
RUN mkdir -p $HOME/app
ADD package.json $HOME/app
RUN chown -R appuser:appuser $HOME/*
USER appuser

# Install dependencies
WORKDIR $HOME/app
RUN npm install

# Build the app
ADD . $HOME/app
RUN npm build

# Expose the app port
EXPOSE 3000

# Start the app
CMD npm run start

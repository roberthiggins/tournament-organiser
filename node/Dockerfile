# A node webserver

FROM node:4
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

# Prepare app directory
RUN mkdir -p /usr/src/app
ADD package.json /usr/src/app/

# Install dependencies
WORKDIR /usr/src/app
RUN npm install

# Build the app
ADD . /usr/src/app
RUN npm build

# Expose the app port
EXPOSE 3000

# Start the app
CMD npm run start

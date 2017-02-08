# A node webserver

FROM node
MAINTAINER Robert Higgins <robert.h.higgins@gmail.com>

# Create a nonroot user named app
RUN useradd --user-group --create-home --shell /bin/false appuser
RUN curl -L https://npmjs.org/install.sh | sh
#RUN npm install --global npm ## This should work but https://github.com/npm/npm/issues/9863
ENV HOME=/home/appuser

# Prepare app directory
RUN mkdir -p $HOME/app
ADD package.json $HOME/app
RUN chown -R appuser:appuser $HOME/*
USER appuser

# Install dependencies
WORKDIR $HOME/app
RUN npm install -q

# Build the app
ADD . $HOME/app
RUN mkdir -p $HOME/app/log
RUN npm build -q

# Expose the app port
EXPOSE 3000

HEALTHCHECK --interval=1s --timeout=1s \
    CMD curl --fail http://localhost:8000/ || exit 1

# Start the app
CMD npm run start

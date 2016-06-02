"""
This helper script will extract variables from your env_config file (that are
required by the database) and use them to create an env-file for use by docker.
The file will be placed in the appropriate place in the database directory.
"""

import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('config/dev/config.ini')

with open('webserver/env_file', 'a') as env_file:

    OPTS = dict(CONFIG.items('WEBSERVER'))
    for key, value in OPTS.items():
        env_file.write('{}={}\n'.format(key.upper(), value))

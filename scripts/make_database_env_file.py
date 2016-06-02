"""
This helper script will extract variables from your env_config file (that are
required by the database) and use them to create an env-file for use by docker.
The file will be placed in the appropriate place in the database directory.
"""

import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('config/dev/config.ini')

DATABASE_NAME = CONFIG.get('DATABASE', 'DATABASE_NAME')
DATABASE_PASSWORD = CONFIG.get('DATABASE', 'DATABASE_PASSWORD')

with open('database/env_file', 'a') as env_file:
    env_file.write('DATABASE_NAME={}\n'.format(DATABASE_NAME))
    env_file.write('DATABASE_PASSWORD={}\n'.format(DATABASE_PASSWORD))

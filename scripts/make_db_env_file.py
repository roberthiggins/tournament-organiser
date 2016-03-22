"""
This helper script will extract variables from your env_config file (that are
required by the db) and use them to create an env-file for use by docker. The
file will be placed in the appropriate place in the db directory.
"""

import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('database/env_config.ini')

DB_NAME = CONFIG.get('DATABASE', 'DB_NAME')
DB_PASSWORD = CONFIG.get('DATABASE', 'DB_PASSWORD')

with open('database/env_file', 'a') as env_file:
    env_file.write('DB_NAME={}\n'.format(DB_NAME))
    env_file.write('DB_PASSWORD={}\n'.format(DB_PASSWORD))

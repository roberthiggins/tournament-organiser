"""
This helper script will extract variables from your env_config file (that are
required by the database) and use them to create an env-file for use by docker.
The file will be placed in the appropriate place in the database directory.
"""

import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('config/dev/config.ini')

POSTGRES_DB = CONFIG.get('DATABASE', 'POSTGRES_DB')
DATABASE_PASSWORD = CONFIG.get('DATABASE', 'DATABASE_PASSWORD')
POSTGRES_USER = CONFIG.get('DATABASE', 'POSTGRES_USER')

with open('database/env_file', 'a') as env_file:
    env_file.write('POSTGRES_USER={}\n'.format(POSTGRES_USER))
    env_file.write('POSTGRES_DB={}\n'.format(POSTGRES_DB))
    env_file.write('DATABASE_PASSWORD={}\n'.format(DATABASE_PASSWORD))

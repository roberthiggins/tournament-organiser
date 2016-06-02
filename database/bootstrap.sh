# The container doesn't have a working db as we might wish to set passwords,
# etc. at runtime. So we create the actual db here. This script will be run as
# the entrypoint to the image.

# Create a PostgreSQL role named ``docker`` with default password and
# then create a database `to-db` owned by the ``docker`` role. Then fill that
# database from the files in the setup directory.
# IMPORTANT ASSUMPTION: We assume that all the files in the setup dir are
# ordered correctly. This can be done by prefixing a number to the filename.
/etc/init.d/postgresql start

COMMAND="CREATE USER docker WITH SUPERUSER PASSWORD '"$DATABASE_PASSWORD"';"
psql --command "$COMMAND"

createdb -O docker $DATABASE_NAME
for i in setup/*.sql; do psql --file=$i -d to-db ;done

/etc/init.d/postgresql stop


# Start the db running as a daemon
/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c "config_file=/etc/postgresql/9.3/main/postgresql.conf"

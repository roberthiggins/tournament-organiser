#!/bin/bash
# Taken from docker compose reference

set -e

host="$1"
shift
cmd="$@"

check () {
    args=(
            --host "$1"
            --username "postgres"
            --quiet --no-align --tuples-only
    #        --password "$DATABASE_PASSWORD"
    )
    select="$(echo 'SELECT 1' | psql "${args[@]}")" && [ "$select" = '1' ]
}

until check $host &> /dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd

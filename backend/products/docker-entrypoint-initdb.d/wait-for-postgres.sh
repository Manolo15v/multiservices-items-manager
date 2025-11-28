#!/bin/bash
# Este script espera argumentos: $1 = host, $2 = database, $3 = username, $4 = password

set -e
host="$1"
shift
cmd="$@"

until PGPASSWORD=$4 psql -h "$host" -U "$3" -d "$2" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd
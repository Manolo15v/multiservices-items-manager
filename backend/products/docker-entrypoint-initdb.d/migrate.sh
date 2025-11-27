#!/bin/bash
set -e

# Esperar a que la base de datos esté lista
./docker-entrypoint-initdb.d/wait-for-postgres.sh postgresql laravel postgres secret

# Ejecutar migraciones
cd /var/www/html && php artisan migrate --force --no-interaction

>&2 echo "Migrations completed successfully"
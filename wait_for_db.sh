#!/bin/bash

# Default values
DB_HOST=${DJANGO_DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

# Wait until the PostgreSQL server is ready
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL is up - continuing..."
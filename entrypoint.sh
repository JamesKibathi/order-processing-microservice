#!/bin/sh

echo "Waiting for database to be ready..."
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 2
done

echo "Database is up, starting the application..."
exec "$@"

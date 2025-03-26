#!/bin/sh

echo "Waiting for database to be ready..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 2
done

echo "Database is up, starting the application..."
exec "$@"

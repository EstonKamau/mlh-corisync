#!/bin/bash

set -e

# Wait for PostgreSQL to be available
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 1
done

# Run the enable_logical_replication.sql script
echo "Running enable_logical_replication.sql on $POSTGRES_DB..."
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /scripts/enable_logical_replication.sql

echo "Logical replication setup completed."

# Pass execution to any additional commands
exec "$@"
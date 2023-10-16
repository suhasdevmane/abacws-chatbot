#!/bin/bash

# Wait for the TimescaleDB container to start (adjust the hostname as needed)
while ! nc -z timescaledb 5432; do
  sleep 1
done

# Execute the command to create the TimescaleDB extension
psql -h timescaledb -U postgres -d thingsboard -W -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

echo "TimescaleDB extension has been created."

# Start ThingsBoard
exec /usr/share/thingsboard/bin/run.sh

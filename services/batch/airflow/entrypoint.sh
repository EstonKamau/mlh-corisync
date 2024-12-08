#!/bin/bash

# Initialize the Airflow database
airflow db init

# Create a user if it doesn't already exist
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin_password || echo "User already exists."

# Start the Airflow webserver
echo "Starting Airflow webserver..."
exec airflow webserver &

# Start the Airflow scheduler
echo "Starting Airflow scheduler..."
exec airflow scheduler &

# Start the Airflow worker
echo "Starting Airflow worker..."
exec airflow celery worker
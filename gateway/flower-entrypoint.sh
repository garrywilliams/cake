#!/bin/bash
# celery-entrypoint.sh for Celery service

# # Wait for Postgres to be ready (optional, only if Celery needs to wait for DB)
# /code/wait-for.sh db -- echo "Postgres is up."

# Start the Celery worker
echo "Starting Celery worker..."
celery -A gateway flower --loglevel=info

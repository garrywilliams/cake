#!/bin/bash

# Wait for Postgres to be ready
/code/wait-for.sh db -- echo "Postgres is up."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

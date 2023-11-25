# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Copy entrypoint script into the image and set correct path
COPY entrypoint.sh celery-entrypoint.sh flower-entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh /code/celery-entrypoint.sh /code/flower-entrypoint.sh

# Copy wait-for script into the image
COPY wait-for.sh /code/wait-for.sh
RUN chmod +x /code/wait-for.sh

# Set the working directory to /code
WORKDIR /code

# Set script as entrypoint
# ENTRYPOINT ["/code/entrypoint.sh"]

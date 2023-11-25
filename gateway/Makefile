.PHONY: setup clean test run coverage dependencies dev_dependencies

# Python binaries like python, pip in the venv will take precedence.
VIRTUAL_ENV_DIR = venv
SHELL := /bin/bash  # required for PATH to work
export PATH := $(VIRTUAL_ENV_DIR)/bin:$(PATH)

# Default target
default: dev_dependencies

# Create virtualenv
$(VIRTUAL_ENV_DIR):
	python3 -m venv $(VIRTUAL_ENV_DIR)
	@echo "Virtual environment created."

# Sentinel file for production dependencies
install-requirements: $(VIRTUAL_ENV_DIR) requirements.txt
	@test -f install-requirements || pip install -r requirements.txt
	@test -f install-requirements || touch install-requirements

# Sentinel file for development dependencies
install-requirements-dev: install-requirements requirements-dev.txt
	@test -f install-requirements-dev || pip install -r requirements-dev.txt
	@test -f install-requirements-dev || touch install-requirements-dev

# Install production dependencies
dependencies: install-requirements

# Install development dependencies
dev_dependencies: install-requirements-dev

# Clean up the project
clean:
	rm -rf $(VIRTUAL_ENV_DIR)
	rm -f install-requirements install-requirements-dev
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

# Run tests
test: dev_dependencies
	python manage.py test

# Run the application
run: dependencies migrations
	python manage.py runserver

# Generate coverage report
coverage: dev_dependencies
	coverage run -m pytest
	coverage report
	coverage html

# Lint the code
lint: dev_dependencies
	isort --profile black .
	black . --target-version py310
	flake8 .

# Alembic Migrations
migrations:
	python manage.py migrate

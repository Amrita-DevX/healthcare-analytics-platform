# Makefile - Command shortcuts for common tasks
#
# Why we need this:
#   Instead of typing long commands like:
#     python src/data/make_dataset.py
#   You just type:
#     make data
#
# This is standard in production projects.

# Project configuration
PYTHON = python3
PROJECT_NAME = healthcare-analytics-platform

# Help command (default when you just type 'make')
.PHONY: help
help:
	@echo "$(PROJECT_NAME) - Available Commands"
	@echo "===================================="
	@echo "  make data          - Run data loading pipeline"
	@echo "  make mlflow        - Start MLflow UI"
	@echo "  make clean         - Delete processed data files"
	@echo "  make install       - Install Python dependencies"
	@echo "  make lint          - Check code quality"
	@echo "  make test          - Run unit tests"
	@echo ""

# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt
	@echo "Dependencies installed successfully"

# Run data loading pipeline
.PHONY: data
data:
	@echo "Running data loading pipeline..."
	$(PYTHON) src/data/make_dataset.py
	@echo "Data loading complete"

# Start MLflow UI
.PHONY: mlflow
mlflow:
	@echo "Starting MLflow UI at http://localhost:5000"
	mlflow ui --port 5000

# Clean processed data (keep raw data)
.PHONY: clean
clean:
	@echo "Cleaning processed data..."
	rm -rf data/interim/*
	rm -rf data/processed/*
	rm -rf logs/*
	@echo "Clean complete"

# Run code quality checks
.PHONY: lint
lint:
	@echo "Checking code quality..."
	flake8 src/
	@echo "Lint check complete"

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	pytest tests/
	@echo "Tests complete"

# Create project directories
.PHONY: setup
setup:
	mkdir -p data/raw/interim/processed
	mkdir -p logs
	mkdir -p models
	mkdir -p notebooks
	@echo "Project directories created"

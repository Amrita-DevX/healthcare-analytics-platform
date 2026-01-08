# Makefile - Healthcare Analytics Platform

PYTHON = python3
PROJECT_NAME = healthcare-analytics-platform

.PHONY: help
help:
	@echo "$(PROJECT_NAME) - Available Commands"
	@echo "===================================="
	@echo "  make install       - Install dependencies"
	@echo "  make data          - Run data loading pipeline"
	@echo "  make eda           - Run EDA notebook"
	@echo "  make clean-data    - Run data cleaning notebook"
	@echo "  make pipeline      - Run full pipeline (load + clean)"
	@echo "  make mlflow        - Start MLflow UI"
	@echo "  make jupyter       - Start Jupyter Lab"
	@echo "  make clean         - Delete processed data"
	@echo ""

.PHONY: install
install:
	pip install -r requirements.txt
	@echo "Dependencies installed"

.PHONY: data
data:
	@echo "Running data loading pipeline..."
	$(PYTHON) src/data/make_dataset.py
	@echo "Data loading complete"

.PHONY: eda
eda:
	@echo "Running EDA notebook..."
	jupyter nbconvert --to notebook --execute notebooks/01_eda_platform.ipynb --output 01_eda_platform.ipynb
	@echo "EDA complete"

.PHONY: clean-data
clean-data:
	@echo "Running data cleaning notebook..."
	jupyter nbconvert --to notebook --execute notebooks/02_data_cleaning.ipynb --output 02_data_cleaning.ipynb
	@echo "Data cleaning complete"

.PHONY: pipeline
pipeline: data clean-data
	@echo "Full data pipeline complete"

.PHONY: mlflow
mlflow:
	@echo "Starting MLflow UI..."
	mlflow ui --port 5000

.PHONY: jupyter
jupyter:
	@echo "Starting Jupyter Lab..."
	jupyter lab

.PHONY: clean
clean:
	@echo "Cleaning processed data..."
	rm -rf data/interim/*
	rm -rf data/processed/*
	rm -rf logs/*
	@echo "Clean complete"

.PHONY: setup
setup:
	mkdir -p data/raw data/interim data/processed
	mkdir -p logs models notebooks
	@echo "Project directories created"

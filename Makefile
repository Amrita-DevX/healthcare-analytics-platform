# Why: One command runs everythin.g No manual notebooks!
.PHONY: setup data train-churn test lint

setup:
	pip install -r requirements.txt  # Install deps once

data:
	python src/data/make_dataset.py  # Download + process data

train-churn:
	python src/models/train_churn.py  # Train Module 2 model

test:
	pytest tests/  # Validate pipeline

lint:
	black .  # Format code (install black via pip)

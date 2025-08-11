# Makefile for Aethersheets Project

.PHONY: help install run clean test lint format docker-build docker-run docker-shell

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies using uv"
	@echo "  run          - Run the application"
	@echo "  clean        - Clean cache and temporary files"
	@echo "  test         - Run tests (when available)"
	@echo "  lint         - Run linting (when configured)"
	@echo "  format       - Format code (when configured)"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run application in Docker container"
	@echo "  docker-shell - Start interactive bash shell in Docker container"

# Development commands
install:
	uv sync

run:
	uv run python src/main.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

test:
	@echo "Tests not yet configured"

lint:
	@echo "Linting not yet configured"

format:
	@echo "Code formatting not yet configured"

# Docker commands
docker-build:
	docker build -t aethersheets .

docker-run:
	docker run --rm -it \
		-v $(PWD):/app \
		-v $(PWD)/.env:/app/.env \
		aethersheets \
		uv run python src/main.py

docker-shell:
	docker run --rm -it \
		-v $(PWD):/app \
		-v $(PWD)/.env:/app/.env \
		aethersheets

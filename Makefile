# Makefile for Aethersheets Project

# Include environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help install run clean test lint format docker-build docker-run docker-shell check-env

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies using uv"
	@echo "  run          - Run the application with parameters"
	@echo "  clean        - Clean cache and temporary files"
	@echo "  test         - Run tests (when available)"
	@echo "  lint         - Run linting (when configured)"
	@echo "  format       - Format code (when configured)"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run application in Docker container"
	@echo "  docker-shell - Start interactive bash shell in Docker container"
	@echo ""
	@echo "Run command usage:"
	@echo "  make run SHEET='<spreadsheet_url_or_id>' [INPUT_COL='<column>'] [INPUT_WS='<worksheet>'] [OUTPUT_WS='<worksheet>']"
	@echo ""
	@echo "Examples:"
	@echo "  # With Google Sheets URL:"
	@echo "  make run SHEET='https://docs.google.com/spreadsheets/d/1Jz_FgPhoU5cfWR_vgNIAFrhJu5quipcWVtiM4G6y5fM/edit'"
	@echo ""
	@echo "  # With spreadsheet ID:"
	@echo "  make run SHEET='1Jz_FgPhoU5cfWR_vgNIAFrhJu5quipcWVtiM4G6y5fM'"
	@echo ""
	@echo "  # With custom parameters:"
	@echo "  make run SHEET='https://...' INPUT_COL='Name' INPUT_WS='Companies' OUTPUT_WS='Research'"

# Environment check
check-env:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found!"; \
		echo "Please create a .env file based on .env.sample"; \
		echo "Run: cp .env.sample .env"; \
		echo "Then edit .env with your actual API keys"; \
		exit 1; \
	fi
	@echo "✓ .env file found"
	@echo "OPENAI_API_KEY=$$OPENAI_API_KEY"

# Development commands
install:
	uv sync

run: check-env
	@if [ -z "$(SHEET)" ]; then \
		echo "Error: SHEET parameter is required"; \
		echo "Usage: make run SHEET='<spreadsheet_url_or_id>'"; \
		echo "Run 'make help' for more examples"; \
		exit 1; \
	fi
	@cmd="uv run python src/main.py '$(SHEET)'"; \
	if [ -n "$(INPUT_COL)" ]; then cmd="$$cmd --input-column '$(INPUT_COL)'"; fi; \
	if [ -n "$(INPUT_WS)" ]; then cmd="$$cmd --input-worksheet '$(INPUT_WS)'"; fi; \
	if [ -n "$(OUTPUT_WS)" ]; then cmd="$$cmd --output-worksheet '$(OUTPUT_WS)'"; fi; \
	echo "Executing: $$cmd"; \
	eval $$cmd

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

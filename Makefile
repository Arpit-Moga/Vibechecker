.PHONY: help install test lint format clean build docker-build docker-run dev

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build package"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  dev         - Start development server"

# Installation
install:
	uv sync

install-pip:
	pip install -e .
	pip install -r requirements.txt

# Testing
test:
	pytest

test-cov:
	pytest --cov=src/multiagent_mcp_server --cov-report=html --cov-report=term

test-watch:
	pytest --watch

# Code quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Development
dev:
	python -m multiagent_mcp_server.server

dev-reload:
	uvicorn multiagent_mcp_server.server:app --reload --host 0.0.0.0 --port 8080

# Build and distribution
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

# Docker
docker-build:
	docker build -t multiagent-mcp-server .

docker-run:
	docker run -p 8080:8080 multiagent-mcp-server

docker-dev:
	docker run -p 8080:8080 -v $(PWD):/app multiagent-mcp-server

# Documentation
docs-serve:
	mkdocs serve

docs-build:
	mkdocs build

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

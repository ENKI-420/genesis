.PHONY: all install install-dev test lint format typecheck coverage clean build docs serve help

# Default target
all: lint test

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,cli,docs]"

# Testing
test:
	pytest tests/ -v

test-fast:
	pytest tests/ -v -m "not slow"

test-integration:
	pytest tests/test_integration/ -v

test-coverage:
	pytest tests/ -v --cov=src/genesis --cov-report=html --cov-report=term-missing

coverage: test-coverage

# Code quality
lint:
	ruff check src/ tests/
	mypy src/genesis/

format:
	black src/ tests/
	isort src/ tests/
	ruff check --fix src/ tests/

typecheck:
	mypy src/genesis/

# Combination checks
check: lint typecheck test

# Build
build:
	python -m build

build-wheel:
	python -m build --wheel

# Documentation
docs:
	mkdocs build

docs-serve:
	mkdocs serve

# TypeScript
ts-install:
	cd src/genesis_ts && npm install

ts-build:
	cd src/genesis_ts && npm run build

ts-test:
	cd src/genesis_ts && npm test

# CLI
cli-test:
	genesis --help
	genesis status

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Docker
docker-build:
	docker build -t genesis:latest .

docker-run:
	docker run -it --rm genesis:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

# Release
release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major

# Help
help:
	@echo "GENESIS Sovereign Platform - Make Commands"
	@echo ""
	@echo "Installation:"
	@echo "  install      - Install package"
	@echo "  install-dev  - Install with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         - Run all tests"
	@echo "  test-fast    - Run tests excluding slow ones"
	@echo "  test-integration - Run integration tests"
	@echo "  coverage     - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         - Run linter and type checker"
	@echo "  format       - Format code"
	@echo "  typecheck    - Run mypy type checking"
	@echo "  check        - Run all checks (lint, typecheck, test)"
	@echo ""
	@echo "Build:"
	@echo "  build        - Build package"
	@echo "  build-wheel  - Build wheel only"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         - Build documentation"
	@echo "  docs-serve   - Serve documentation locally"
	@echo ""
	@echo "TypeScript:"
	@echo "  ts-install   - Install TypeScript dependencies"
	@echo "  ts-build     - Build TypeScript package"
	@echo "  ts-test      - Run TypeScript tests"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo ""
	@echo "Utility:"
	@echo "  clean        - Remove build artifacts"
	@echo "  help         - Show this help message"

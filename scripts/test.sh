#!/bin/bash
# GENESIS Test Runner

set -e

echo "Running GENESIS tests..."

# Run pytest with coverage
python -m pytest tests/ \
    -v \
    --tb=short \
    --cov=src/genesis \
    --cov-report=term-missing \
    --cov-report=html:coverage_html \
    "$@"

echo "Tests complete!"

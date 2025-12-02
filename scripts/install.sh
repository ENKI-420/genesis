#!/bin/bash
# GENESIS Installation Script for Linux/macOS

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           GENESIS Installation Script                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python 3.10+ required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python $PYTHON_VERSION detected ✓"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install package
echo "Installing GENESIS..."
pip install -e .

# Install development dependencies (optional)
if [ "$1" == "--dev" ]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev]"
fi

# Install CLI dependencies (optional)
if [ "$1" == "--cli" ] || [ "$2" == "--cli" ]; then
    echo "Installing CLI dependencies..."
    pip install -e ".[cli]"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           Installation Complete!                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "To activate: source .venv/bin/activate"
echo "To run CLI: genesis --help"
echo "To run tests: pytest"

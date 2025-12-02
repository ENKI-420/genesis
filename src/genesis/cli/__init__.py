"""
GENESIS CLI Module

This module provides the command-line interface for the GENESIS platform.
It includes:

- Main entry point
- Subcommands for all operations
- Terminal UI (TUI) for interactive use
"""

from genesis.cli.main import main, cli

__all__ = [
    "main",
    "cli",
]

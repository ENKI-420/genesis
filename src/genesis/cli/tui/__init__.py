"""
GENESIS Terminal UI (TUI) Module

This package contains the Terminal User Interface for GENESIS,
providing an interactive dashboard for monitoring and control.

Note: The full TUI requires the 'textual' optional dependency.
"""

from genesis.cli.tui.app import GenesisApp
from genesis.cli.tui.dashboard import DashboardScreen
from genesis.cli.tui.widgets import CCCEWidget, AgentStatusWidget

__all__ = [
    "GenesisApp",
    "DashboardScreen",
    "CCCEWidget",
    "AgentStatusWidget",
]

"""
GENESIS TUI Application

The main TUI application class for GENESIS. This provides an interactive
terminal interface for monitoring and controlling the GENESIS platform.

Note: This requires the 'textual' package for full functionality.
A fallback mode is provided for basic terminal support.
"""

from typing import Optional

# Try to import textual, fall back to basic mode if not available
try:
    from textual.app import App
    from textual.widgets import Header, Footer
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    App = object  # type: ignore


class GenesisApp(App if TEXTUAL_AVAILABLE else object):
    """
    GENESIS Terminal User Interface Application.
    
    Provides an interactive dashboard for:
    - Real-time CCCE metrics
    - Agent status monitoring
    - Portal management
    - System configuration
    
    If textual is not installed, falls back to basic terminal output.
    """
    
    TITLE = "GENESIS Sovereign Quantum Platform"
    CSS_PATH = None
    
    def __init__(self) -> None:
        """Initialize the GENESIS TUI application."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
        self.running = False
    
    def compose(self):
        """Compose the application layout."""
        if not TEXTUAL_AVAILABLE:
            return
        
        from textual.widgets import Header, Footer
        from genesis.cli.tui.dashboard import DashboardScreen
        
        yield Header()
        yield DashboardScreen()
        yield Footer()
    
    def run_basic(self) -> None:
        """Run in basic mode without textual."""
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║           GENESIS Terminal User Interface                 ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print("║                                                           ║")
        print("║  Note: Full TUI requires 'textual' package.               ║")
        print("║  Install with: pip install genesis-sovereign[cli]         ║")
        print("║                                                           ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print("║                    System Status                          ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        
        from genesis.constants import LAMBDA_PHI, PSI_STAR
        
        print(f"║  Λ_Φ = {LAMBDA_PHI:.6e}                               ║")
        print(f"║  Ψ* = {PSI_STAR:.3f}                                        ║")
        print("║                                                           ║")
        print("║  Agents: AIDEN ✓ AURA ✓ PALS ✓ CHRONOS ✓ AEGIS ✓         ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
    
    def start(self) -> None:
        """Start the TUI application."""
        if TEXTUAL_AVAILABLE:
            self.run()
        else:
            self.run_basic()


def run_tui() -> None:
    """Run the GENESIS TUI application."""
    app = GenesisApp()
    app.start()


if __name__ == "__main__":
    run_tui()

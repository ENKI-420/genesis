"""
GENESIS Dashboard Screen

The main dashboard screen for the GENESIS TUI, showing:
- CCCE metrics in real-time
- Agent status
- Portal status
- System health
"""

from typing import Optional

# Try to import textual, fall back to basic mode
try:
    from textual.app import ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.screen import Screen
    from textual.widgets import Static, Label
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    Screen = object  # type: ignore
    ComposeResult = None  # type: ignore


class DashboardScreen(Screen if TEXTUAL_AVAILABLE else object):
    """
    Main dashboard screen for GENESIS TUI.
    
    Displays:
    - Header with title and version
    - CCCE metrics panel
    - Agent status panel
    - Portal status panel
    - System log
    """
    
    def __init__(self) -> None:
        """Initialize the dashboard screen."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
    
    def compose(self) -> "ComposeResult":
        """Compose the dashboard layout."""
        if not TEXTUAL_AVAILABLE:
            return
        
        from textual.containers import Container, Horizontal, Vertical
        from textual.widgets import Static, Label
        from genesis.cli.tui.widgets import CCCEWidget, AgentStatusWidget
        
        with Container():
            yield Static("╔══════════════════════════════════════════╗")
            yield Static("║    GENESIS Sovereign Quantum Platform    ║")
            yield Static("╚══════════════════════════════════════════╝")
            
            with Horizontal():
                yield CCCEWidget()
                yield AgentStatusWidget()
    
    def render_basic(self) -> str:
        """Render basic text output."""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                 GENESIS Dashboard                                 ║
╠══════════════════════════════════════════════════════════════════╣
║  CCCE Metrics          │  Agent Status                           ║
║  ─────────────────────┼───────────────────────────────────       ║
║  Ξ = 7.6500           │  AIDEN    ● Online                       ║
║  Λ = 0.8500           │  AURA     ● Online                       ║
║  Φ = 0.9000           │  PALS     ● Online                       ║
║  Γ = 0.1000           │  CHRONOS  ● Online                       ║
║                        │  AEGIS    ● Online                       ║
╠══════════════════════════════════════════════════════════════════╣
║  Portal Status                                                    ║
║  ─────────────────────────────────────────────────────────       ║
║  Enterprise: Ready    Defense: Ready    Health: Ready            ║
║  Legal: Ready         DARPA: Ready                               ║
╚══════════════════════════════════════════════════════════════════╝
"""


class MetricsPanel:
    """
    Panel for displaying CCCE metrics.
    
    Shows real-time values of:
    - Ξ (CCCE value)
    - Λ (Consciousness)
    - Φ (Coherence)
    - Γ (Decoherence)
    """
    
    def __init__(self) -> None:
        """Initialize the metrics panel."""
        self.xi = 0.0
        self.consciousness = 0.0
        self.coherence = 0.0
        self.decoherence = 0.0
    
    def update(
        self,
        consciousness: float,
        coherence: float,
        decoherence: float,
    ) -> None:
        """Update metric values."""
        self.consciousness = consciousness
        self.coherence = coherence
        self.decoherence = decoherence
        
        if decoherence > 0:
            self.xi = (consciousness * coherence) / decoherence
        else:
            self.xi = float('inf')
    
    def render(self) -> str:
        """Render the metrics panel."""
        lines = [
            "┌─ CCCE Metrics ─────────┐",
            f"│ Ξ = {self.xi:8.4f}          │",
            f"│ Λ = {self.consciousness:8.4f}          │",
            f"│ Φ = {self.coherence:8.4f}          │",
            f"│ Γ = {self.decoherence:8.4f}          │",
            "└─────────────────────────┘",
        ]
        return "\n".join(lines)


class AgentPanel:
    """
    Panel for displaying agent status.
    """
    
    AGENTS = ["AIDEN", "AURA", "PALS", "CHRONOS", "AEGIS"]
    
    def __init__(self) -> None:
        """Initialize the agent panel."""
        self.status = {agent: "online" for agent in self.AGENTS}
    
    def set_status(self, agent: str, status: str) -> None:
        """Set agent status."""
        if agent in self.status:
            self.status[agent] = status
    
    def render(self) -> str:
        """Render the agent panel."""
        lines = ["┌─ Agent Status ─────────┐"]
        
        for agent in self.AGENTS:
            status = self.status.get(agent, "unknown")
            icon = "●" if status == "online" else "○"
            lines.append(f"│ {agent:8} {icon} {status:8} │")
        
        lines.append("└─────────────────────────┘")
        return "\n".join(lines)


class PortalPanel:
    """
    Panel for displaying portal status.
    """
    
    PORTALS = ["enterprise", "defense", "health", "legal", "darpa"]
    
    def __init__(self) -> None:
        """Initialize the portal panel."""
        self.status = {portal: "ready" for portal in self.PORTALS}
    
    def render(self) -> str:
        """Render the portal panel."""
        lines = ["┌─ Portal Status ─────────────────────────────┐"]
        
        row = "│ "
        for i, portal in enumerate(self.PORTALS):
            status = self.status.get(portal, "unknown")
            row += f"{portal.title()}: {status}  "
            if (i + 1) % 3 == 0:
                row = row.rstrip() + " │"
                lines.append(row)
                row = "│ "
        
        if row != "│ ":
            row = row.rstrip().ljust(45) + " │"
            lines.append(row)
        
        lines.append("└──────────────────────────────────────────────┘")
        return "\n".join(lines)

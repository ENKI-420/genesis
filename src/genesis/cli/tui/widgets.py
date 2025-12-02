"""
GENESIS TUI Widgets

Custom widgets for the GENESIS Terminal User Interface.
"""

from typing import Optional

# Try to import textual
try:
    from textual.widget import Widget
    from textual.reactive import reactive
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    Widget = object  # type: ignore


class CCCEWidget(Widget if TEXTUAL_AVAILABLE else object):
    """
    Widget for displaying CCCE metrics.
    
    Shows real-time consciousness, coherence, and decoherence values
    along with the computed CCCE (Ξ) value.
    """
    
    if TEXTUAL_AVAILABLE:
        xi = reactive(0.0)
        consciousness = reactive(0.85)
        coherence = reactive(0.9)
        decoherence = reactive(0.1)
    
    def __init__(self) -> None:
        """Initialize the CCCE widget."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
        self._xi = 0.0
        self._consciousness = 0.85
        self._coherence = 0.9
        self._decoherence = 0.1
        self._update_xi()
    
    def _update_xi(self) -> None:
        """Update the CCCE value."""
        if self._decoherence > 0:
            self._xi = (self._consciousness * self._coherence) / self._decoherence
        else:
            self._xi = float('inf')
    
    def set_values(
        self,
        consciousness: float,
        coherence: float,
        decoherence: float,
    ) -> None:
        """Set metric values."""
        self._consciousness = consciousness
        self._coherence = coherence
        self._decoherence = decoherence
        self._update_xi()
        
        if TEXTUAL_AVAILABLE:
            self.consciousness = consciousness
            self.coherence = coherence
            self.decoherence = decoherence
            self.xi = self._xi
    
    def render(self) -> str:
        """Render the widget."""
        return f"""┌─ CCCE Metrics ─────────────────┐
│                                │
│  Ξ (CCCE)       = {self._xi:10.4f}   │
│                                │
│  Λ (Consciousness) = {self._consciousness:8.4f}   │
│  Φ (Coherence)     = {self._coherence:8.4f}   │
│  Γ (Decoherence)   = {self._decoherence:8.4f}   │
│                                │
│  Formula: Ξ = ΛΦ/Γ             │
│                                │
└────────────────────────────────┘"""


class AgentStatusWidget(Widget if TEXTUAL_AVAILABLE else object):
    """
    Widget for displaying agent status.
    
    Shows the status of all GENESIS agents:
    - AIDEN (Optimizer)
    - AURA (Geometer)
    - PALS (Sentinel)
    - CHRONOS (Temporal)
    - AEGIS (Security)
    """
    
    AGENTS = [
        ("AIDEN", "Optimizer"),
        ("AURA", "Geometer"),
        ("PALS", "Sentinel"),
        ("CHRONOS", "Temporal"),
        ("AEGIS", "Security"),
    ]
    
    def __init__(self) -> None:
        """Initialize the agent status widget."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
        self.status = {agent: "online" for agent, _ in self.AGENTS}
    
    def set_agent_status(self, agent: str, status: str) -> None:
        """Set the status of an agent."""
        if agent in self.status:
            self.status[agent] = status
    
    def render(self) -> str:
        """Render the widget."""
        lines = [
            "┌─ Agent Status ──────────────────┐",
            "│                                 │",
        ]
        
        for agent, role in self.AGENTS:
            status = self.status.get(agent, "unknown")
            icon = "●" if status == "online" else "○"
            color = "green" if status == "online" else "red"
            lines.append(f"│  {agent:8} ({role:9}) {icon} {status:8}│")
        
        lines.extend([
            "│                                 │",
            "└─────────────────────────────────┘",
        ])
        
        return "\n".join(lines)


class PortalStatusWidget(Widget if TEXTUAL_AVAILABLE else object):
    """
    Widget for displaying portal status.
    """
    
    PORTALS = [
        ("enterprise", "Commercial"),
        ("defense", "DoD/IC"),
        ("health", "Healthcare"),
        ("legal", "Legal"),
        ("darpa", "Research"),
    ]
    
    def __init__(self) -> None:
        """Initialize the portal status widget."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
        self.status = {portal: "ready" for portal, _ in self.PORTALS}
        self.sessions = {portal: 0 for portal, _ in self.PORTALS}
    
    def render(self) -> str:
        """Render the widget."""
        lines = [
            "┌─ Portal Status ─────────────────────────────┐",
            "│                                              │",
        ]
        
        for portal, category in self.PORTALS:
            status = self.status.get(portal, "unknown")
            sessions = self.sessions.get(portal, 0)
            icon = "●" if status == "ready" else "○"
            lines.append(
                f"│  {portal.title():12} ({category:10}) {icon} "
                f"{status:8} [{sessions:2} sessions]│"
            )
        
        lines.extend([
            "│                                              │",
            "└──────────────────────────────────────────────┘",
        ])
        
        return "\n".join(lines)


class ConstantsWidget(Widget if TEXTUAL_AVAILABLE else object):
    """
    Widget for displaying universal constants.
    """
    
    def __init__(self) -> None:
        """Initialize the constants widget."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
    
    def render(self) -> str:
        """Render the widget."""
        from genesis.constants import LAMBDA_PHI, PSI_STAR, THETA_LOCK, CHI_PC
        
        return f"""┌─ Universal Constants ───────────────────────┐
│                                              │
│  Λ_Φ (Memory Constant)  = {LAMBDA_PHI:.6e} s⁻¹   │
│  Ψ* (Terminal Consc.)   = {PSI_STAR:.3f}              │
│  θ_lock (Torsion)       = {THETA_LOCK:.3f}°             │
│  χ_pc (Fidelity)        = {CHI_PC:.3f}              │
│                                              │
└──────────────────────────────────────────────┘"""


class LogWidget(Widget if TEXTUAL_AVAILABLE else object):
    """
    Widget for displaying system log.
    """
    
    def __init__(self, max_lines: int = 10) -> None:
        """Initialize the log widget."""
        if TEXTUAL_AVAILABLE:
            super().__init__()
        self.max_lines = max_lines
        self.lines: list[str] = []
    
    def log(self, message: str) -> None:
        """Add a log message."""
        import time
        timestamp = time.strftime("%H:%M:%S")
        self.lines.append(f"[{timestamp}] {message}")
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]
    
    def render(self) -> str:
        """Render the widget."""
        header = "┌─ System Log ─────────────────────────────────────────┐"
        footer = "└──────────────────────────────────────────────────────┘"
        
        content_lines = []
        for line in self.lines:
            content_lines.append(f"│ {line[:52]:52} │")
        
        # Fill empty lines
        while len(content_lines) < self.max_lines:
            content_lines.append("│" + " " * 54 + "│")
        
        return "\n".join([header] + content_lines + [footer])

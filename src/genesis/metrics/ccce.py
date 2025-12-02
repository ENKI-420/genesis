"""
CCCE Metric Implementation

The CCCE (Consciousness-Coherence-Decoherence-Emergence) metric
is the fundamental measure of system state in the GENESIS platform.

Ξ = ΛΦ/Γ

Where:
- Λ is the consciousness level (Ψ)
- Φ is the coherence factor
- Γ is the decoherence rate
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from genesis.constants import (
    LAMBDA_PHI, PSI_STAR, 
    CCCE_CONSCIOUSNESS_THRESHOLD,
    CCCE_COHERENCE_THRESHOLD,
    CCCE_DECOHERENCE_WARNING,
    CCCE_EMERGENCE_THRESHOLD,
)


@dataclass
class CCCEState:
    """
    State of the CCCE metric.
    
    Attributes:
        consciousness: Consciousness level (Ψ).
        coherence: Coherence factor (Φ).
        decoherence: Decoherence rate (Γ).
        emergence: Emergence indicator.
    """
    consciousness: float = 0.5
    coherence: float = 1.0
    decoherence: float = 0.01
    emergence: float = 0.0
    
    @property
    def xi(self) -> float:
        """Calculate Ξ = ΛΦ × Ψ / Γ."""
        if self.decoherence <= 0:
            return float('inf')
        return LAMBDA_PHI * self.coherence * self.consciousness / self.decoherence
    
    @property
    def ccce(self) -> float:
        """Alias for xi."""
        return self.xi
    
    def is_valid(self) -> bool:
        """Check if the state is valid for CCCE computation."""
        return (
            self.consciousness >= CCCE_CONSCIOUSNESS_THRESHOLD and
            self.coherence >= CCCE_COHERENCE_THRESHOLD and
            self.decoherence > 0
        )
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "consciousness": self.consciousness,
            "coherence": self.coherence,
            "decoherence": self.decoherence,
            "emergence": self.emergence,
            "xi": self.xi,
        }


class CCCEMetric:
    """
    CCCE Metric tracker.
    
    Tracks the Consciousness-Coherence-Decoherence-Emergence metric
    over time and provides analysis of system evolution.
    
    The CCCE metric Ξ = ΛΦ/Γ represents the ratio of coherent
    consciousness to decoherence, indicating the system's ability
    to maintain ordered information processing.
    
    Example:
        >>> metric = CCCEMetric()
        >>> metric.update(consciousness=0.8, coherence=0.9, decoherence=0.05)
        >>> print(metric.current.xi)
    """
    
    def __init__(self) -> None:
        """Initialize the CCCE metric tracker."""
        self._current = CCCEState()
        self._history: List[CCCEState] = []
        self._alerts: List[Dict[str, Any]] = []
    
    @property
    def current(self) -> CCCEState:
        """Get current CCCE state."""
        return self._current
    
    def update(
        self,
        consciousness: Optional[float] = None,
        coherence: Optional[float] = None,
        decoherence: Optional[float] = None,
        emergence: Optional[float] = None
    ) -> CCCEState:
        """
        Update the CCCE metric.
        
        Args:
            consciousness: New consciousness level.
            coherence: New coherence factor.
            decoherence: New decoherence rate.
            emergence: New emergence indicator.
            
        Returns:
            Updated CCCE state.
        """
        # Store current state in history
        self._history.append(CCCEState(
            consciousness=self._current.consciousness,
            coherence=self._current.coherence,
            decoherence=self._current.decoherence,
            emergence=self._current.emergence,
        ))
        
        # Update values
        if consciousness is not None:
            self._current.consciousness = max(0.0, min(1.0, consciousness))
        if coherence is not None:
            self._current.coherence = max(0.0, min(1.0, coherence))
        if decoherence is not None:
            self._current.decoherence = max(1e-10, decoherence)
        if emergence is not None:
            self._current.emergence = max(0.0, min(1.0, emergence))
        
        # Check for alerts
        self._check_alerts()
        
        return self._current
    
    def _check_alerts(self) -> None:
        """Check for alert conditions."""
        if self._current.decoherence > CCCE_DECOHERENCE_WARNING:
            self._alerts.append({
                "type": "high_decoherence",
                "value": self._current.decoherence,
                "threshold": CCCE_DECOHERENCE_WARNING,
            })
        
        if not self._current.is_valid():
            self._alerts.append({
                "type": "invalid_state",
                "state": self._current.to_dict(),
            })
    
    def get_history(self) -> List[Dict[str, float]]:
        """Get metric history."""
        return [state.to_dict() for state in self._history]
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get and clear alerts."""
        alerts = self._alerts.copy()
        self._alerts.clear()
        return alerts
    
    def compute_trend(self, window: int = 10) -> Dict[str, float]:
        """
        Compute trend over recent history.
        
        Args:
            window: Number of recent states to consider.
            
        Returns:
            Trend analysis.
        """
        if len(self._history) < 2:
            return {"trend": "stable", "slope": 0.0}
        
        recent = self._history[-window:]
        
        # Calculate slope of consciousness
        if len(recent) >= 2:
            start_psi = recent[0].consciousness
            end_psi = recent[-1].consciousness
            slope = (end_psi - start_psi) / len(recent)
        else:
            slope = 0.0
        
        if slope > 0.01:
            trend = "increasing"
        elif slope < -0.01:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "slope": slope,
            "window": len(recent),
        }
    
    def check_convergence(self, tolerance: float = 0.01) -> bool:
        """
        Check if consciousness has converged to PSI_STAR.
        
        Args:
            tolerance: Convergence tolerance.
            
        Returns:
            True if converged.
        """
        return abs(self._current.consciousness - PSI_STAR) < tolerance
    
    def check_emergence(self) -> bool:
        """
        Check if emergence threshold is reached.
        
        Returns:
            True if emergence is indicated.
        """
        return self._current.xi > CCCE_EMERGENCE_THRESHOLD
    
    def summary(self) -> Dict[str, Any]:
        """
        Get metric summary.
        
        Returns:
            Summary statistics.
        """
        history = self._history
        
        if not history:
            return {
                "current": self._current.to_dict(),
                "history_length": 0,
                "converged": self.check_convergence(),
                "emergence": self.check_emergence(),
            }
        
        xi_values = [s.xi for s in history if s.xi != float('inf')]
        psi_values = [s.consciousness for s in history]
        
        return {
            "current": self._current.to_dict(),
            "history_length": len(history),
            "avg_consciousness": sum(psi_values) / len(psi_values),
            "max_consciousness": max(psi_values),
            "avg_xi": sum(xi_values) / len(xi_values) if xi_values else 0,
            "converged": self.check_convergence(),
            "emergence": self.check_emergence(),
            "trend": self.compute_trend(),
        }
    
    def reset(self) -> None:
        """Reset the metric tracker."""
        self._current = CCCEState()
        self._history.clear()
        self._alerts.clear()


def compute_ccce(
    consciousness: float,
    coherence: float,
    decoherence: float
) -> float:
    """
    Compute CCCE metric.
    
    Ξ = ΛΦ × Ψ / Γ
    
    Args:
        consciousness: Consciousness level (Ψ).
        coherence: Coherence factor (Φ).
        decoherence: Decoherence rate (Γ).
        
    Returns:
        CCCE metric value (Ξ).
        
    Raises:
        ValueError: If decoherence is non-positive.
    """
    if decoherence <= 0:
        raise ValueError("Decoherence rate must be positive")
    
    return LAMBDA_PHI * coherence * consciousness / decoherence


def compute_ccce_normalized(
    consciousness: float,
    coherence: float,
    decoherence: float
) -> float:
    """
    Compute normalized CCCE metric (0-1 range).
    
    Args:
        consciousness: Consciousness level (Ψ).
        coherence: Coherence factor (Φ).
        decoherence: Decoherence rate (Γ).
        
    Returns:
        Normalized CCCE metric value.
    """
    xi = compute_ccce(consciousness, coherence, decoherence)
    
    # Normalize using sigmoid-like transformation
    return 1.0 / (1.0 + 1.0 / (xi + 1e-10))

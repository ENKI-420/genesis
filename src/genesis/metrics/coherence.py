"""
Coherence Metrics

Provides tools for measuring and tracking quantum coherence
in the GENESIS platform.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from genesis.constants import CHI_PC


@dataclass
class CoherenceState:
    """
    State of quantum coherence.
    
    Attributes:
        coherence: Primary coherence value (0-1).
        fidelity: Gate fidelity.
        purity: State purity.
        entanglement: Entanglement measure.
    """
    coherence: float = 1.0
    fidelity: float = 1.0
    purity: float = 1.0
    entanglement: float = 0.0


class CoherenceMetric:
    """
    Tracks quantum coherence metrics.
    
    Monitors coherence, fidelity, purity, and entanglement
    to assess the quantum state quality of organisms.
    
    Example:
        >>> metric = CoherenceMetric()
        >>> metric.update(coherence=0.95, fidelity=0.99)
        >>> print(metric.quality_score())
    """
    
    def __init__(self) -> None:
        """Initialize the coherence metric."""
        self._current = CoherenceState()
        self._history: List[CoherenceState] = []
    
    @property
    def current(self) -> CoherenceState:
        """Get current coherence state."""
        return self._current
    
    def update(
        self,
        coherence: Optional[float] = None,
        fidelity: Optional[float] = None,
        purity: Optional[float] = None,
        entanglement: Optional[float] = None
    ) -> CoherenceState:
        """
        Update coherence metrics.
        
        Args:
            coherence: New coherence value.
            fidelity: New fidelity value.
            purity: New purity value.
            entanglement: New entanglement value.
            
        Returns:
            Updated state.
        """
        self._history.append(CoherenceState(
            coherence=self._current.coherence,
            fidelity=self._current.fidelity,
            purity=self._current.purity,
            entanglement=self._current.entanglement,
        ))
        
        if coherence is not None:
            self._current.coherence = max(0.0, min(1.0, coherence))
        if fidelity is not None:
            self._current.fidelity = max(0.0, min(1.0, fidelity))
        if purity is not None:
            self._current.purity = max(0.0, min(1.0, purity))
        if entanglement is not None:
            self._current.entanglement = max(0.0, min(1.0, entanglement))
        
        return self._current
    
    def apply_decoherence(self, rate: float) -> float:
        """
        Apply decoherence to current state.
        
        Args:
            rate: Decoherence rate (Γ).
            
        Returns:
            New coherence value.
        """
        new_coherence = self._current.coherence * (1 - rate)
        self.update(coherence=new_coherence)
        return new_coherence
    
    def quality_score(self) -> float:
        """
        Calculate overall quality score.
        
        Combines coherence, fidelity, and purity into
        a single quality metric.
        
        Returns:
            Quality score (0-1).
        """
        return (
            0.4 * self._current.coherence +
            0.3 * self._current.fidelity +
            0.3 * self._current.purity
        )
    
    def phase_conjugate_fidelity(self) -> float:
        """
        Calculate phase conjugate fidelity.
        
        Compares current fidelity to theoretical maximum χ_pc.
        
        Returns:
            Ratio to theoretical maximum.
        """
        return self._current.fidelity / CHI_PC
    
    def coherence_time(self, rate: float) -> float:
        """
        Estimate coherence time.
        
        T2 = 1 / Γ
        
        Args:
            rate: Decoherence rate.
            
        Returns:
            Estimated coherence time.
        """
        if rate <= 0:
            return float('inf')
        return 1.0 / rate
    
    def get_history(self) -> List[Dict[str, float]]:
        """Get coherence history."""
        return [
            {
                "coherence": s.coherence,
                "fidelity": s.fidelity,
                "purity": s.purity,
                "entanglement": s.entanglement,
            }
            for s in self._history
        ]
    
    def decay_trend(self, window: int = 10) -> float:
        """
        Calculate coherence decay trend.
        
        Args:
            window: Number of recent states.
            
        Returns:
            Decay rate (negative = decay).
        """
        if len(self._history) < 2:
            return 0.0
        
        recent = self._history[-window:]
        
        if len(recent) < 2:
            return 0.0
        
        start_coherence = recent[0].coherence
        end_coherence = recent[-1].coherence
        
        return (end_coherence - start_coherence) / len(recent)
    
    def summary(self) -> Dict[str, Any]:
        """Get coherence summary."""
        return {
            "current": {
                "coherence": self._current.coherence,
                "fidelity": self._current.fidelity,
                "purity": self._current.purity,
                "entanglement": self._current.entanglement,
            },
            "quality_score": self.quality_score(),
            "phase_conjugate_ratio": self.phase_conjugate_fidelity(),
            "history_length": len(self._history),
            "decay_trend": self.decay_trend(),
        }
    
    def reset(self) -> None:
        """Reset the metric."""
        self._current = CoherenceState()
        self._history.clear()


def measure_coherence_from_state(amplitudes: List[complex]) -> float:
    """
    Measure coherence from quantum state amplitudes.
    
    Uses the l1-norm of coherence.
    
    Args:
        amplitudes: Complex amplitudes.
        
    Returns:
        Coherence measure.
    """
    n = len(amplitudes)
    if n <= 1:
        return 0.0
    
    # Sum of off-diagonal density matrix elements
    total = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                rho_ij = amplitudes[i] * amplitudes[j].conjugate()
                total += abs(rho_ij)
    
    # Normalize
    max_coherence = n * (n - 1)
    return total / max_coherence if max_coherence > 0 else 0.0


def measure_purity_from_state(amplitudes: List[complex]) -> float:
    """
    Measure purity from quantum state amplitudes.
    
    For a pure state, Tr(ρ²) = 1.
    
    Args:
        amplitudes: Complex amplitudes.
        
    Returns:
        Purity measure (1 for pure state).
    """
    # For a pure state described by amplitudes, purity is always 1
    # This would be different for mixed states (density matrices)
    norm_sq = sum(abs(a) ** 2 for a in amplitudes)
    return 1.0 if abs(norm_sq - 1.0) < 1e-10 else norm_sq

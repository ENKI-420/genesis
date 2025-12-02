"""
Persistence Functional

Implements the persistence functional for tracking and maintaining
the stability of memory and consciousness states.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from genesis.constants import LAMBDA_PHI, PSI_STAR
from genesis.memory.kernel import MemoryKernel
import genesis.core.math as gmath


@dataclass
class PersistenceState:
    """
    State of the persistence functional.
    
    Attributes:
        value: Current persistence value.
        stability: Stability measure.
        entropy: Information entropy.
        tau: Current temporal coordinate.
    """
    value: float = 0.0
    stability: float = 1.0
    entropy: float = 0.0
    tau: float = 0.0


class PersistenceFunctional:
    """
    Persistence functional for memory and consciousness stability.
    
    The persistence functional P[Ψ] measures the integrated stability
    of the consciousness field over time:
    
    P[Ψ] = ∫ K(τ,τ') Ψ(τ') dτ'
    
    Higher persistence indicates more stable, coherent evolution.
    
    Example:
        >>> functional = PersistenceFunctional()
        >>> functional.record(0.5, tau=0.0)
        >>> functional.record(0.7, tau=1.0)
        >>> print(functional.compute())
    """
    
    def __init__(
        self,
        kernel: Optional[MemoryKernel] = None
    ) -> None:
        """
        Initialize the persistence functional.
        
        Args:
            kernel: Memory kernel to use.
        """
        self.kernel = kernel or MemoryKernel()
        self._history: List[tuple] = []  # (tau, value)
        self._state = PersistenceState()
    
    def record(self, value: float, tau: float) -> None:
        """
        Record a value at a given time.
        
        Args:
            value: Value to record.
            tau: Temporal coordinate.
        """
        self._history.append((tau, value))
        self._state.tau = tau
    
    def compute(self, tau: Optional[float] = None) -> float:
        """
        Compute the persistence functional at time tau.
        
        P[Ψ](τ) = Σ K(τ, τ_i) × Ψ(τ_i)
        
        Args:
            tau: Time at which to evaluate (default: latest).
            
        Returns:
            Persistence functional value.
        """
        if not self._history:
            return 0.0
        
        if tau is None:
            tau = self._state.tau
        
        times = [t for t, _ in self._history]
        values = [v for _, v in self._history]
        
        persistence = self.kernel.convolve(values, times, tau)
        
        # Normalize by the sum of kernel values
        norm = sum(self.kernel(tau, t) for t in times)
        if norm > 0:
            persistence /= norm
        
        self._state.value = persistence
        return persistence
    
    def compute_stability(self) -> float:
        """
        Compute stability measure.
        
        Stability is based on the variance of persistence over time.
        
        Returns:
            Stability measure (0 = unstable, 1 = stable).
        """
        if len(self._history) < 2:
            return 1.0
        
        values = [v for _, v in self._history]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        
        # Convert variance to stability (high variance = low stability)
        stability = 1.0 / (1.0 + variance)
        
        self._state.stability = stability
        return stability
    
    def compute_entropy(self) -> float:
        """
        Compute information entropy of the history.
        
        Returns:
            Shannon entropy.
        """
        if len(self._history) < 2:
            return 0.0
        
        values = [v for _, v in self._history]
        
        # Normalize to get probabilities
        total = sum(abs(v) for v in values)
        if total == 0:
            return 0.0
        
        probs = [abs(v) / total for v in values]
        
        # Shannon entropy: -Σ p log(p)
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * gmath.ln(p)
        
        self._state.entropy = entropy
        return entropy
    
    def convergence_to_target(self, target: float = PSI_STAR) -> float:
        """
        Compute convergence toward target value.
        
        Args:
            target: Target value.
            
        Returns:
            Convergence measure (1 = converged).
        """
        if not self._history:
            return 0.0
        
        current_value = self._history[-1][1]
        distance = abs(current_value - target)
        
        return 1.0 / (1.0 + distance)
    
    def rate_of_change(self) -> float:
        """
        Compute current rate of change.
        
        Returns:
            dP/dτ.
        """
        if len(self._history) < 2:
            return 0.0
        
        tau1, v1 = self._history[-2]
        tau2, v2 = self._history[-1]
        
        if tau2 == tau1:
            return 0.0
        
        return (v2 - v1) / (tau2 - tau1)
    
    def get_state(self) -> PersistenceState:
        """Get current persistence state."""
        self.compute()
        self.compute_stability()
        self.compute_entropy()
        return self._state
    
    def get_history(self) -> List[Dict[str, float]]:
        """Get persistence history."""
        return [
            {"tau": tau, "value": value}
            for tau, value in self._history
        ]
    
    def summary(self) -> Dict[str, Any]:
        """Get persistence summary."""
        return {
            "persistence": self.compute(),
            "stability": self.compute_stability(),
            "entropy": self.compute_entropy(),
            "convergence": self.convergence_to_target(),
            "rate_of_change": self.rate_of_change(),
            "history_length": len(self._history),
        }
    
    def reset(self) -> None:
        """Reset the functional."""
        self._history.clear()
        self._state = PersistenceState()


def compute_persistence_integral(
    psi: Callable[[float], float],
    tau: float,
    tau_min: float = 0.0,
    tau_max: Optional[float] = None,
    kernel: Optional[MemoryKernel] = None
) -> float:
    """
    Compute the persistence integral.
    
    P[Ψ](τ) = ∫_{τ_min}^{τ} K(τ,τ') Ψ(τ') dτ'
    
    Args:
        psi: Consciousness function Ψ(τ').
        tau: Current time.
        tau_min: Lower integration bound.
        tau_max: Upper integration bound (default: tau).
        kernel: Memory kernel.
        
    Returns:
        Persistence integral value.
    """
    if tau_max is None:
        tau_max = tau
    
    kernel = kernel or MemoryKernel()
    return kernel.integrate(psi, tau, tau_min, tau_max)

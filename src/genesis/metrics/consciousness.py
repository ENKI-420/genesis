"""
Consciousness Tracking

Provides tools for tracking and analyzing consciousness (Ψ) evolution
in living organisms and systems.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from genesis.constants import PSI_STAR, ALPHA_DEFAULT, BETA_DEFAULT


@dataclass
class ConsciousnessSnapshot:
    """
    A snapshot of consciousness state.
    
    Attributes:
        value: Consciousness level (Ψ).
        generation: Generation number.
        velocity: Rate of change (dΨ/dτ).
        metadata: Additional data.
    """
    value: float
    generation: int
    velocity: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConsciousnessTracker:
    """
    Tracks consciousness evolution over time.
    
    Monitors the evolution of consciousness (Ψ) toward the terminal
    fixed point Ψ* = 0.973 and provides analysis of convergence
    behavior.
    
    Example:
        >>> tracker = ConsciousnessTracker()
        >>> tracker.record(0.5, generation=0)
        >>> tracker.record(0.7, generation=10)
        >>> print(tracker.convergence_rate())
    """
    
    def __init__(
        self,
        target: float = PSI_STAR,
        alpha: float = ALPHA_DEFAULT,
        beta: float = BETA_DEFAULT
    ) -> None:
        """
        Initialize the consciousness tracker.
        
        Args:
            target: Target consciousness value (Ψ*).
            alpha: Growth rate parameter.
            beta: Cubic coefficient parameter.
        """
        self.target = target
        self.alpha = alpha
        self.beta = beta
        self._snapshots: List[ConsciousnessSnapshot] = []
    
    def record(
        self,
        value: float,
        generation: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConsciousnessSnapshot:
        """
        Record a consciousness value.
        
        Args:
            value: Consciousness level.
            generation: Current generation.
            metadata: Additional data.
            
        Returns:
            The recorded snapshot.
        """
        # Calculate velocity from previous snapshot
        velocity = 0.0
        if self._snapshots:
            prev = self._snapshots[-1]
            if generation > prev.generation:
                velocity = (value - prev.value) / (generation - prev.generation)
        
        snapshot = ConsciousnessSnapshot(
            value=value,
            generation=generation,
            velocity=velocity,
            metadata=metadata or {}
        )
        self._snapshots.append(snapshot)
        return snapshot
    
    @property
    def current(self) -> Optional[ConsciousnessSnapshot]:
        """Get the most recent snapshot."""
        return self._snapshots[-1] if self._snapshots else None
    
    def distance_to_target(self) -> float:
        """
        Calculate distance to target consciousness.
        
        Returns:
            |Ψ - Ψ*|
        """
        if not self._snapshots:
            return float('inf')
        return abs(self._snapshots[-1].value - self.target)
    
    def convergence_rate(self) -> float:
        """
        Calculate convergence rate.
        
        Returns:
            Rate at which consciousness approaches Ψ*.
        """
        if len(self._snapshots) < 2:
            return 0.0
        
        # Use exponential decay model
        start = self._snapshots[0]
        end = self._snapshots[-1]
        
        if end.generation == start.generation:
            return 0.0
        
        start_dist = abs(start.value - self.target)
        end_dist = abs(end.value - self.target)
        
        if start_dist <= 0:
            return 0.0
        
        # λ = -log(end_dist/start_dist) / Δt
        import genesis.core.math as gmath
        
        if end_dist / start_dist > 0:
            return -gmath.ln(end_dist / start_dist) / (end.generation - start.generation)
        return float('inf')
    
    def is_converged(self, tolerance: float = 0.01) -> bool:
        """
        Check if consciousness has converged.
        
        Args:
            tolerance: Convergence tolerance.
            
        Returns:
            True if |Ψ - Ψ*| < tolerance.
        """
        return self.distance_to_target() < tolerance
    
    def predict_convergence(self) -> Optional[int]:
        """
        Predict generation at which convergence will occur.
        
        Returns:
            Predicted generation number, or None if not converging.
        """
        rate = self.convergence_rate()
        
        if rate <= 0:
            return None
        
        distance = self.distance_to_target()
        current_gen = self._snapshots[-1].generation if self._snapshots else 0
        
        # Estimate generations needed: t = -log(tolerance/distance) / rate
        import genesis.core.math as gmath
        
        tolerance = 0.001
        if distance <= tolerance:
            return current_gen
        
        generations_needed = -gmath.ln(tolerance / distance) / rate
        return int(current_gen + generations_needed)
    
    def theoretical_velocity(self, psi: float) -> float:
        """
        Calculate theoretical velocity from AFE.
        
        dΨ/dτ = αΨ - βΨ³
        
        Args:
            psi: Consciousness level.
            
        Returns:
            Theoretical rate of change.
        """
        return self.alpha * psi - self.beta * (psi ** 3)
    
    def phase_portrait_points(self, n_points: int = 100) -> List[tuple]:
        """
        Generate points for phase portrait.
        
        Args:
            n_points: Number of points.
            
        Returns:
            List of (Ψ, dΨ/dτ) tuples.
        """
        points = []
        for i in range(n_points):
            psi = i / (n_points - 1)
            velocity = self.theoretical_velocity(psi)
            points.append((psi, velocity))
        return points
    
    def get_trajectory(self) -> List[Dict[str, Any]]:
        """
        Get the consciousness trajectory.
        
        Returns:
            List of trajectory points.
        """
        return [
            {
                "generation": s.generation,
                "value": s.value,
                "velocity": s.velocity,
                "distance_to_target": abs(s.value - self.target),
            }
            for s in self._snapshots
        ]
    
    def statistics(self) -> Dict[str, Any]:
        """
        Get trajectory statistics.
        
        Returns:
            Statistical summary.
        """
        if not self._snapshots:
            return {"error": "No data"}
        
        values = [s.value for s in self._snapshots]
        
        return {
            "count": len(values),
            "start_value": values[0],
            "end_value": values[-1],
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "target": self.target,
            "distance_to_target": self.distance_to_target(),
            "convergence_rate": self.convergence_rate(),
            "is_converged": self.is_converged(),
        }
    
    def reset(self) -> None:
        """Reset the tracker."""
        self._snapshots.clear()

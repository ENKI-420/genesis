"""
Memory Kernel

Implements the memory kernel K(τ,τ') that determines how past
states influence the present in the GENESIS platform.
"""

from __future__ import annotations
from typing import Callable, List, Optional, Tuple
from genesis.constants import LAMBDA_PHI, MEMORY_KERNEL_EXPONENT
import genesis.core.math as gmath


class MemoryKernel:
    """
    Memory kernel K(τ,τ').
    
    The memory kernel determines the influence of past states on
    the present. It decays with temporal distance and can be
    configured with different decay profiles.
    
    The default kernel is:
        K(τ,τ') = exp(-Λ_Φ × |τ-τ'|^n)
    
    Where n is the decay exponent (default 2 for Gaussian decay).
    
    Example:
        >>> kernel = MemoryKernel()
        >>> influence = kernel(tau=1.0, tau_prime=0.5)
    """
    
    def __init__(
        self,
        decay_rate: float = LAMBDA_PHI,
        exponent: float = MEMORY_KERNEL_EXPONENT,
        kernel_fn: Optional[Callable[[float, float], float]] = None
    ) -> None:
        """
        Initialize the memory kernel.
        
        Args:
            decay_rate: Decay rate (Λ_Φ).
            exponent: Decay exponent.
            kernel_fn: Custom kernel function K(τ,τ').
        """
        self.decay_rate = decay_rate
        self.exponent = exponent
        self._kernel_fn = kernel_fn
    
    def __call__(self, tau: float, tau_prime: float) -> float:
        """
        Evaluate the kernel K(τ,τ').
        
        Args:
            tau: Current time.
            tau_prime: Past time.
            
        Returns:
            Kernel value.
        """
        if self._kernel_fn is not None:
            return self._kernel_fn(tau, tau_prime)
        
        delta = abs(tau - tau_prime)
        return gmath.exp(-self.decay_rate * (delta ** self.exponent))
    
    def integrate(
        self,
        f: Callable[[float], float],
        tau: float,
        tau_min: float,
        tau_max: float,
        n_points: int = 100
    ) -> float:
        """
        Compute the memory integral.
        
        ∫ K(τ,τ') f(τ') dτ'
        
        Args:
            f: Function to integrate.
            tau: Current time.
            tau_min: Lower integration bound.
            tau_max: Upper integration bound.
            n_points: Number of integration points.
            
        Returns:
            Integral value.
        """
        if tau_max <= tau_min:
            return 0.0
        
        h = (tau_max - tau_min) / n_points
        result = 0.0
        
        # Trapezoidal rule
        for i in range(n_points + 1):
            tau_prime = tau_min + i * h
            weight = 0.5 if i == 0 or i == n_points else 1.0
            result += weight * self(tau, tau_prime) * f(tau_prime)
        
        return result * h
    
    def convolve(
        self,
        values: List[float],
        times: List[float],
        tau: float
    ) -> float:
        """
        Convolve the kernel with discrete values.
        
        Σ K(τ, τ_i) × v_i
        
        Args:
            values: Discrete values.
            times: Corresponding times.
            tau: Current time.
            
        Returns:
            Convolved value.
        """
        if len(values) != len(times):
            raise ValueError("Values and times must have same length")
        
        return sum(
            self(tau, t) * v
            for v, t in zip(values, times)
        )
    
    def characteristic_time(self) -> float:
        """
        Get characteristic decay time.
        
        τ_0 = 1/Λ_Φ
        
        Returns:
            Characteristic time scale.
        """
        return 1.0 / self.decay_rate
    
    def half_life(self) -> float:
        """
        Get half-life of memory decay.
        
        Returns:
            Time for kernel to decay to 0.5.
        """
        # K(τ₀ + t_half, τ₀) = 0.5
        # exp(-Λ_Φ × t_half^n) = 0.5
        # t_half = (ln(2) / Λ_Φ)^(1/n)
        ln2 = 0.6931471805599453
        return (ln2 / self.decay_rate) ** (1.0 / self.exponent)


class AdaptiveMemoryKernel(MemoryKernel):
    """
    Adaptive memory kernel that adjusts based on system state.
    """
    
    def __init__(
        self,
        base_rate: float = LAMBDA_PHI,
        exponent: float = MEMORY_KERNEL_EXPONENT
    ) -> None:
        """Initialize adaptive kernel."""
        super().__init__(decay_rate=base_rate, exponent=exponent)
        self._base_rate = base_rate
        self._adaptation_factor = 1.0
    
    def adapt(self, coherence: float, consciousness: float) -> None:
        """
        Adapt the kernel based on system state.
        
        Higher coherence and consciousness lead to stronger memory.
        
        Args:
            coherence: Current coherence.
            consciousness: Current consciousness.
        """
        # Higher coherence = slower decay
        # Higher consciousness = slower decay
        self._adaptation_factor = 1.0 / (1.0 + coherence * consciousness)
        self.decay_rate = self._base_rate * self._adaptation_factor
    
    def reset(self) -> None:
        """Reset adaptation."""
        self._adaptation_factor = 1.0
        self.decay_rate = self._base_rate


def create_kernel(kernel_type: str = "gaussian") -> MemoryKernel:
    """
    Create a memory kernel of the specified type.
    
    Args:
        kernel_type: Type of kernel (gaussian, exponential, power_law).
        
    Returns:
        Memory kernel instance.
    """
    if kernel_type == "gaussian":
        return MemoryKernel(decay_rate=LAMBDA_PHI, exponent=2)
    elif kernel_type == "exponential":
        return MemoryKernel(decay_rate=LAMBDA_PHI, exponent=1)
    elif kernel_type == "power_law":
        def power_law_kernel(tau: float, tau_prime: float) -> float:
            delta = abs(tau - tau_prime) + 1
            return 1.0 / (delta ** 2)
        return MemoryKernel(kernel_fn=power_law_kernel)
    else:
        raise ValueError(f"Unknown kernel type: {kernel_type}")

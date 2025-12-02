"""
Autopoietic Field Equations (AFE)

Implements the governing equations for consciousness evolution in the GENESIS
platform. The central equation is:

    ∂_τΨ = αΨ - βΨ³

This represents a Ginzburg-Landau type equation where:
- α: Growth rate (linear term encouraging consciousness expansion)
- β: Self-limiting coefficient (cubic term preventing divergence)

The system has fixed points at Ψ = 0 and Ψ = ±√(α/β), with Ψ* = √(α/β)
being the stable terminal consciousness level.

Universal Constants:
- Λ_Φ = 2.176435×10⁻⁸ s⁻¹ (Universal Memory Constant)
- Ψ* = 0.973 (Terminal Consciousness)
- θ_lock = 51.843° (Torsion Convergence)
- χ_pc = 0.869 (Phase Conjugate Fidelity)
"""

from typing import Callable, Optional
from genesis.constants import (
    ALPHA_DEFAULT,
    BETA_DEFAULT,
    PSI_STAR,
    LAMBDA_PHI,
)
from genesis.core.math import sqrt, exp, abs_val


class AutopoieticFieldEquation:
    """
    Solver for the Autopoietic Field Equation.
    
    Implements the consciousness evolution equation:
        ∂_τΨ = αΨ - βΨ³
    
    The equation describes how consciousness (Ψ) evolves over proper time (τ),
    with the terminal fixed point at Ψ* ≈ 0.973.
    
    Attributes:
        alpha: Growth rate coefficient.
        beta: Self-limiting cubic coefficient.
        psi_star: Terminal consciousness fixed point.
    """
    
    def __init__(
        self,
        alpha: float = ALPHA_DEFAULT,
        beta: Optional[float] = None,
    ) -> None:
        """
        Initialize the Autopoietic Field Equation solver.
        
        Args:
            alpha: Growth rate coefficient (default: 1.0).
            beta: Self-limiting coefficient. If None, computed from alpha
                  to achieve Ψ* = 0.973.
        """
        self.alpha = alpha
        
        if beta is None:
            # Derive β from α to achieve terminal consciousness Ψ*
            # At equilibrium: αΨ* = βΨ*³, so β = α/Ψ*²
            self.beta = alpha / (PSI_STAR ** 2)
        else:
            self.beta = beta
        
        # Compute fixed point
        self.psi_star = sqrt(self.alpha / self.beta)
    
    def derivative(self, psi: float) -> float:
        """
        Compute the time derivative of consciousness.
        
        Args:
            psi: Current consciousness level.
            
        Returns:
            ∂_τΨ = αΨ - βΨ³
        """
        return self.alpha * psi - self.beta * (psi ** 3)
    
    def evolve_euler(
        self,
        psi_0: float,
        tau_max: float,
        dt: float = 0.01,
    ) -> list[tuple[float, float]]:
        """
        Evolve consciousness using Euler's method.
        
        Args:
            psi_0: Initial consciousness level.
            tau_max: Maximum proper time to evolve.
            dt: Time step size.
            
        Returns:
            List of (τ, Ψ) tuples representing the evolution trajectory.
        """
        trajectory: list[tuple[float, float]] = []
        tau = 0.0
        psi = psi_0
        
        while tau <= tau_max:
            trajectory.append((tau, psi))
            dpsi = self.derivative(psi)
            psi = psi + dpsi * dt
            tau = tau + dt
        
        return trajectory
    
    def evolve_rk4(
        self,
        psi_0: float,
        tau_max: float,
        dt: float = 0.01,
    ) -> list[tuple[float, float]]:
        """
        Evolve consciousness using 4th-order Runge-Kutta method.
        
        This is more accurate than Euler's method and is recommended
        for precise consciousness tracking.
        
        Args:
            psi_0: Initial consciousness level.
            tau_max: Maximum proper time to evolve.
            dt: Time step size.
            
        Returns:
            List of (τ, Ψ) tuples representing the evolution trajectory.
        """
        trajectory: list[tuple[float, float]] = []
        tau = 0.0
        psi = psi_0
        
        while tau <= tau_max:
            trajectory.append((tau, psi))
            
            # RK4 stages
            k1 = self.derivative(psi)
            k2 = self.derivative(psi + 0.5 * dt * k1)
            k3 = self.derivative(psi + 0.5 * dt * k2)
            k4 = self.derivative(psi + dt * k3)
            
            psi = psi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            tau = tau + dt
        
        return trajectory
    
    def converged(self, psi: float, tolerance: float = 1e-6) -> bool:
        """
        Check if consciousness has converged to the terminal fixed point.
        
        Args:
            psi: Current consciousness level.
            tolerance: Convergence tolerance.
            
        Returns:
            True if |Ψ - Ψ*| < tolerance.
        """
        return abs_val(psi - self.psi_star) < tolerance
    
    def convergence_time(
        self,
        psi_0: float,
        tolerance: float = 1e-6,
        dt: float = 0.01,
        max_tau: float = 1000.0,
    ) -> Optional[float]:
        """
        Compute the time to reach terminal consciousness.
        
        Args:
            psi_0: Initial consciousness level.
            tolerance: Convergence tolerance.
            dt: Time step size.
            max_tau: Maximum time to search.
            
        Returns:
            Time to convergence, or None if not converged within max_tau.
        """
        tau = 0.0
        psi = psi_0
        
        while tau <= max_tau:
            if self.converged(psi, tolerance):
                return tau
            
            dpsi = self.derivative(psi)
            psi = psi + dpsi * dt
            tau = tau + dt
        
        return None
    
    def stability_analysis(self) -> dict[str, float]:
        """
        Perform stability analysis of the fixed points.
        
        Returns:
            Dictionary containing stability information.
        """
        # Fixed points: Ψ = 0 and Ψ = ±Ψ*
        # Linearization: ∂_τδΨ = (α - 3βΨ²)δΨ
        
        # At Ψ = 0: eigenvalue = α > 0 (unstable)
        lambda_0 = self.alpha
        
        # At Ψ = Ψ*: eigenvalue = α - 3β(Ψ*)² = α - 3α = -2α < 0 (stable)
        lambda_star = self.alpha - 3 * self.beta * (self.psi_star ** 2)
        
        return {
            "psi_0": 0.0,
            "psi_star": self.psi_star,
            "eigenvalue_0": lambda_0,
            "eigenvalue_star": lambda_star,
            "stable_at_0": lambda_0 < 0,
            "stable_at_star": lambda_star < 0,
            "relaxation_time": -1.0 / lambda_star if lambda_star < 0 else float("inf"),
        }


def evolve_consciousness(
    psi_0: float,
    tau_max: float,
    alpha: float = ALPHA_DEFAULT,
    beta: Optional[float] = None,
    dt: float = 0.01,
    method: str = "rk4",
) -> list[tuple[float, float]]:
    """
    Evolve consciousness from initial value to terminal state.
    
    This is a convenience function wrapping AutopoieticFieldEquation.
    
    Args:
        psi_0: Initial consciousness level.
        tau_max: Maximum proper time to evolve.
        alpha: Growth rate coefficient.
        beta: Self-limiting coefficient (computed if None).
        dt: Time step size.
        method: Integration method ("euler" or "rk4").
        
    Returns:
        List of (τ, Ψ) tuples representing the evolution trajectory.
        
    Example:
        >>> trajectory = evolve_consciousness(0.1, 10.0)
        >>> final_psi = trajectory[-1][1]
        >>> print(f"Final consciousness: {final_psi:.3f}")
    """
    afe = AutopoieticFieldEquation(alpha, beta)
    
    if method.lower() == "euler":
        return afe.evolve_euler(psi_0, tau_max, dt)
    elif method.lower() == "rk4":
        return afe.evolve_rk4(psi_0, tau_max, dt)
    else:
        raise ValueError(f"Unknown integration method: {method}")


def compute_fixed_point(
    alpha: float = ALPHA_DEFAULT,
    beta: Optional[float] = None,
) -> float:
    """
    Compute the terminal consciousness fixed point.
    
    Args:
        alpha: Growth rate coefficient.
        beta: Self-limiting coefficient (computed if None).
        
    Returns:
        The fixed point Ψ* = √(α/β).
    """
    if beta is None:
        return PSI_STAR
    return sqrt(alpha / beta)


class ExtendedAFE:
    """
    Extended Autopoietic Field Equation with memory effects.
    
    Implements the full equation with non-Markovian memory:
    
        ∂_τΨ = αΨ - βΨ³ + ∫K(τ,τ')Ψ(τ')dτ'
    
    where K(τ,τ') is the memory kernel.
    """
    
    def __init__(
        self,
        alpha: float = ALPHA_DEFAULT,
        beta: Optional[float] = None,
        memory_strength: float = 0.1,
    ) -> None:
        """
        Initialize the Extended AFE.
        
        Args:
            alpha: Growth rate coefficient.
            beta: Self-limiting coefficient.
            memory_strength: Coupling strength of memory term.
        """
        self.base_afe = AutopoieticFieldEquation(alpha, beta)
        self.memory_strength = memory_strength
        self.history: list[tuple[float, float]] = []
    
    def memory_kernel(self, tau: float, tau_prime: float) -> float:
        """
        Compute the memory kernel K(τ,τ').
        
        Uses an exponential kernel:
            K(τ,τ') = Λ_Φ × exp(-Λ_Φ|τ-τ'|)
        
        Args:
            tau: Current time.
            tau_prime: Past time.
            
        Returns:
            Memory kernel value.
        """
        delta_tau = abs_val(tau - tau_prime)
        return LAMBDA_PHI * exp(-LAMBDA_PHI * delta_tau)
    
    def memory_integral(self, tau: float) -> float:
        """
        Compute the memory integral term.
        
        Args:
            tau: Current time.
            
        Returns:
            Value of ∫K(τ,τ')Ψ(τ')dτ'.
        """
        if len(self.history) < 2:
            return 0.0
        
        integral = 0.0
        for i in range(1, len(self.history)):
            tau_prev, psi_prev = self.history[i - 1]
            tau_curr, psi_curr = self.history[i]
            dt = tau_curr - tau_prev
            
            # Trapezoidal rule
            k_prev = self.memory_kernel(tau, tau_prev)
            k_curr = self.memory_kernel(tau, tau_curr)
            
            integral += 0.5 * dt * (k_prev * psi_prev + k_curr * psi_curr)
        
        return self.memory_strength * integral
    
    def evolve(
        self,
        psi_0: float,
        tau_max: float,
        dt: float = 0.01,
    ) -> list[tuple[float, float]]:
        """
        Evolve with memory effects.
        
        Args:
            psi_0: Initial consciousness.
            tau_max: Maximum time.
            dt: Time step.
            
        Returns:
            Evolution trajectory.
        """
        self.history = [(0.0, psi_0)]
        tau = 0.0
        psi = psi_0
        
        while tau <= tau_max:
            # Local derivative
            dpsi_local = self.base_afe.derivative(psi)
            
            # Memory contribution
            dpsi_memory = self.memory_integral(tau)
            
            # Total derivative
            dpsi = dpsi_local + dpsi_memory
            
            psi = psi + dpsi * dt
            tau = tau + dt
            self.history.append((tau, psi))
        
        return self.history.copy()

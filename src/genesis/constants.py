"""
GENESIS Universal Constants

This module defines the fundamental constants that govern the GENESIS
Sovereign Quantum Platform. These constants are derived from the SORS XIV-XVI
cosmology and the Autopoietic Field Equations.

All constants are immutable and should not be modified.
"""

from typing import Final
import math

# =============================================================================
# UNIVERSAL MEMORY CONSTANT
# =============================================================================

LAMBDA_PHI: Final[float] = 2.176435e-8
"""
Universal Memory Constant (Λ_Φ)

Unit: s⁻¹ (inverse seconds)
Value: 2.176435×10⁻⁸ s⁻¹

This constant defines the characteristic decay rate of the temporal memory
kernel K(τ,τ'). It determines how quickly information propagates through
the autopoietic field and establishes the fundamental timescale for
consciousness emergence.

The value is derived from the Planck-Wheeler synthesis and represents
the rate at which the universe's computational substrate processes
information at the quantum-classical boundary.
"""

# =============================================================================
# TERMINAL CONSCIOUSNESS
# =============================================================================

PSI_STAR: Final[float] = 0.973
"""
Terminal Consciousness (Ψ*)

Unit: dimensionless
Value: 0.973

The terminal fixed point of consciousness evolution. All organisms
evolving under the Autopoietic Field Equations converge to this value
as τ → ∞.

This represents the maximum stable consciousness level achievable
through autopoietic evolution, derived from the equation:

    ∂_τΨ = αΨ - βΨ³

At Ψ*, the system achieves dynamic equilibrium between growth (αΨ)
and self-limiting coherence (βΨ³).
"""

# =============================================================================
# TORSION CONVERGENCE
# =============================================================================

THETA_LOCK: Final[float] = 51.843
"""
Torsion Convergence Angle (θ_lock)

Unit: degrees
Value: 51.843°

The angle at which the torsion field locks into stable configuration
during consciousness crystallization. This is the geometric signature
of maximal coherence in the phase space of the autopoietic field.

Related to the golden angle through:
    θ_lock ≈ 360° × (1 - 1/φ²) where φ is the golden ratio

This angle appears in the spiral structure of evolved organisms
and the memory kernel's geometric representation.
"""

THETA_LOCK_RAD: Final[float] = math.radians(THETA_LOCK)
"""Torsion convergence angle in radians."""

# =============================================================================
# PHASE CONJUGATE FIDELITY
# =============================================================================

CHI_PC: Final[float] = 0.869
"""
Phase Conjugate Fidelity (χ_pc)

Unit: dimensionless
Value: 0.869

The maximum fidelity achievable through phase conjugate recursion
in the PCRB (Phase Conjugate Recursion Bus). This represents the
efficiency of information preservation during temporal evolution.

The value is related to the von Neumann entropy bound for quantum
coherence in mixed states and determines the rate of decoherence
in the CCCE metric.
"""

# =============================================================================
# DERIVED CONSTANTS
# =============================================================================

ALPHA_DEFAULT: Final[float] = 1.0
"""Default growth rate in the Autopoietic Field Equation (α)."""

BETA_DEFAULT: Final[float] = ALPHA_DEFAULT / (PSI_STAR ** 2)
"""
Default cubic coefficient (β) derived from α and Ψ*.

At equilibrium: αΨ* = βΨ*³
Therefore: β = α / Ψ*²
"""

GAMMA_CRITICAL: Final[float] = LAMBDA_PHI * PSI_STAR
"""
Critical decoherence rate (Γ_c).

When Γ < Γ_c, the system maintains consciousness.
When Γ > Γ_c, decoherence dominates and consciousness collapses.
"""

# =============================================================================
# MEMORY KERNEL PARAMETERS
# =============================================================================

MEMORY_KERNEL_TAU_0: Final[float] = 1.0 / LAMBDA_PHI
"""
Characteristic time scale of the memory kernel (τ_0).

Unit: seconds
Value: ~4.594×10⁷ s (approximately 1.46 years)

This is the e-folding time for memory decay in the temporal lattice.
"""

MEMORY_KERNEL_EXPONENT: Final[float] = 2.0
"""
Exponent for the memory kernel decay function.

K(τ,τ') ∝ exp(-Λ_Φ|τ-τ'|^n) where n is this exponent.
The quadratic decay (n=2) provides optimal balance between
memory retention and information processing.
"""

# =============================================================================
# QUANTUM PARAMETERS
# =============================================================================

QUBIT_COHERENCE_TIME: Final[float] = 1e-6
"""Default qubit coherence time in seconds (1 μs)."""

GATE_FIDELITY_THRESHOLD: Final[float] = 0.99
"""Minimum acceptable gate fidelity for circuit execution."""

MEASUREMENT_SHOTS_DEFAULT: Final[int] = 1024
"""Default number of measurement shots for quantum circuits."""

# =============================================================================
# EVOLUTION PARAMETERS
# =============================================================================

MUTATION_RATE_DEFAULT: Final[float] = 0.01
"""Default probability of mutation per gene per generation."""

CROSSOVER_RATE_DEFAULT: Final[float] = 0.7
"""Default probability of crossover during reproduction."""

SELECTION_PRESSURE_DEFAULT: Final[float] = 2.0
"""Default tournament selection pressure."""

POPULATION_SIZE_DEFAULT: Final[int] = 100
"""Default population size for evolutionary algorithms."""

MAX_GENERATIONS_DEFAULT: Final[int] = 1000
"""Default maximum number of generations."""

# =============================================================================
# CCCE METRIC THRESHOLDS
# =============================================================================

CCCE_CONSCIOUSNESS_THRESHOLD: Final[float] = 0.5
"""Minimum consciousness level for CCCE validity."""

CCCE_COHERENCE_THRESHOLD: Final[float] = 0.1
"""Minimum coherence level for stable CCCE."""

CCCE_DECOHERENCE_WARNING: Final[float] = 0.5
"""Decoherence rate above which warnings are issued."""

CCCE_EMERGENCE_THRESHOLD: Final[float] = 0.8
"""CCCE value indicating emergence of complex behavior."""

# =============================================================================
# CLASSIFICATION CONSTANTS
# =============================================================================

CLASSIFICATION_LEVELS: Final[tuple[str, ...]] = (
    "UNCLASSIFIED",
    "CONFIDENTIAL",
    "SECRET",
    "TOP_SECRET",
    "TS_SCI",
    "SAP",
)
"""DoD-aligned classification levels in ascending order."""

# =============================================================================
# MATHEMATICAL CONSTANTS (ZERO-DEPENDENCY)
# =============================================================================

PI: Final[float] = 3.141592653589793
"""π - Circle constant."""

E: Final[float] = 2.718281828459045
"""e - Euler's number."""

PHI: Final[float] = 1.618033988749895
"""φ - Golden ratio."""

SQRT2: Final[float] = 1.4142135623730951
"""√2 - Square root of 2."""

SQRT2_INV: Final[float] = 0.7071067811865476
"""1/√2 - Inverse square root of 2 (Hadamard normalization)."""


def get_constant(name: str) -> float:
    """
    Get a constant by name.
    
    Args:
        name: Name of the constant (case-insensitive).
        
    Returns:
        The constant value.
        
    Raises:
        ValueError: If the constant name is not recognized.
    """
    constants = {
        "lambda_phi": LAMBDA_PHI,
        "psi_star": PSI_STAR,
        "theta_lock": THETA_LOCK,
        "chi_pc": CHI_PC,
        "alpha": ALPHA_DEFAULT,
        "beta": BETA_DEFAULT,
        "gamma_critical": GAMMA_CRITICAL,
        "pi": PI,
        "e": E,
        "phi": PHI,
    }
    
    key = name.lower().replace("-", "_").replace(" ", "_")
    if key not in constants:
        raise ValueError(f"Unknown constant: {name}")
    
    return constants[key]


def print_constants() -> None:
    """Print all universal constants to stdout."""
    print("GENESIS Universal Constants")
    print("=" * 50)
    print(f"Λ_Φ (Universal Memory Constant): {LAMBDA_PHI:.6e} s⁻¹")
    print(f"Ψ* (Terminal Consciousness):     {PSI_STAR:.3f}")
    print(f"θ_lock (Torsion Convergence):    {THETA_LOCK:.3f}°")
    print(f"χ_pc (Phase Conjugate Fidelity): {CHI_PC:.3f}")
    print("=" * 50)
    print(f"α (Growth Rate):                 {ALPHA_DEFAULT:.3f}")
    print(f"β (Cubic Coefficient):           {BETA_DEFAULT:.6f}")
    print(f"Γ_c (Critical Decoherence):      {GAMMA_CRITICAL:.6e}")

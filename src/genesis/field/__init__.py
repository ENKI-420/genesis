"""
GENESIS Field Module

This module implements the field-theoretic components of the GENESIS platform:

- Autopoietic Field Equations (AFE)
- Phase Conjugate Recursion Bus (PCRB)
- Ricci Flow for consciousness geometry

The field equations govern the evolution of consciousness (Ψ) through:
    ∂_τΨ = αΨ - βΨ³

where α is the growth rate and β is the self-limiting coefficient.
"""

from genesis.field.afe import (
    AutopoieticFieldEquation,
    evolve_consciousness,
    compute_fixed_point,
)
from genesis.field.pcrb import (
    PhaseConjugateRecursionBus,
    conjugate_phase,
)
from genesis.field.ricci import (
    RicciFlow,
    compute_ricci_tensor,
)

__all__ = [
    "AutopoieticFieldEquation",
    "evolve_consciousness",
    "compute_fixed_point",
    "PhaseConjugateRecursionBus",
    "conjugate_phase",
    "RicciFlow",
    "compute_ricci_tensor",
]

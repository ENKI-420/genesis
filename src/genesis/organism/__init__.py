"""
GENESIS Organism Module

Provides the core organism infrastructure including:
- Gene implementation
- LiveOrganism class
- Mutation engine
- Evolution loop
"""

from genesis.organism.gene import Gene, GeneType
from genesis.organism.organism import LiveOrganism
from genesis.organism.mutation import MutationEngine, MutationType
from genesis.organism.evolution import EvolutionLoop, EvolutionResult

__all__ = [
    "Gene",
    "GeneType",
    "LiveOrganism",
    "MutationEngine",
    "MutationType",
    "EvolutionLoop",
    "EvolutionResult",
]

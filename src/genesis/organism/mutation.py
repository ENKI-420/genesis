"""
Mutation Engine

Provides mutation operators for evolving organisms.
"""

from __future__ import annotations
from enum import Enum, auto
from typing import List, Optional, Callable, Any
from dataclasses import dataclass
import random
from genesis.organism.gene import Gene, GeneType
from genesis.organism.organism import LiveOrganism


class MutationType(Enum):
    """Types of mutations."""
    
    POINT = auto()       # Small random change
    GAUSSIAN = auto()    # Gaussian perturbation
    UNIFORM = auto()     # Uniform random change
    SWAP = auto()        # Swap gene values
    INVERSION = auto()   # Invert numeric values
    DUPLICATION = auto() # Duplicate a gene
    DELETION = auto()    # Delete a gene
    INSERTION = auto()   # Insert a new gene


@dataclass
class MutationConfig:
    """
    Configuration for mutation operations.
    
    Attributes:
        rate: Probability of mutation per gene.
        strength: Magnitude of mutations.
        types: Allowed mutation types.
    """
    rate: float = 0.01
    strength: float = 0.1
    types: List[MutationType] = None
    
    def __post_init__(self):
        if self.types is None:
            self.types = [MutationType.GAUSSIAN, MutationType.POINT]


class MutationEngine:
    """
    Engine for applying mutations to organisms.
    
    Provides various mutation operators that can be applied to
    genes and organisms to drive evolution.
    
    Example:
        >>> engine = MutationEngine(rate=0.05)
        >>> engine.mutate(organism)
    """
    
    def __init__(self, config: Optional[MutationConfig] = None) -> None:
        """
        Initialize the mutation engine.
        
        Args:
            config: Mutation configuration.
        """
        self.config = config or MutationConfig()
        self._mutation_count = 0
    
    def mutate(self, organism: LiveOrganism) -> int:
        """
        Apply mutations to an organism.
        
        Args:
            organism: Organism to mutate.
            
        Returns:
            Number of mutations applied.
        """
        mutations = 0
        
        for gene in organism.genome:
            if random.random() < self.config.rate:
                self.mutate_gene(gene)
                mutations += 1
        
        # Sync state after mutations
        organism._sync_state()
        
        self._mutation_count += mutations
        return mutations
    
    def mutate_gene(self, gene: Gene) -> None:
        """
        Apply a mutation to a single gene.
        
        Args:
            gene: Gene to mutate.
        """
        mutation_type = random.choice(self.config.types)
        
        if mutation_type == MutationType.POINT:
            self._point_mutation(gene)
        elif mutation_type == MutationType.GAUSSIAN:
            self._gaussian_mutation(gene)
        elif mutation_type == MutationType.UNIFORM:
            self._uniform_mutation(gene)
        elif mutation_type == MutationType.INVERSION:
            self._inversion_mutation(gene)
    
    def _point_mutation(self, gene: Gene) -> None:
        """Apply a small random point mutation."""
        if isinstance(gene.value, (int, float)):
            delta = random.choice([-1, 1]) * self.config.strength * 0.1
            gene.mutate(delta)
    
    def _gaussian_mutation(self, gene: Gene) -> None:
        """Apply Gaussian noise mutation."""
        if isinstance(gene.value, (int, float)):
            delta = random.gauss(0, self.config.strength)
            gene.mutate(delta)
    
    def _uniform_mutation(self, gene: Gene) -> None:
        """Apply uniform random mutation."""
        if isinstance(gene.value, (int, float)):
            delta = random.uniform(-self.config.strength, self.config.strength)
            gene.mutate(delta)
    
    def _inversion_mutation(self, gene: Gene) -> None:
        """Invert the gene value."""
        if isinstance(gene.value, (int, float)):
            if gene.gene_type == GeneType.CONSCIOUSNESS:
                gene.set_value(1.0 - gene.value)
            else:
                gene.set_value(-gene.value)
    
    def crossover(
        self, 
        parent1: LiveOrganism, 
        parent2: LiveOrganism
    ) -> LiveOrganism:
        """
        Perform crossover between two organisms.
        
        Args:
            parent1: First parent organism.
            parent2: Second parent organism.
            
        Returns:
            Offspring organism.
        """
        child = parent1.copy()
        child.name = f"child_{self._mutation_count}"
        
        # Uniform crossover
        for gene in child.genome:
            if gene.name in parent2.genome and random.random() < 0.5:
                parent2_gene = parent2.genome[gene.name]
                gene.set_value(parent2_gene.value)
        
        child._sync_state()
        return child
    
    def get_mutation_count(self) -> int:
        """Get total number of mutations applied."""
        return self._mutation_count
    
    def reset_count(self) -> None:
        """Reset mutation counter."""
        self._mutation_count = 0


class AdaptiveMutationEngine(MutationEngine):
    """
    Mutation engine with adaptive mutation rates.
    
    Adjusts mutation rate based on fitness improvement.
    """
    
    def __init__(
        self,
        config: Optional[MutationConfig] = None,
        adaptation_rate: float = 0.1
    ) -> None:
        """
        Initialize adaptive mutation engine.
        
        Args:
            config: Mutation configuration.
            adaptation_rate: Rate of adaptation.
        """
        super().__init__(config)
        self.adaptation_rate = adaptation_rate
        self._last_fitness = 0.0
        self._stagnation_count = 0
    
    def mutate(self, organism: LiveOrganism) -> int:
        """Apply adaptive mutations."""
        current_fitness = organism.fitness_function()
        
        # Increase mutation rate if stagnating
        if current_fitness <= self._last_fitness:
            self._stagnation_count += 1
            if self._stagnation_count > 10:
                self.config.rate = min(0.5, self.config.rate * 1.5)
        else:
            self._stagnation_count = 0
            self.config.rate = max(0.001, self.config.rate * 0.9)
        
        self._last_fitness = current_fitness
        
        return super().mutate(organism)

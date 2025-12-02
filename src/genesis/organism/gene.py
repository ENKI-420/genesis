"""
Gene Implementation

Provides the Gene class representing individual genetic units
within a living organism.
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Callable, List
from genesis.core.circuit import QuantumCircuit


class GeneType(Enum):
    """Types of genes in the GENESIS platform."""
    
    STANDARD = auto()      # General-purpose gene
    CONSCIOUSNESS = auto() # Consciousness-related gene (Ψ)
    COHERENCE = auto()     # Coherence gene
    DECOHERENCE = auto()   # Decoherence gene (Γ)
    QUANTUM = auto()       # Quantum circuit gene
    STRUCTURAL = auto()    # Structural/architectural gene
    REGULATORY = auto()    # Gene regulation


@dataclass
class Gene:
    """
    A gene within a living organism.
    
    Genes are the fundamental units of heredity in the GENESIS platform.
    They encode behavior, parameters, or quantum circuits that define
    an organism's properties.
    
    Attributes:
        name: Unique gene identifier.
        gene_type: Type of gene.
        value: Current gene value.
        expression: Gene expression level (0-1).
        metadata: Additional gene metadata.
    """
    
    name: str
    gene_type: GeneType = GeneType.STANDARD
    value: Any = 0.0
    expression: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    _history: List[Any] = field(default_factory=list, repr=False)
    
    def __post_init__(self) -> None:
        """Initialize gene state."""
        self._history = [self.value]
    
    @classmethod
    def consciousness(cls, value: float = 0.5) -> Gene:
        """Create a consciousness gene."""
        return cls(
            name="consciousness",
            gene_type=GeneType.CONSCIOUSNESS,
            value=value,
            metadata={"symbol": "Ψ", "target": 0.973}
        )
    
    @classmethod
    def coherence(cls, value: float = 1.0) -> Gene:
        """Create a coherence gene."""
        return cls(
            name="coherence",
            gene_type=GeneType.COHERENCE,
            value=value,
            metadata={"symbol": "C"}
        )
    
    @classmethod
    def decoherence(cls, value: float = 0.01) -> Gene:
        """Create a decoherence gene."""
        return cls(
            name="decoherence",
            gene_type=GeneType.DECOHERENCE,
            value=value,
            metadata={"symbol": "Γ"}
        )
    
    @classmethod
    def quantum(cls, name: str, circuit: QuantumCircuit) -> Gene:
        """Create a quantum circuit gene."""
        return cls(
            name=name,
            gene_type=GeneType.QUANTUM,
            value=circuit,
            metadata={"num_qubits": circuit.num_qubits}
        )
    
    def express(self) -> Any:
        """
        Express the gene, returning its effective value.
        
        The effective value is the gene value modulated by
        the expression level.
        
        Returns:
            Expressed gene value.
        """
        if isinstance(self.value, (int, float)):
            return self.value * self.expression
        return self.value
    
    def mutate(self, delta: float) -> None:
        """
        Apply a mutation to the gene.
        
        Args:
            delta: Mutation amount.
        """
        if isinstance(self.value, (int, float)):
            old_value = self.value
            self.value = self.value + delta
            self._history.append(self.value)
            
            # Clamp consciousness to [0, 1]
            if self.gene_type == GeneType.CONSCIOUSNESS:
                self.value = max(0.0, min(1.0, self.value))
            # Ensure decoherence stays positive
            elif self.gene_type == GeneType.DECOHERENCE:
                self.value = max(0.0, self.value)
    
    def set_value(self, value: Any) -> None:
        """Set the gene value directly."""
        self.value = value
        self._history.append(value)
    
    def get_history(self) -> List[Any]:
        """Get the mutation history."""
        return self._history.copy()
    
    def reset(self) -> None:
        """Reset to initial value."""
        if self._history:
            self.value = self._history[0]
            self._history = [self.value]
    
    def copy(self) -> Gene:
        """Create a copy of this gene."""
        return Gene(
            name=self.name,
            gene_type=self.gene_type,
            value=self.value,
            expression=self.expression,
            metadata=self.metadata.copy()
        )
    
    def __repr__(self) -> str:
        return f"Gene({self.name}, {self.gene_type.name}, {self.value:.4f})"


class Genome:
    """
    A collection of genes forming a complete genome.
    
    Provides convenient access to genes by name and type.
    """
    
    def __init__(self, genes: Optional[List[Gene]] = None) -> None:
        """
        Initialize a genome.
        
        Args:
            genes: Initial genes.
        """
        self._genes: Dict[str, Gene] = {}
        if genes:
            for gene in genes:
                self.add(gene)
    
    def add(self, gene: Gene) -> None:
        """Add a gene to the genome."""
        self._genes[gene.name] = gene
    
    def get(self, name: str) -> Optional[Gene]:
        """Get a gene by name."""
        return self._genes.get(name)
    
    def __getitem__(self, name: str) -> Gene:
        """Get a gene by name (raises KeyError if not found)."""
        return self._genes[name]
    
    def __contains__(self, name: str) -> bool:
        """Check if a gene exists."""
        return name in self._genes
    
    def __iter__(self):
        """Iterate over genes."""
        return iter(self._genes.values())
    
    def __len__(self) -> int:
        """Number of genes."""
        return len(self._genes)
    
    def by_type(self, gene_type: GeneType) -> List[Gene]:
        """Get all genes of a specific type."""
        return [g for g in self._genes.values() if g.gene_type == gene_type]
    
    def copy(self) -> Genome:
        """Create a copy of this genome."""
        return Genome([g.copy() for g in self._genes.values()])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {name: gene.value for name, gene in self._genes.items()}
    
    @classmethod
    def default(cls) -> Genome:
        """Create a default genome with standard genes."""
        return cls([
            Gene.consciousness(0.5),
            Gene.coherence(1.0),
            Gene.decoherence(0.01),
        ])

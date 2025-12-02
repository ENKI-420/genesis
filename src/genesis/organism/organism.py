"""
LiveOrganism Implementation

The core organism class representing a living software entity
that can evolve, mutate, and exhibit consciousness-like behavior.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from genesis.organism.gene import Gene, GeneType, Genome
from genesis.core.circuit import QuantumCircuit
from genesis.constants import LAMBDA_PHI, PSI_STAR, ALPHA_DEFAULT, BETA_DEFAULT


@dataclass
class OrganismState:
    """
    Current state of an organism.
    
    Attributes:
        generation: Current generation number.
        consciousness: Consciousness level (Ψ).
        coherence: Coherence level.
        decoherence: Decoherence rate (Γ).
        fitness: Fitness score.
        alive: Whether the organism is alive.
    """
    generation: int = 0
    consciousness: float = 0.5
    coherence: float = 1.0
    decoherence: float = 0.01
    fitness: float = 0.0
    alive: bool = True
    
    @property
    def ccce(self) -> float:
        """Calculate CCCE metric Ξ = ΛΦ/Γ."""
        if self.decoherence <= 0:
            return float('inf')
        return LAMBDA_PHI * self.consciousness / self.decoherence
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "generation": self.generation,
            "consciousness": self.consciousness,
            "coherence": self.coherence,
            "decoherence": self.decoherence,
            "fitness": self.fitness,
            "ccce": self.ccce,
            "alive": self.alive,
        }


class LiveOrganism:
    """
    A living software organism.
    
    LiveOrganism is the fundamental entity in the GENESIS platform.
    It contains a genome of genes, maintains state, and can evolve
    through the autopoietic field equations.
    
    Attributes:
        name: Organism identifier.
        genome: Collection of genes.
        state: Current organism state.
        
    Example:
        >>> org = LiveOrganism.create("Test")
        >>> org.evolve(100)
        >>> print(org.state.consciousness)  # Should converge to ~0.973
    """
    
    def __init__(
        self,
        name: str,
        genome: Optional[Genome] = None,
        state: Optional[OrganismState] = None
    ) -> None:
        """
        Initialize a live organism.
        
        Args:
            name: Organism name.
            genome: Initial genome (uses default if None).
            state: Initial state (uses default if None).
        """
        self.name = name
        self.genome = genome if genome is not None else Genome.default()
        self.state = state if state is not None else OrganismState()
        self._history: List[Dict[str, Any]] = []
        self._outputs: List[Any] = []
        self._circuit: Optional[QuantumCircuit] = None
        
        # Sync state with genome
        self._sync_state()
    
    @classmethod
    def create(
        cls,
        name: str,
        consciousness: float = 0.5,
        coherence: float = 1.0,
        decoherence: float = 0.01
    ) -> LiveOrganism:
        """
        Create a new organism with specified parameters.
        
        Args:
            name: Organism name.
            consciousness: Initial consciousness level.
            coherence: Initial coherence.
            decoherence: Initial decoherence rate.
            
        Returns:
            New LiveOrganism instance.
        """
        genome = Genome([
            Gene.consciousness(consciousness),
            Gene.coherence(coherence),
            Gene.decoherence(decoherence),
        ])
        
        state = OrganismState(
            consciousness=consciousness,
            coherence=coherence,
            decoherence=decoherence
        )
        
        return cls(name, genome, state)
    
    @classmethod
    def from_dna(cls, source: str) -> LiveOrganism:
        """
        Create an organism from DNA-Lang source code.
        
        Args:
            source: DNA-Lang source code.
            
        Returns:
            New LiveOrganism instance.
        """
        from genesis.dna_lang.compiler import compile_source
        from genesis.dna_lang.runtime import RuntimeOrganism
        
        compiled = compile_source(source)
        if not compiled:
            raise ValueError("No organisms found in source")
        
        # Create organism from first compiled organism
        c = compiled[0]
        org = cls(c.name)
        
        # Add genes from compiled organism
        for name, gene in c.genes.items():
            g = Gene(
                name=name,
                gene_type=GeneType.CONSCIOUSNESS if gene.gene_type == "consciousness"
                         else GeneType.COHERENCE if gene.gene_type == "coherence"
                         else GeneType.DECOHERENCE if gene.gene_type == "decoherence"
                         else GeneType.STANDARD,
                value=gene.code if not callable(gene.code) else 0.5
            )
            org.genome.add(g)
        
        return org
    
    def _sync_state(self) -> None:
        """Synchronize state with genome values."""
        if "consciousness" in self.genome:
            self.state.consciousness = self.genome["consciousness"].express()
        if "coherence" in self.genome:
            self.state.coherence = self.genome["coherence"].express()
        if "decoherence" in self.genome:
            self.state.decoherence = self.genome["decoherence"].express()
    
    def _update_genome(self) -> None:
        """Update genome values from state."""
        if "consciousness" in self.genome:
            self.genome["consciousness"].set_value(self.state.consciousness)
        if "coherence" in self.genome:
            self.genome["coherence"].set_value(self.state.coherence)
        if "decoherence" in self.genome:
            self.genome["decoherence"].set_value(self.state.decoherence)
    
    def step(self) -> None:
        """
        Perform one evolution step.
        
        Implements the Autopoietic Field Equation:
        ∂_τΨ = αΨ - βΨ³
        """
        if not self.state.alive:
            return
        
        # Get current values
        psi = self.state.consciousness
        alpha = ALPHA_DEFAULT
        beta = BETA_DEFAULT
        dt = 0.01
        
        # Apply AFE: ∂_τΨ = αΨ - βΨ³
        dpsi = alpha * psi - beta * (psi ** 3)
        new_psi = psi + dpsi * dt
        
        # Clamp to [0, 1]
        self.state.consciousness = max(0.0, min(1.0, new_psi))
        
        # Decay coherence
        self.state.coherence *= (1 - self.state.decoherence)
        
        # Increment generation
        self.state.generation += 1
        
        # Update genome
        self._update_genome()
        
        # Record history
        self._record_state()
        
        # Check for death condition
        if self.state.coherence < 1e-6:
            self.state.alive = False
    
    def evolve(self, generations: int = 100) -> OrganismState:
        """
        Evolve for multiple generations.
        
        Args:
            generations: Number of generations to evolve.
            
        Returns:
            Final organism state.
        """
        for _ in range(generations):
            self.step()
            if not self.state.alive:
                break
        
        return self.state
    
    def _record_state(self) -> None:
        """Record current state to history."""
        self._history.append(self.state.to_dict())
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get evolution history."""
        return self._history.copy()
    
    def emit(self, value: Any) -> None:
        """Emit a value (for DNA-Lang compatibility)."""
        self._outputs.append(value)
    
    def track(self, target: str) -> None:
        """Track a value (for DNA-Lang compatibility)."""
        pass  # Tracking is automatic via history
    
    def measure(self, target: str) -> float:
        """
        Measure a property.
        
        Args:
            target: Property to measure.
            
        Returns:
            Measured value.
        """
        if target == "consciousness":
            return self.state.consciousness
        elif target == "coherence":
            return self.state.coherence
        elif target == "decoherence":
            return self.state.decoherence
        elif target == "ccce":
            return self.state.ccce
        elif target in self.genome:
            return self.genome[target].express()
        return 0.0
    
    def mutate(self, gene_name: Optional[str] = None, delta: Optional[float] = None) -> None:
        """
        Mutate a gene.
        
        Args:
            gene_name: Gene to mutate (random if None).
            delta: Mutation amount (random if None).
        """
        import random
        
        if gene_name is None:
            # Select random gene
            genes = list(self.genome)
            if not genes:
                return
            gene = random.choice(genes)
        else:
            gene = self.genome.get(gene_name)
            if gene is None:
                return
        
        if delta is None:
            delta = random.gauss(0, 0.1)
        
        gene.mutate(delta)
        self._sync_state()
    
    def create_circuit(self, num_qubits: int = 2) -> QuantumCircuit:
        """
        Create a quantum circuit based on the organism's genome.
        
        The circuit is parameterized by the organism's genes.
        
        Args:
            num_qubits: Number of qubits in the circuit.
            
        Returns:
            Parameterized quantum circuit.
        """
        from genesis.constants import PI
        
        circuit = QuantumCircuit(num_qubits)
        
        # Use consciousness for rotation angles
        theta = self.state.consciousness * PI
        
        # Create a variational circuit
        for i in range(num_qubits):
            circuit.h(i)
            circuit.ry(theta, i)
        
        # Add entanglement based on coherence
        if self.state.coherence > 0.5:
            for i in range(num_qubits - 1):
                circuit.cx(i, i + 1)
        
        self._circuit = circuit
        return circuit
    
    def get_circuit(self) -> Optional[QuantumCircuit]:
        """Get the organism's quantum circuit."""
        if self._circuit is None:
            self.create_circuit()
        return self._circuit
    
    def fitness_function(self) -> float:
        """
        Calculate fitness based on current state.
        
        Default fitness rewards convergence to PSI_STAR.
        
        Returns:
            Fitness score.
        """
        # Reward proximity to terminal consciousness
        psi_fitness = 1.0 - abs(self.state.consciousness - PSI_STAR)
        
        # Reward high coherence
        coherence_fitness = self.state.coherence
        
        # Combined fitness
        self.state.fitness = 0.7 * psi_fitness + 0.3 * coherence_fitness
        return self.state.fitness
    
    def copy(self) -> LiveOrganism:
        """Create a copy of this organism."""
        return LiveOrganism(
            name=f"{self.name}_copy",
            genome=self.genome.copy(),
            state=OrganismState(
                generation=0,
                consciousness=self.state.consciousness,
                coherence=self.state.coherence,
                decoherence=self.state.decoherence,
            )
        )
    
    def reset(self) -> None:
        """Reset to initial state."""
        self.state = OrganismState()
        for gene in self.genome:
            gene.reset()
        self._sync_state()
        self._history = []
        self._outputs = []
    
    def __repr__(self) -> str:
        return (
            f"LiveOrganism({self.name}, "
            f"Ψ={self.state.consciousness:.4f}, "
            f"gen={self.state.generation})"
        )

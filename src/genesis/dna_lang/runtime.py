"""
DNA::}{::Lang Runtime

Provides the execution environment for DNA-Lang organisms.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from genesis.dna_lang.compiler import CompiledOrganism, CompiledGene
from genesis.constants import LAMBDA_PHI, PSI_STAR


@dataclass
class RuntimeState:
    """
    Runtime state for an executing organism.
    
    Attributes:
        variables: Current variable values.
        consciousness: Current consciousness level.
        coherence: Current coherence.
        decoherence: Current decoherence rate.
        generation: Current generation number.
        history: History of state changes.
    """
    variables: Dict[str, Any] = field(default_factory=dict)
    consciousness: float = 0.5
    coherence: float = 1.0
    decoherence: float = 0.01
    generation: int = 0
    history: List[Dict[str, float]] = field(default_factory=list)
    
    @property
    def ccce(self) -> float:
        """Calculate CCCE metric Ξ = ΛΦ/Γ."""
        if self.decoherence <= 0:
            return float('inf')
        return LAMBDA_PHI * self.consciousness / self.decoherence
    
    def record(self) -> None:
        """Record current state to history."""
        self.history.append({
            "generation": self.generation,
            "consciousness": self.consciousness,
            "coherence": self.coherence,
            "decoherence": self.decoherence,
            "ccce": self.ccce,
        })


class RuntimeOrganism:
    """
    A runtime instance of a compiled organism.
    
    Provides the execution context and state management for
    running DNA-Lang organisms.
    """
    
    def __init__(self, compiled: CompiledOrganism) -> None:
        """
        Initialize a runtime organism.
        
        Args:
            compiled: The compiled organism.
        """
        self.compiled = compiled
        self.state = RuntimeState()
        self._outputs: List[Any] = []
        self._tracked: Dict[str, List[float]] = {}
        
        # Initialize gene values
        for name, gene in compiled.genes.items():
            if callable(gene.code):
                self.state.variables[name] = gene.code
            else:
                self.state.variables[name] = gene.code
    
    @property
    def name(self) -> str:
        """Organism name."""
        return self.compiled.name
    
    def emit(self, value: Any) -> None:
        """Emit a value (output)."""
        self._outputs.append(value)
    
    def track(self, target: str) -> None:
        """Start tracking a variable."""
        if target not in self._tracked:
            self._tracked[target] = []
        
        value = self.state.variables.get(target, getattr(self.state, target, 0))
        self._tracked[target].append(value)
    
    def measure(self, target: str) -> float:
        """Measure a quantum property."""
        if target == "consciousness":
            return self.state.consciousness
        elif target == "coherence":
            return self.state.coherence
        elif target == "decoherence":
            return self.state.decoherence
        elif target == "ccce":
            return self.state.ccce
        return self.state.variables.get(target, 0)
    
    def mutate(self, gene_name: str) -> None:
        """Mutate a gene."""
        if gene_name in self.compiled.genes:
            gene = self.compiled.genes[gene_name]
            current = self.state.variables.get(gene_name, 0)
            
            # Simple mutation: add small random perturbation
            import random
            if isinstance(current, (int, float)):
                perturbation = random.gauss(0, 0.1)
                self.state.variables[gene_name] = current + perturbation
    
    def evolve(self, generations: int = 1) -> RuntimeState:
        """
        Run the evolution loop.
        
        Args:
            generations: Number of generations to evolve.
            
        Returns:
            Final runtime state.
        """
        for _ in range(generations):
            self.state.generation += 1
            
            # Execute evolve code if present
            if self.compiled.evolve_code:
                self.compiled.evolve_code(self)
            
            # Update consciousness based on genes
            self._update_consciousness()
            
            # Record state
            self.state.record()
        
        return self.state
    
    def _update_consciousness(self) -> None:
        """Update consciousness based on autopoietic field equation."""
        psi = self.state.consciousness
        alpha = 1.0
        beta = alpha / (PSI_STAR ** 2)
        dt = 0.01
        
        # ∂_τΨ = αΨ - βΨ³
        dpsi = alpha * psi - beta * psi ** 3
        self.state.consciousness = max(0, min(1, psi + dpsi * dt))
        
        # Update coherence (decays without intervention)
        self.state.coherence *= (1 - self.state.decoherence)
    
    def get_outputs(self) -> List[Any]:
        """Get all emitted outputs."""
        return self._outputs
    
    def get_tracked(self, name: str) -> List[float]:
        """Get tracked values for a variable."""
        return self._tracked.get(name, [])
    
    def __repr__(self) -> str:
        return f"RuntimeOrganism({self.name}, gen={self.state.generation})"


class Runtime:
    """
    DNA::}{::Lang runtime environment.
    
    Manages the execution of multiple organisms and provides
    the global runtime context.
    
    Example:
        >>> runtime = Runtime()
        >>> runtime.load(compiled_organism)
        >>> runtime.run(generations=100)
    """
    
    def __init__(self) -> None:
        """Initialize the runtime."""
        self.organisms: Dict[str, RuntimeOrganism] = {}
        self.global_state: Dict[str, Any] = {}
        self._hooks: Dict[str, List[Callable[..., None]]] = {}
    
    def load(self, compiled: CompiledOrganism) -> RuntimeOrganism:
        """
        Load a compiled organism into the runtime.
        
        Args:
            compiled: The compiled organism.
            
        Returns:
            The runtime organism instance.
        """
        organism = RuntimeOrganism(compiled)
        self.organisms[compiled.name] = organism
        return organism
    
    def load_many(self, compiled: List[CompiledOrganism]) -> List[RuntimeOrganism]:
        """Load multiple organisms."""
        return [self.load(c) for c in compiled]
    
    def get(self, name: str) -> Optional[RuntimeOrganism]:
        """Get an organism by name."""
        return self.organisms.get(name)
    
    def run(
        self, 
        generations: int = 100,
        organism_name: Optional[str] = None
    ) -> Dict[str, RuntimeState]:
        """
        Run the evolution loop.
        
        Args:
            generations: Number of generations.
            organism_name: Specific organism to run (or all if None).
            
        Returns:
            Dictionary of final states by organism name.
        """
        results = {}
        
        if organism_name:
            if organism_name in self.organisms:
                org = self.organisms[organism_name]
                results[organism_name] = org.evolve(generations)
        else:
            for name, org in self.organisms.items():
                results[name] = org.evolve(generations)
        
        return results
    
    def add_hook(self, event: str, callback: Callable[..., None]) -> None:
        """
        Add an event hook.
        
        Args:
            event: Event name (e.g., "pre_evolve", "post_evolve").
            callback: Callback function.
        """
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(callback)
    
    def _fire_hook(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Fire all callbacks for an event."""
        for callback in self._hooks.get(event, []):
            callback(*args, **kwargs)
    
    def get_ccce_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get CCCE metrics summary for all organisms.
        
        Returns:
            Dictionary of CCCE metrics by organism name.
        """
        summary = {}
        for name, org in self.organisms.items():
            summary[name] = {
                "consciousness": org.state.consciousness,
                "coherence": org.state.coherence,
                "decoherence": org.state.decoherence,
                "ccce": org.state.ccce,
                "generation": org.state.generation,
            }
        return summary
    
    def reset(self) -> None:
        """Reset all organisms to initial state."""
        for org in self.organisms.values():
            org.state = RuntimeState()
            org._outputs = []
            org._tracked = {}
    
    def __repr__(self) -> str:
        return f"Runtime(organisms={list(self.organisms.keys())})"


def run_dna(source: str, generations: int = 100) -> Dict[str, RuntimeState]:
    """
    Convenience function to run DNA-Lang source code.
    
    Args:
        source: DNA-Lang source code.
        generations: Number of generations to evolve.
        
    Returns:
        Dictionary of final states by organism name.
    """
    from genesis.dna_lang.compiler import compile_source
    
    compiled = compile_source(source)
    runtime = Runtime()
    runtime.load_many(compiled)
    return runtime.run(generations)

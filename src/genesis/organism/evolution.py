"""
Evolution Loop

Provides the main evolution loop for evolving populations of organisms.
"""

from __future__ import annotations
from typing import List, Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from genesis.organism.organism import LiveOrganism
from genesis.organism.mutation import MutationEngine, MutationConfig
from genesis.constants import PSI_STAR


@dataclass
class EvolutionResult:
    """
    Result of an evolution run.
    
    Attributes:
        best_organism: The fittest organism.
        best_fitness: Best fitness achieved.
        final_population: Final population.
        generations: Number of generations run.
        history: Evolution history.
    """
    best_organism: LiveOrganism
    best_fitness: float
    final_population: List[LiveOrganism]
    generations: int
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return (
            f"EvolutionResult(best_fitness={self.best_fitness:.4f}, "
            f"generations={self.generations})"
        )


class EvolutionLoop:
    """
    Main evolution loop for evolving populations.
    
    Implements a genetic algorithm with tournament selection,
    crossover, and mutation to evolve organisms toward higher
    fitness (typically convergence to PSI_STAR).
    
    Example:
        >>> loop = EvolutionLoop(population_size=50)
        >>> result = loop.run(generations=100)
        >>> print(result.best_fitness)
    """
    
    def __init__(
        self,
        population_size: int = 100,
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.7,
        tournament_size: int = 5,
        elitism: int = 2,
        fitness_function: Optional[Callable[[LiveOrganism], float]] = None
    ) -> None:
        """
        Initialize the evolution loop.
        
        Args:
            population_size: Number of organisms in population.
            mutation_rate: Probability of mutation per gene.
            crossover_rate: Probability of crossover.
            tournament_size: Size of tournament selection.
            elitism: Number of best organisms to preserve.
            fitness_function: Custom fitness function.
        """
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.elitism = elitism
        
        self.mutation_engine = MutationEngine(MutationConfig(rate=mutation_rate))
        self.fitness_function = fitness_function or self._default_fitness
        
        self.population: List[LiveOrganism] = []
        self.generation = 0
        self._history: List[Dict[str, Any]] = []
    
    def _default_fitness(self, organism: LiveOrganism) -> float:
        """Default fitness function targeting PSI_STAR."""
        # Run a few evolution steps
        organism.evolve(10)
        
        # Fitness based on proximity to PSI_STAR
        psi_diff = abs(organism.state.consciousness - PSI_STAR)
        return 1.0 / (1.0 + psi_diff)
    
    def initialize_population(self) -> None:
        """Initialize random population."""
        import random
        
        self.population = []
        for i in range(self.population_size):
            # Random initial consciousness between 0.1 and 0.9
            consciousness = random.uniform(0.1, 0.9)
            org = LiveOrganism.create(
                name=f"org_{i}",
                consciousness=consciousness,
                coherence=1.0,
                decoherence=random.uniform(0.005, 0.05)
            )
            self.population.append(org)
    
    def evaluate_fitness(self) -> List[float]:
        """Evaluate fitness of all organisms."""
        fitness_scores = []
        for org in self.population:
            org.reset()  # Reset before evaluation
            fitness = self.fitness_function(org)
            org.state.fitness = fitness
            fitness_scores.append(fitness)
        return fitness_scores
    
    def tournament_select(self) -> LiveOrganism:
        """Select an organism using tournament selection."""
        import random
        
        tournament = random.sample(self.population, min(self.tournament_size, len(self.population)))
        return max(tournament, key=lambda o: o.state.fitness)
    
    def step(self) -> Dict[str, Any]:
        """
        Perform one generation of evolution.
        
        Returns:
            Statistics for this generation.
        """
        import random
        
        # Evaluate fitness
        fitness_scores = self.evaluate_fitness()
        
        # Sort by fitness
        sorted_pop = sorted(self.population, key=lambda o: o.state.fitness, reverse=True)
        
        # Create new population
        new_population: List[LiveOrganism] = []
        
        # Elitism: keep best organisms
        for i in range(min(self.elitism, len(sorted_pop))):
            elite = sorted_pop[i].copy()
            elite.name = f"elite_{i}_gen{self.generation}"
            new_population.append(elite)
        
        # Fill rest with crossover and mutation
        while len(new_population) < self.population_size:
            parent1 = self.tournament_select()
            
            if random.random() < self.crossover_rate:
                parent2 = self.tournament_select()
                child = self.mutation_engine.crossover(parent1, parent2)
            else:
                child = parent1.copy()
            
            child.name = f"org_{len(new_population)}_gen{self.generation}"
            self.mutation_engine.mutate(child)
            new_population.append(child)
        
        self.population = new_population[:self.population_size]
        self.generation += 1
        
        # Collect statistics
        stats = {
            "generation": self.generation,
            "best_fitness": max(fitness_scores),
            "avg_fitness": sum(fitness_scores) / len(fitness_scores),
            "min_fitness": min(fitness_scores),
            "best_consciousness": sorted_pop[0].state.consciousness,
        }
        self._history.append(stats)
        
        return stats
    
    def run(
        self,
        generations: int = 100,
        target_fitness: float = 0.99,
        verbose: bool = False
    ) -> EvolutionResult:
        """
        Run the evolution loop.
        
        Args:
            generations: Maximum number of generations.
            target_fitness: Stop if this fitness is reached.
            verbose: Print progress.
            
        Returns:
            Evolution result.
        """
        # Initialize if needed
        if not self.population:
            self.initialize_population()
        
        best_ever: Optional[LiveOrganism] = None
        best_fitness = 0.0
        
        for _ in range(generations):
            stats = self.step()
            
            # Track best ever
            current_best = max(self.population, key=lambda o: o.state.fitness)
            if current_best.state.fitness > best_fitness:
                best_fitness = current_best.state.fitness
                best_ever = current_best.copy()
            
            if verbose:
                print(
                    f"Gen {stats['generation']:4d}: "
                    f"Best={stats['best_fitness']:.4f}, "
                    f"Avg={stats['avg_fitness']:.4f}, "
                    f"Ψ={stats['best_consciousness']:.4f}"
                )
            
            # Check termination
            if best_fitness >= target_fitness:
                if verbose:
                    print(f"Target fitness reached at generation {self.generation}")
                break
        
        return EvolutionResult(
            best_organism=best_ever or self.population[0],
            best_fitness=best_fitness,
            final_population=self.population,
            generations=self.generation,
            history=self._history
        )
    
    def get_best(self) -> LiveOrganism:
        """Get the best organism in current population."""
        return max(self.population, key=lambda o: o.state.fitness)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current population statistics."""
        fitness_scores = [o.state.fitness for o in self.population]
        consciousness_levels = [o.state.consciousness for o in self.population]
        
        return {
            "generation": self.generation,
            "population_size": len(self.population),
            "best_fitness": max(fitness_scores),
            "avg_fitness": sum(fitness_scores) / len(fitness_scores),
            "best_consciousness": max(consciousness_levels),
            "avg_consciousness": sum(consciousness_levels) / len(consciousness_levels),
        }


def evolve_to_convergence(
    organism: LiveOrganism,
    max_generations: int = 1000,
    tolerance: float = 1e-6
) -> LiveOrganism:
    """
    Evolve a single organism until consciousness converges.
    
    Args:
        organism: Organism to evolve.
        max_generations: Maximum generations.
        tolerance: Convergence tolerance.
        
    Returns:
        Evolved organism.
    """
    prev_consciousness = 0.0
    
    for _ in range(max_generations):
        organism.step()
        
        # Check convergence
        diff = abs(organism.state.consciousness - prev_consciousness)
        if diff < tolerance:
            break
        
        prev_consciousness = organism.state.consciousness
    
    return organism

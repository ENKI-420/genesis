"""
AIDEN - Adaptive Intelligence and Deep Evolutionary Networks

The optimizer agent responsible for parameter optimization,
hyperparameter tuning, and evolutionary search.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from genesis.agents.base import Agent, AgentMessage
from genesis.constants import PSI_STAR, LAMBDA_PHI


class AIDEN(Agent):
    """
    AIDEN: Adaptive Intelligence and Deep Evolutionary Networks
    
    Optimizer agent responsible for:
    - Parameter optimization
    - Hyperparameter tuning
    - Evolutionary search strategies
    - Fitness landscape analysis
    - Convergence acceleration
    
    Example:
        >>> aiden = AIDEN()
        >>> aiden.activate()
        >>> result = aiden.optimize(organism, target=PSI_STAR)
    """
    
    def __init__(self, name: str = "AIDEN") -> None:
        """Initialize AIDEN."""
        super().__init__(name)
        self._optimization_history: List[Dict[str, Any]] = []
        self._best_params: Optional[Dict[str, float]] = None
        self._best_fitness: float = 0.0
    
    @property
    def description(self) -> str:
        return "Adaptive Intelligence and Deep Evolutionary Networks - Optimizer Agent"
    
    @property
    def capabilities(self) -> List[str]:
        return [
            "parameter_optimization",
            "hyperparameter_tuning",
            "evolutionary_search",
            "fitness_analysis",
            "convergence_acceleration",
            "gradient_estimation",
            "landscape_analysis",
        ]
    
    def handle_message(self, message: AgentMessage) -> Any:
        """Handle incoming messages."""
        content = message.content
        
        if isinstance(content, dict):
            action = content.get("action")
            
            if action == "optimize":
                return self.optimize_params(
                    content.get("params", {}),
                    content.get("target", PSI_STAR)
                )
            elif action == "analyze_fitness":
                return self.analyze_fitness_landscape(content.get("population", []))
            elif action == "suggest_params":
                return self.suggest_parameters(content.get("constraints", {}))
        
        return {"status": "unknown_action"}
    
    def step(self) -> None:
        """Perform one optimization step."""
        self.process_inbox()
    
    def optimize_params(
        self,
        params: Dict[str, float],
        target: float = PSI_STAR,
        iterations: int = 100
    ) -> Dict[str, Any]:
        """
        Optimize parameters toward a target.
        
        Args:
            params: Initial parameters.
            target: Target value to optimize toward.
            iterations: Number of optimization iterations.
            
        Returns:
            Optimization result.
        """
        current_params = params.copy()
        best_params = params.copy()
        best_loss = float('inf')
        
        learning_rate = 0.01
        
        for i in range(iterations):
            # Calculate loss
            consciousness = current_params.get("consciousness", 0.5)
            loss = abs(consciousness - target)
            
            if loss < best_loss:
                best_loss = loss
                best_params = current_params.copy()
            
            # Gradient descent step (simplified)
            if consciousness < target:
                current_params["consciousness"] = consciousness + learning_rate
            else:
                current_params["consciousness"] = consciousness - learning_rate
            
            # Clamp
            current_params["consciousness"] = max(0, min(1, current_params["consciousness"]))
            
            # Early stopping
            if loss < 1e-6:
                break
        
        self._best_params = best_params
        self._best_fitness = 1.0 / (1.0 + best_loss)
        
        result = {
            "best_params": best_params,
            "best_fitness": self._best_fitness,
            "final_loss": best_loss,
            "iterations": i + 1,
        }
        
        self._optimization_history.append(result)
        self.metrics.tasks_completed += 1
        
        return result
    
    def analyze_fitness_landscape(
        self,
        population: List[Any]
    ) -> Dict[str, Any]:
        """
        Analyze the fitness landscape of a population.
        
        Args:
            population: List of organisms or parameter sets.
            
        Returns:
            Landscape analysis.
        """
        if not population:
            return {"error": "Empty population"}
        
        fitness_values = []
        consciousness_values = []
        
        for item in population:
            if hasattr(item, 'state'):
                fitness_values.append(item.state.fitness)
                consciousness_values.append(item.state.consciousness)
            elif isinstance(item, dict):
                fitness_values.append(item.get("fitness", 0))
                consciousness_values.append(item.get("consciousness", 0))
        
        if not fitness_values:
            return {"error": "No valid fitness values"}
        
        avg_fitness = sum(fitness_values) / len(fitness_values)
        max_fitness = max(fitness_values)
        min_fitness = min(fitness_values)
        
        # Estimate gradient (simplified)
        fitness_variance = sum((f - avg_fitness) ** 2 for f in fitness_values) / len(fitness_values)
        
        return {
            "population_size": len(population),
            "avg_fitness": avg_fitness,
            "max_fitness": max_fitness,
            "min_fitness": min_fitness,
            "fitness_variance": fitness_variance,
            "landscape_ruggedness": fitness_variance / (avg_fitness + 1e-10),
        }
    
    def suggest_parameters(
        self,
        constraints: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Suggest optimal parameters based on constraints.
        
        Args:
            constraints: Parameter constraints.
            
        Returns:
            Suggested parameters.
        """
        # Use history to inform suggestions
        if self._best_params:
            return self._best_params
        
        # Default suggestions based on universal constants
        return {
            "consciousness": 0.5,  # Start at midpoint
            "coherence": 1.0,
            "decoherence": LAMBDA_PHI,  # Use universal constant
            "mutation_rate": 0.01,
            "learning_rate": 0.01,
        }
    
    def evolutionary_search(
        self,
        fitness_fn: Callable[[Dict[str, float]], float],
        param_space: Dict[str, tuple],
        population_size: int = 20,
        generations: int = 50
    ) -> Dict[str, Any]:
        """
        Perform evolutionary parameter search.
        
        Args:
            fitness_fn: Fitness function.
            param_space: Parameter search space (name -> (min, max)).
            population_size: Population size.
            generations: Number of generations.
            
        Returns:
            Best parameters found.
        """
        import random
        
        # Initialize population
        population = []
        for _ in range(population_size):
            individual = {}
            for name, (min_val, max_val) in param_space.items():
                individual[name] = random.uniform(min_val, max_val)
            population.append(individual)
        
        best_ever = None
        best_fitness = float('-inf')
        
        for gen in range(generations):
            # Evaluate fitness
            scored = [(ind, fitness_fn(ind)) for ind in population]
            scored.sort(key=lambda x: x[1], reverse=True)
            
            if scored[0][1] > best_fitness:
                best_fitness = scored[0][1]
                best_ever = scored[0][0].copy()
            
            # Selection and reproduction
            new_population = [scored[0][0].copy()]  # Elitism
            
            while len(new_population) < population_size:
                # Tournament selection
                parent1 = random.choice(scored[:5])[0]
                parent2 = random.choice(scored[:5])[0]
                
                # Crossover
                child = {}
                for name in param_space:
                    if random.random() < 0.5:
                        child[name] = parent1[name]
                    else:
                        child[name] = parent2[name]
                
                # Mutation
                for name, (min_val, max_val) in param_space.items():
                    if random.random() < 0.1:
                        child[name] += random.gauss(0, (max_val - min_val) * 0.1)
                        child[name] = max(min_val, min(max_val, child[name]))
                
                new_population.append(child)
            
            population = new_population
        
        self._best_params = best_ever
        self._best_fitness = best_fitness
        self.metrics.tasks_completed += 1
        
        return {
            "best_params": best_ever,
            "best_fitness": best_fitness,
            "generations": generations,
        }
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get optimization history."""
        return self._optimization_history.copy()

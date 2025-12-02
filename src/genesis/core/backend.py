"""
Quantum Execution Backend

Provides the backend interface and implementation for executing
quantum circuits in the GENESIS platform.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from genesis.core.circuit import QuantumCircuit
from genesis.core.state import QuantumState


@dataclass
class ExecutionResult:
    """
    Result of circuit execution.
    
    Attributes:
        counts: Measurement counts for each bitstring.
        statevector: Final statevector (if requested).
        metadata: Additional execution metadata.
    """
    counts: Dict[str, int]
    statevector: Optional[QuantumState] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def total_shots(self) -> int:
        """Total number of measurement shots."""
        return sum(self.counts.values())
    
    def probabilities(self) -> Dict[str, float]:
        """Convert counts to probabilities."""
        total = self.total_shots
        return {k: v / total for k, v in self.counts.items()}
    
    def most_frequent(self) -> str:
        """Return the most frequently measured bitstring."""
        return max(self.counts.keys(), key=lambda k: self.counts[k])


class Backend(ABC):
    """
    Abstract base class for quantum execution backends.
    
    A backend is responsible for executing quantum circuits and
    returning measurement results.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name."""
        pass
    
    @property
    @abstractmethod
    def max_qubits(self) -> int:
        """Maximum supported number of qubits."""
        pass
    
    @abstractmethod
    def run(
        self,
        circuit: QuantumCircuit,
        shots: int = 1024,
        return_statevector: bool = False
    ) -> ExecutionResult:
        """
        Execute a circuit.
        
        Args:
            circuit: The circuit to execute.
            shots: Number of measurement shots.
            return_statevector: Whether to include final statevector.
            
        Returns:
            Execution result.
        """
        pass
    
    def run_batch(
        self,
        circuits: List[QuantumCircuit],
        shots: int = 1024
    ) -> List[ExecutionResult]:
        """
        Execute multiple circuits.
        
        Args:
            circuits: List of circuits.
            shots: Number of shots per circuit.
            
        Returns:
            List of execution results.
        """
        return [self.run(c, shots) for c in circuits]


class SovereignBackend(Backend):
    """
    Zero-dependency statevector simulation backend.
    
    This is the default backend for the GENESIS platform, implementing
    full statevector simulation without any external dependencies.
    
    Attributes:
        _max_qubits: Maximum number of qubits (memory limited).
        _seed: Random seed for reproducibility.
    """
    
    def __init__(
        self,
        max_qubits: int = 20,
        seed: Optional[int] = None
    ) -> None:
        """
        Initialize the backend.
        
        Args:
            max_qubits: Maximum qubits to simulate (default 20).
            seed: Random seed for measurement sampling.
        """
        self._max_qubits = max_qubits
        self._seed = seed
        self._shot_seed = seed if seed else 12345
    
    @property
    def name(self) -> str:
        return "sovereign_simulator"
    
    @property
    def max_qubits(self) -> int:
        return self._max_qubits
    
    def run(
        self,
        circuit: QuantumCircuit,
        shots: int = 1024,
        return_statevector: bool = False
    ) -> ExecutionResult:
        """Execute a circuit using statevector simulation."""
        if circuit.num_qubits > self._max_qubits:
            raise ValueError(
                f"Circuit has {circuit.num_qubits} qubits, "
                f"but backend only supports up to {self._max_qubits}"
            )
        
        # Get final statevector
        state = circuit.get_statevector()
        
        # Sample measurements
        counts = self._sample_measurements(state, shots)
        
        metadata = {
            "backend": self.name,
            "shots": shots,
            "num_qubits": circuit.num_qubits,
            "circuit_depth": circuit.depth,
        }
        
        return ExecutionResult(
            counts=counts,
            statevector=state if return_statevector else None,
            metadata=metadata
        )
    
    def _sample_measurements(
        self,
        state: QuantumState,
        shots: int
    ) -> Dict[str, int]:
        """Sample measurement outcomes from a statevector."""
        probs = state.probabilities()
        counts: Dict[str, int] = {}
        
        # Linear congruential generator for reproducibility
        seed = self._shot_seed
        a, c, m = 1103515245, 12345, 2**31
        
        for _ in range(shots):
            seed = (a * seed + c) % m
            r = seed / m
            
            cumulative = 0.0
            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    bitstring = format(i, f'0{state.num_qubits}b')
                    counts[bitstring] = counts.get(bitstring, 0) + 1
                    break
        
        return counts


class NoisyBackend(Backend):
    """
    Statevector simulator with noise modeling.
    
    Simulates basic noise effects including:
    - Depolarizing noise
    - Amplitude damping
    - Measurement errors
    """
    
    def __init__(
        self,
        max_qubits: int = 20,
        depolarizing_rate: float = 0.001,
        amplitude_damping_rate: float = 0.001,
        measurement_error_rate: float = 0.01,
        seed: Optional[int] = None
    ) -> None:
        """
        Initialize the noisy backend.
        
        Args:
            max_qubits: Maximum qubits to simulate.
            depolarizing_rate: Probability of depolarizing error per gate.
            amplitude_damping_rate: Amplitude damping rate.
            measurement_error_rate: Probability of measurement bit flip.
            seed: Random seed.
        """
        self._max_qubits = max_qubits
        self.depolarizing_rate = depolarizing_rate
        self.amplitude_damping_rate = amplitude_damping_rate
        self.measurement_error_rate = measurement_error_rate
        self._seed = seed if seed else 12345
    
    @property
    def name(self) -> str:
        return "noisy_simulator"
    
    @property
    def max_qubits(self) -> int:
        return self._max_qubits
    
    def run(
        self,
        circuit: QuantumCircuit,
        shots: int = 1024,
        return_statevector: bool = False
    ) -> ExecutionResult:
        """Execute with noise simulation."""
        if circuit.num_qubits > self._max_qubits:
            raise ValueError(
                f"Circuit has {circuit.num_qubits} qubits, "
                f"but backend only supports up to {self._max_qubits}"
            )
        
        # For now, use ideal simulation and add measurement noise
        # Full noise modeling would require density matrix simulation
        state = circuit.get_statevector()
        counts = self._sample_with_noise(state, shots)
        
        metadata = {
            "backend": self.name,
            "shots": shots,
            "depolarizing_rate": self.depolarizing_rate,
            "measurement_error_rate": self.measurement_error_rate,
        }
        
        return ExecutionResult(
            counts=counts,
            statevector=state if return_statevector else None,
            metadata=metadata
        )
    
    def _sample_with_noise(
        self,
        state: QuantumState,
        shots: int
    ) -> Dict[str, int]:
        """Sample measurements with noise."""
        probs = state.probabilities()
        counts: Dict[str, int] = {}
        
        seed = self._seed
        a, c, m = 1103515245, 12345, 2**31
        
        for _ in range(shots):
            # Sample outcome
            seed = (a * seed + c) % m
            r = seed / m
            
            cumulative = 0.0
            outcome = 0
            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    outcome = i
                    break
            
            # Apply measurement errors
            bitstring = format(outcome, f'0{state.num_qubits}b')
            noisy_bits = list(bitstring)
            
            for j in range(len(noisy_bits)):
                seed = (a * seed + c) % m
                if seed / m < self.measurement_error_rate:
                    noisy_bits[j] = '1' if noisy_bits[j] == '0' else '0'
            
            noisy_bitstring = ''.join(noisy_bits)
            counts[noisy_bitstring] = counts.get(noisy_bitstring, 0) + 1
        
        return counts


def get_backend(name: str = "sovereign", **kwargs: Any) -> Backend:
    """
    Get a backend by name.
    
    Args:
        name: Backend name ("sovereign" or "noisy").
        **kwargs: Backend-specific options.
        
    Returns:
        Backend instance.
    """
    backends = {
        "sovereign": SovereignBackend,
        "noisy": NoisyBackend,
    }
    
    if name not in backends:
        raise ValueError(f"Unknown backend: {name}")
    
    return backends[name](**kwargs)

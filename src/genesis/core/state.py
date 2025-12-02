"""
Quantum State Implementation

Provides the QuantumState class for representing and manipulating
quantum state vectors without external dependencies.
"""

from __future__ import annotations
from typing import List, Optional, Tuple, Dict
from genesis.core.complex import Complex
from genesis.core import math as gmath
from genesis.constants import SQRT2_INV


class QuantumState:
    """
    Quantum state vector representation.
    
    A quantum state of n qubits is represented as a vector of 2^n complex
    amplitudes. The state |ψ⟩ = Σᵢ αᵢ|i⟩ where |αᵢ|² is the probability
    of measuring basis state |i⟩.
    
    Attributes:
        num_qubits: Number of qubits in the state.
        amplitudes: List of complex amplitudes.
        
    Example:
        >>> state = QuantumState(2)  # |00⟩
        >>> state.apply_gate(H(), 0)  # Apply Hadamard to qubit 0
        >>> print(state.probabilities())  # [0.5, 0.5, 0, 0]
    """
    
    def __init__(
        self, 
        num_qubits: int, 
        amplitudes: Optional[List[Complex]] = None
    ) -> None:
        """
        Initialize a quantum state.
        
        Args:
            num_qubits: Number of qubits.
            amplitudes: Initial amplitudes. If None, initializes to |0...0⟩.
        """
        if num_qubits < 1:
            raise ValueError("Number of qubits must be at least 1")
        
        self.num_qubits = num_qubits
        self._dim = 1 << num_qubits  # 2^n
        
        if amplitudes is None:
            # Initialize to |0...0⟩
            self.amplitudes = [Complex(0.0, 0.0) for _ in range(self._dim)]
            self.amplitudes[0] = Complex(1.0, 0.0)
        else:
            if len(amplitudes) != self._dim:
                raise ValueError(
                    f"Expected {self._dim} amplitudes, got {len(amplitudes)}"
                )
            self.amplitudes = [Complex(a.real, a.imag) for a in amplitudes]
    
    @classmethod
    def from_basis(cls, num_qubits: int, basis_state: int) -> QuantumState:
        """
        Create a computational basis state.
        
        Args:
            num_qubits: Number of qubits.
            basis_state: Integer index of the basis state.
            
        Returns:
            QuantumState initialized to |basis_state⟩.
        """
        dim = 1 << num_qubits
        if basis_state < 0 or basis_state >= dim:
            raise ValueError(f"Basis state must be in [0, {dim-1}]")
        
        amplitudes = [Complex(0.0, 0.0) for _ in range(dim)]
        amplitudes[basis_state] = Complex(1.0, 0.0)
        return cls(num_qubits, amplitudes)
    
    @classmethod
    def from_string(cls, bitstring: str) -> QuantumState:
        """
        Create a state from a bitstring like "01" or "101".
        
        Args:
            bitstring: String of 0s and 1s.
            
        Returns:
            QuantumState initialized to the specified basis state.
        """
        num_qubits = len(bitstring)
        basis_state = int(bitstring, 2)
        return cls.from_basis(num_qubits, basis_state)
    
    @classmethod
    def bell_state(cls, which: int = 0) -> QuantumState:
        """
        Create a Bell state.
        
        Args:
            which: Which Bell state (0-3):
                0: |Φ+⟩ = (|00⟩ + |11⟩)/√2
                1: |Φ-⟩ = (|00⟩ - |11⟩)/√2
                2: |Ψ+⟩ = (|01⟩ + |10⟩)/√2
                3: |Ψ-⟩ = (|01⟩ - |10⟩)/√2
                
        Returns:
            The requested Bell state.
        """
        amplitudes = [Complex(0.0, 0.0) for _ in range(4)]
        s = SQRT2_INV
        
        if which == 0:  # |Φ+⟩
            amplitudes[0] = Complex(s, 0.0)
            amplitudes[3] = Complex(s, 0.0)
        elif which == 1:  # |Φ-⟩
            amplitudes[0] = Complex(s, 0.0)
            amplitudes[3] = Complex(-s, 0.0)
        elif which == 2:  # |Ψ+⟩
            amplitudes[1] = Complex(s, 0.0)
            amplitudes[2] = Complex(s, 0.0)
        elif which == 3:  # |Ψ-⟩
            amplitudes[1] = Complex(s, 0.0)
            amplitudes[2] = Complex(-s, 0.0)
        else:
            raise ValueError("Bell state index must be 0-3")
        
        return cls(2, amplitudes)
    
    @classmethod
    def ghz_state(cls, num_qubits: int) -> QuantumState:
        """
        Create a GHZ (Greenberger–Horne–Zeilinger) state.
        
        |GHZ⟩ = (|00...0⟩ + |11...1⟩)/√2
        
        Args:
            num_qubits: Number of qubits (at least 2).
            
        Returns:
            The GHZ state.
        """
        if num_qubits < 2:
            raise ValueError("GHZ state requires at least 2 qubits")
        
        dim = 1 << num_qubits
        amplitudes = [Complex(0.0, 0.0) for _ in range(dim)]
        s = SQRT2_INV
        amplitudes[0] = Complex(s, 0.0)
        amplitudes[dim - 1] = Complex(s, 0.0)
        
        return cls(num_qubits, amplitudes)
    
    def copy(self) -> QuantumState:
        """Create a copy of this state."""
        return QuantumState(
            self.num_qubits,
            [Complex(a.real, a.imag) for a in self.amplitudes]
        )
    
    def normalize(self) -> None:
        """Normalize the state in place."""
        norm = gmath.sqrt(sum(a.modulus_squared() for a in self.amplitudes))
        if norm > 0:
            for i in range(len(self.amplitudes)):
                self.amplitudes[i] = self.amplitudes[i] / norm
    
    def is_normalized(self, tolerance: float = 1e-10) -> bool:
        """Check if the state is normalized."""
        total = sum(a.modulus_squared() for a in self.amplitudes)
        return abs(total - 1.0) < tolerance
    
    def probabilities(self) -> List[float]:
        """
        Get measurement probabilities for each basis state.
        
        Returns:
            List of probabilities |αᵢ|² for each basis state.
        """
        return [a.modulus_squared() for a in self.amplitudes]
    
    def apply1(
        self, 
        gate: List[List[Complex]], 
        target: int
    ) -> None:
        """
        Apply a single-qubit gate to the state.
        
        Args:
            gate: 2×2 gate matrix.
            target: Target qubit index (0-indexed from right/LSB).
        """
        if target < 0 or target >= self.num_qubits:
            raise ValueError(f"Target qubit {target} out of range")
        
        # Apply gate to each pair of amplitudes differing in target bit
        mask = 1 << target
        for i in range(self._dim):
            if i & mask == 0:
                j = i | mask
                a0 = self.amplitudes[i]
                a1 = self.amplitudes[j]
                self.amplitudes[i] = gate[0][0] * a0 + gate[0][1] * a1
                self.amplitudes[j] = gate[1][0] * a0 + gate[1][1] * a1
    
    def apply2(
        self,
        gate: List[List[Complex]],
        control: int,
        target: int
    ) -> None:
        """
        Apply a two-qubit gate to the state.
        
        Args:
            gate: 4×4 gate matrix.
            control: Control qubit index.
            target: Target qubit index.
        """
        if control == target:
            raise ValueError("Control and target must be different")
        if not (0 <= control < self.num_qubits and 0 <= target < self.num_qubits):
            raise ValueError("Qubit indices out of range")
        
        mask_c = 1 << control
        mask_t = 1 << target
        
        # Process each group of 4 basis states
        processed = [False] * self._dim
        for i in range(self._dim):
            if processed[i]:
                continue
            
            # Get indices of the 4 basis states
            i00 = i & ~mask_c & ~mask_t
            i01 = i00 | mask_t
            i10 = i00 | mask_c
            i11 = i00 | mask_c | mask_t
            
            # Mark as processed
            processed[i00] = processed[i01] = True
            processed[i10] = processed[i11] = True
            
            # Get current amplitudes
            a = [
                self.amplitudes[i00],
                self.amplitudes[i01],
                self.amplitudes[i10],
                self.amplitudes[i11]
            ]
            
            # Apply gate
            for k in range(4):
                idx = [i00, i01, i10, i11][k]
                self.amplitudes[idx] = sum(
                    gate[k][m] * a[m] for m in range(4)
                )
    
    def measure(self, shots: int = 1) -> Dict[str, int]:
        """
        Perform measurement in the computational basis.
        
        This simulates quantum measurement by sampling from the probability
        distribution. The state is NOT collapsed.
        
        Args:
            shots: Number of measurement samples.
            
        Returns:
            Dictionary mapping bitstrings to counts.
        """
        probs = self.probabilities()
        counts: Dict[str, int] = {}
        
        # Simple random sampling using linear congruential generator
        seed = 12345
        a, c, m = 1103515245, 12345, 2**31
        
        for _ in range(shots):
            seed = (a * seed + c) % m
            r = seed / m
            
            cumulative = 0.0
            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    bitstring = format(i, f'0{self.num_qubits}b')
                    counts[bitstring] = counts.get(bitstring, 0) + 1
                    break
        
        return counts
    
    def measure_qubit(self, qubit: int) -> Tuple[int, QuantumState]:
        """
        Measure a single qubit, collapsing the state.
        
        Args:
            qubit: Index of qubit to measure.
            
        Returns:
            Tuple of (measured_value, collapsed_state).
        """
        if qubit < 0 or qubit >= self.num_qubits:
            raise ValueError(f"Qubit {qubit} out of range")
        
        mask = 1 << qubit
        
        # Calculate probability of measuring 0
        prob_0 = sum(
            self.amplitudes[i].modulus_squared()
            for i in range(self._dim)
            if (i & mask) == 0
        )
        
        # Simple random choice
        seed = 42  # Deterministic for reproducibility in tests
        measured = 0 if (seed % 100) / 100 < prob_0 else 1
        
        # Collapse the state
        new_amplitudes = []
        for i in range(self._dim):
            if ((i >> qubit) & 1) == measured:
                new_amplitudes.append(self.amplitudes[i])
            else:
                new_amplitudes.append(Complex(0.0, 0.0))
        
        new_state = QuantumState(self.num_qubits, new_amplitudes)
        new_state.normalize()
        
        return measured, new_state
    
    def fidelity(self, other: QuantumState) -> float:
        """
        Calculate fidelity between this state and another.
        
        F(ψ, φ) = |⟨ψ|φ⟩|²
        
        Args:
            other: The other quantum state.
            
        Returns:
            Fidelity value in [0, 1].
        """
        if self.num_qubits != other.num_qubits:
            raise ValueError("States must have same number of qubits")
        
        # Calculate inner product ⟨ψ|φ⟩
        inner = Complex(0.0, 0.0)
        for i in range(self._dim):
            inner = inner + self.amplitudes[i].conjugate() * other.amplitudes[i]
        
        return inner.modulus_squared()
    
    def expectation(self, observable: List[List[Complex]]) -> float:
        """
        Calculate expectation value of an observable.
        
        ⟨O⟩ = ⟨ψ|O|ψ⟩
        
        Args:
            observable: Hermitian matrix representing the observable.
            
        Returns:
            Real expectation value.
        """
        if len(observable) != self._dim or len(observable[0]) != self._dim:
            raise ValueError("Observable dimensions don't match state")
        
        result = Complex(0.0, 0.0)
        for i in range(self._dim):
            for j in range(self._dim):
                result = result + (
                    self.amplitudes[i].conjugate() * 
                    observable[i][j] * 
                    self.amplitudes[j]
                )
        
        return result.real
    
    def tensor(self, other: QuantumState) -> QuantumState:
        """
        Compute tensor product with another state.
        
        |ψ⟩ ⊗ |φ⟩
        
        Args:
            other: The other quantum state.
            
        Returns:
            New state representing the tensor product.
        """
        new_qubits = self.num_qubits + other.num_qubits
        new_amplitudes = []
        
        for i in range(self._dim):
            for j in range(other._dim):
                new_amplitudes.append(self.amplitudes[i] * other.amplitudes[j])
        
        return QuantumState(new_qubits, new_amplitudes)
    
    def __repr__(self) -> str:
        """String representation."""
        terms = []
        for i, amp in enumerate(self.amplitudes):
            if amp.modulus_squared() > 1e-10:
                bitstring = format(i, f'0{self.num_qubits}b')
                terms.append(f"{amp}|{bitstring}⟩")
        return " + ".join(terms) if terms else "0"
    
    def __eq__(self, other: object) -> bool:
        """Check equality with tolerance."""
        if not isinstance(other, QuantumState):
            return NotImplemented
        if self.num_qubits != other.num_qubits:
            return False
        return all(
            (self.amplitudes[i] - other.amplitudes[i]).modulus() < 1e-10
            for i in range(self._dim)
        )

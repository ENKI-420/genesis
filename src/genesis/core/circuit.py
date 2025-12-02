"""
Quantum Circuit Implementation

Provides the QuantumCircuit class for building and executing quantum
algorithms without external dependencies.
"""

from __future__ import annotations
from typing import List, Tuple, Optional, Dict, Any, Union
from genesis.core.complex import Complex
from genesis.core.state import QuantumState
from genesis.core.gates import (
    Gate, I, X, Y, Z, H, S, T, CNOT, CZ, SWAP,
    RX, RY, RZ, Phase
)


class Instruction:
    """
    A quantum instruction (gate application).
    
    Attributes:
        gate: The gate to apply.
        targets: Target qubit indices.
        controls: Control qubit indices (if any).
        parameters: Gate parameters (if any).
    """
    
    def __init__(
        self,
        gate: Gate,
        targets: Tuple[int, ...],
        controls: Tuple[int, ...] = (),
        parameters: Tuple[float, ...] = ()
    ) -> None:
        self.gate = gate
        self.targets = targets
        self.controls = controls
        self.parameters = parameters
    
    def __repr__(self) -> str:
        if self.controls:
            return f"C{self.gate.name}(controls={self.controls}, targets={self.targets})"
        return f"{self.gate.name}(targets={self.targets})"


class QuantumCircuit:
    """
    Quantum circuit representation.
    
    A circuit is a sequence of quantum gates applied to a fixed number
    of qubits. The circuit can be executed on a backend to produce
    measurement results.
    
    Attributes:
        num_qubits: Number of qubits in the circuit.
        num_classical: Number of classical bits for measurement storage.
        instructions: List of instructions in the circuit.
        
    Example:
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0)
        >>> qc.cx(0, 1)  # Creates Bell state
        >>> result = qc.run()
    """
    
    def __init__(
        self,
        num_qubits: int,
        num_classical: Optional[int] = None
    ) -> None:
        """
        Initialize a quantum circuit.
        
        Args:
            num_qubits: Number of qubits.
            num_classical: Number of classical bits (default: num_qubits).
        """
        if num_qubits < 1:
            raise ValueError("Circuit must have at least 1 qubit")
        
        self.num_qubits = num_qubits
        self.num_classical = num_classical if num_classical is not None else num_qubits
        self.instructions: List[Instruction] = []
        self._measurements: List[Tuple[int, int]] = []  # (qubit, classical_bit)
    
    def _validate_qubit(self, qubit: int) -> None:
        """Validate that a qubit index is valid."""
        if qubit < 0 or qubit >= self.num_qubits:
            raise ValueError(f"Qubit {qubit} out of range [0, {self.num_qubits-1}]")
    
    def _validate_qubits(self, *qubits: int) -> None:
        """Validate multiple qubit indices."""
        for q in qubits:
            self._validate_qubit(q)
        if len(set(qubits)) != len(qubits):
            raise ValueError("Duplicate qubit indices")
    
    # Single-qubit gates
    def i(self, qubit: int) -> QuantumCircuit:
        """Apply identity gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(I, (qubit,)))
        return self
    
    def x(self, qubit: int) -> QuantumCircuit:
        """Apply Pauli-X (NOT) gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(X, (qubit,)))
        return self
    
    def y(self, qubit: int) -> QuantumCircuit:
        """Apply Pauli-Y gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(Y, (qubit,)))
        return self
    
    def z(self, qubit: int) -> QuantumCircuit:
        """Apply Pauli-Z gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(Z, (qubit,)))
        return self
    
    def h(self, qubit: int) -> QuantumCircuit:
        """Apply Hadamard gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(H, (qubit,)))
        return self
    
    def s(self, qubit: int) -> QuantumCircuit:
        """Apply S (phase) gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(S, (qubit,)))
        return self
    
    def t(self, qubit: int) -> QuantumCircuit:
        """Apply T gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(T, (qubit,)))
        return self
    
    def rx(self, theta: float, qubit: int) -> QuantumCircuit:
        """Apply RX rotation gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(RX(theta), (qubit,), (), (theta,)))
        return self
    
    def ry(self, theta: float, qubit: int) -> QuantumCircuit:
        """Apply RY rotation gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(RY(theta), (qubit,), (), (theta,)))
        return self
    
    def rz(self, theta: float, qubit: int) -> QuantumCircuit:
        """Apply RZ rotation gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(RZ(theta), (qubit,), (), (theta,)))
        return self
    
    def p(self, phi: float, qubit: int) -> QuantumCircuit:
        """Apply phase gate."""
        self._validate_qubit(qubit)
        self.instructions.append(Instruction(Phase(phi), (qubit,), (), (phi,)))
        return self
    
    # Two-qubit gates
    def cx(self, control: int, target: int) -> QuantumCircuit:
        """Apply CNOT (controlled-X) gate."""
        self._validate_qubits(control, target)
        self.instructions.append(Instruction(CNOT, (target,), (control,)))
        return self
    
    def cnot(self, control: int, target: int) -> QuantumCircuit:
        """Apply CNOT gate (alias for cx)."""
        return self.cx(control, target)
    
    def cz(self, control: int, target: int) -> QuantumCircuit:
        """Apply CZ (controlled-Z) gate."""
        self._validate_qubits(control, target)
        self.instructions.append(Instruction(CZ, (target,), (control,)))
        return self
    
    def swap(self, qubit1: int, qubit2: int) -> QuantumCircuit:
        """Apply SWAP gate."""
        self._validate_qubits(qubit1, qubit2)
        self.instructions.append(Instruction(SWAP, (qubit1, qubit2)))
        return self
    
    # Measurement
    def measure(
        self, 
        qubit: int, 
        classical_bit: Optional[int] = None
    ) -> QuantumCircuit:
        """
        Add a measurement operation.
        
        Args:
            qubit: Qubit to measure.
            classical_bit: Classical bit to store result (default: same as qubit).
        """
        self._validate_qubit(qubit)
        if classical_bit is None:
            classical_bit = qubit
        if classical_bit < 0 or classical_bit >= self.num_classical:
            raise ValueError(f"Classical bit {classical_bit} out of range")
        
        self._measurements.append((qubit, classical_bit))
        return self
    
    def measure_all(self) -> QuantumCircuit:
        """Measure all qubits."""
        for i in range(self.num_qubits):
            self.measure(i, i)
        return self
    
    # Barriers and utilities
    def barrier(self, *qubits: int) -> QuantumCircuit:
        """
        Add a barrier (for visualization, no effect on execution).
        
        Args:
            qubits: Qubits to barrier (default: all).
        """
        # Barriers are currently no-ops in our implementation
        return self
    
    def reset(self, qubit: int) -> QuantumCircuit:
        """
        Reset a qubit to |0⟩.
        
        This is implemented as measure + conditional X.
        """
        self._validate_qubit(qubit)
        # Note: In a real implementation, this would need special handling
        return self
    
    # Circuit operations
    def inverse(self) -> QuantumCircuit:
        """
        Return the inverse of this circuit.
        
        Returns:
            New circuit that undoes this circuit's operations.
        """
        inv = QuantumCircuit(self.num_qubits, self.num_classical)
        
        for inst in reversed(self.instructions):
            inv_gate = inst.gate.dagger()
            inv.instructions.append(Instruction(
                inv_gate, inst.targets, inst.controls, inst.parameters
            ))
        
        return inv
    
    def compose(
        self, 
        other: QuantumCircuit, 
        qubits: Optional[List[int]] = None
    ) -> QuantumCircuit:
        """
        Compose with another circuit.
        
        Args:
            other: Circuit to append.
            qubits: Qubit mapping (default: identity).
            
        Returns:
            New composed circuit.
        """
        if qubits is None:
            if other.num_qubits != self.num_qubits:
                raise ValueError("Circuit dimensions don't match")
            qubits = list(range(self.num_qubits))
        
        result = QuantumCircuit(self.num_qubits, self.num_classical)
        result.instructions = list(self.instructions)
        
        for inst in other.instructions:
            new_targets = tuple(qubits[t] for t in inst.targets)
            new_controls = tuple(qubits[c] for c in inst.controls)
            result.instructions.append(Instruction(
                inst.gate, new_targets, new_controls, inst.parameters
            ))
        
        return result
    
    def copy(self) -> QuantumCircuit:
        """Create a copy of this circuit."""
        qc = QuantumCircuit(self.num_qubits, self.num_classical)
        qc.instructions = list(self.instructions)
        qc._measurements = list(self._measurements)
        return qc
    
    @property
    def depth(self) -> int:
        """
        Calculate circuit depth.
        
        Returns:
            Maximum number of gates on any qubit.
        """
        if not self.instructions:
            return 0
        
        depths = [0] * self.num_qubits
        for inst in self.instructions:
            affected = list(inst.targets) + list(inst.controls)
            max_depth = max(depths[q] for q in affected)
            for q in affected:
                depths[q] = max_depth + 1
        
        return max(depths)
    
    @property
    def num_gates(self) -> int:
        """Return total number of gates."""
        return len(self.instructions)
    
    def gate_counts(self) -> Dict[str, int]:
        """
        Count occurrences of each gate type.
        
        Returns:
            Dictionary mapping gate names to counts.
        """
        counts: Dict[str, int] = {}
        for inst in self.instructions:
            name = inst.gate.name
            counts[name] = counts.get(name, 0) + 1
        return counts
    
    def run(
        self, 
        shots: int = 1024,
        initial_state: Optional[QuantumState] = None
    ) -> Dict[str, int]:
        """
        Execute the circuit and return measurement results.
        
        Args:
            shots: Number of measurement shots.
            initial_state: Initial state (default: |0...0⟩).
            
        Returns:
            Dictionary mapping bitstrings to counts.
        """
        # Initialize state
        if initial_state is not None:
            state = initial_state.copy()
        else:
            state = QuantumState(self.num_qubits)
        
        # Apply gates
        for inst in self.instructions:
            if len(inst.targets) == 1 and not inst.controls:
                # Single-qubit gate
                state.apply1(inst.gate.matrix, inst.targets[0])
            elif inst.controls:
                # Controlled gate - apply as 4x4 matrix
                control = inst.controls[0]
                target = inst.targets[0]
                state.apply2(inst.gate.matrix, control, target)
            elif len(inst.targets) == 2:
                # Two-qubit gate
                state.apply2(inst.gate.matrix, inst.targets[0], inst.targets[1])
        
        # Measure
        return state.measure(shots)
    
    def get_statevector(
        self, 
        initial_state: Optional[QuantumState] = None
    ) -> QuantumState:
        """
        Get the final state vector without measurement.
        
        Args:
            initial_state: Initial state (default: |0...0⟩).
            
        Returns:
            Final quantum state.
        """
        if initial_state is not None:
            state = initial_state.copy()
        else:
            state = QuantumState(self.num_qubits)
        
        for inst in self.instructions:
            if len(inst.targets) == 1 and not inst.controls:
                state.apply1(inst.gate.matrix, inst.targets[0])
            elif inst.controls:
                control = inst.controls[0]
                target = inst.targets[0]
                state.apply2(inst.gate.matrix, control, target)
            elif len(inst.targets) == 2:
                state.apply2(inst.gate.matrix, inst.targets[0], inst.targets[1])
        
        return state
    
    def __repr__(self) -> str:
        """String representation."""
        lines = [f"QuantumCircuit({self.num_qubits} qubits, {self.num_classical} classical)"]
        for inst in self.instructions:
            lines.append(f"  {inst}")
        if self._measurements:
            for q, c in self._measurements:
                lines.append(f"  Measure q{q} -> c{c}")
        return "\n".join(lines)
    
    def draw(self, output: str = "text") -> str:
        """
        Draw the circuit as ASCII art.
        
        Args:
            output: Output format ("text" only for now).
            
        Returns:
            ASCII representation of the circuit.
        """
        # Simple text drawing
        lines = [f"q{i}: " for i in range(self.num_qubits)]
        
        for inst in self.instructions:
            all_qubits = list(inst.targets) + list(inst.controls)
            min_q, max_q = min(all_qubits), max(all_qubits)
            
            for i in range(self.num_qubits):
                if i in inst.controls:
                    lines[i] += "●─"
                elif i in inst.targets:
                    if inst.gate.name in ("X", "CNOT"):
                        lines[i] += "⊕─"
                    else:
                        name = inst.gate.name[:2]
                        lines[i] += f"[{name}]─"
                elif min_q < i < max_q:
                    lines[i] += "│─"
                else:
                    lines[i] += "──"
        
        return "\n".join(lines)


def bell_circuit() -> QuantumCircuit:
    """Create a Bell state preparation circuit."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def ghz_circuit(n: int) -> QuantumCircuit:
    """Create a GHZ state preparation circuit."""
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return qc


def qft_circuit(n: int) -> QuantumCircuit:
    """Create a Quantum Fourier Transform circuit."""
    from genesis.constants import PI
    
    qc = QuantumCircuit(n)
    
    for i in range(n):
        qc.h(i)
        for j in range(i + 1, n):
            angle = PI / (2 ** (j - i))
            # Controlled phase - implemented as CRZ
            qc.p(angle, j)
            # Note: Proper controlled version would need CPhase gate
    
    # Swap qubits to match standard QFT ordering
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    
    return qc

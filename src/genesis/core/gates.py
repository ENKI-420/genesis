"""
Quantum Gate Implementation

Provides standard quantum gates and gate operations for the GENESIS platform.
All gates are implemented without external dependencies.
"""

from __future__ import annotations
from typing import List, Callable, Optional
from genesis.core.complex import Complex
from genesis.core import math as gmath
from genesis.constants import PI, SQRT2_INV


class Gate:
    """
    Base class for quantum gates.
    
    A gate is represented by its unitary matrix. Single-qubit gates
    are 2×2 matrices, two-qubit gates are 4×4 matrices.
    
    Attributes:
        name: Human-readable name of the gate.
        matrix: The unitary matrix representation.
        num_qubits: Number of qubits the gate acts on.
    """
    
    def __init__(
        self, 
        name: str, 
        matrix: List[List[Complex]], 
        num_qubits: int = 1
    ) -> None:
        """
        Initialize a gate.
        
        Args:
            name: Gate name.
            matrix: Unitary matrix.
            num_qubits: Number of qubits (default 1).
        """
        self.name = name
        self.matrix = matrix
        self.num_qubits = num_qubits
    
    @property
    def dim(self) -> int:
        """Dimension of the gate matrix."""
        return 1 << self.num_qubits
    
    def dagger(self) -> Gate:
        """
        Return the conjugate transpose (adjoint) of the gate.
        
        Returns:
            New Gate representing the adjoint.
        """
        n = len(self.matrix)
        adjoint = [
            [self.matrix[j][i].conjugate() for j in range(n)]
            for i in range(n)
        ]
        return Gate(f"{self.name}†", adjoint, self.num_qubits)
    
    def compose(self, other: Gate) -> Gate:
        """
        Compose with another gate (matrix multiplication).
        
        Args:
            other: Gate to compose with.
            
        Returns:
            New Gate representing self @ other.
        """
        if self.num_qubits != other.num_qubits:
            raise ValueError("Gates must have same number of qubits")
        
        n = len(self.matrix)
        result = [[Complex(0.0, 0.0) for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] = result[i][j] + self.matrix[i][k] * other.matrix[k][j]
        
        return Gate(f"({self.name}∘{other.name})", result, self.num_qubits)
    
    def tensor(self, other: Gate) -> Gate:
        """
        Compute tensor product with another gate.
        
        Args:
            other: Gate to tensor with.
            
        Returns:
            New Gate representing self ⊗ other.
        """
        n1, n2 = len(self.matrix), len(other.matrix)
        n = n1 * n2
        
        result = [[Complex(0.0, 0.0) for _ in range(n)] for _ in range(n)]
        
        for i in range(n1):
            for j in range(n1):
                for k in range(n2):
                    for l in range(n2):
                        result[i * n2 + k][j * n2 + l] = (
                            self.matrix[i][j] * other.matrix[k][l]
                        )
        
        return Gate(
            f"({self.name}⊗{other.name})", 
            result, 
            self.num_qubits + other.num_qubits
        )
    
    def is_unitary(self, tolerance: float = 1e-10) -> bool:
        """Check if the gate is unitary (U†U = I)."""
        n = len(self.matrix)
        adjoint = self.dagger()
        
        for i in range(n):
            for j in range(n):
                expected = 1.0 if i == j else 0.0
                computed = Complex(0.0, 0.0)
                for k in range(n):
                    computed = computed + adjoint.matrix[i][k] * self.matrix[k][j]
                if abs(computed.real - expected) > tolerance or abs(computed.imag) > tolerance:
                    return False
        return True
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Gate({self.name})"
    
    def __matmul__(self, other: Gate) -> Gate:
        """Matrix multiplication operator."""
        return self.compose(other)


# =============================================================================
# SINGLE-QUBIT GATES
# =============================================================================

def _make_single_gate(
    name: str,
    m00: Complex,
    m01: Complex,
    m10: Complex,
    m11: Complex
) -> Gate:
    """Helper to create a single-qubit gate."""
    return Gate(name, [[m00, m01], [m10, m11]], 1)


# Identity gate
I = _make_single_gate(
    "I",
    Complex(1.0, 0.0), Complex(0.0, 0.0),
    Complex(0.0, 0.0), Complex(1.0, 0.0)
)

# Pauli-X (NOT) gate
X = _make_single_gate(
    "X",
    Complex(0.0, 0.0), Complex(1.0, 0.0),
    Complex(1.0, 0.0), Complex(0.0, 0.0)
)

# Pauli-Y gate
Y = _make_single_gate(
    "Y",
    Complex(0.0, 0.0), Complex(0.0, -1.0),
    Complex(0.0, 1.0), Complex(0.0, 0.0)
)

# Pauli-Z gate
Z = _make_single_gate(
    "Z",
    Complex(1.0, 0.0), Complex(0.0, 0.0),
    Complex(0.0, 0.0), Complex(-1.0, 0.0)
)

# Hadamard gate
H = _make_single_gate(
    "H",
    Complex(SQRT2_INV, 0.0), Complex(SQRT2_INV, 0.0),
    Complex(SQRT2_INV, 0.0), Complex(-SQRT2_INV, 0.0)
)

# S gate (Phase gate, √Z)
S = _make_single_gate(
    "S",
    Complex(1.0, 0.0), Complex(0.0, 0.0),
    Complex(0.0, 0.0), Complex(0.0, 1.0)
)

# T gate (π/8 gate, √S)
T = _make_single_gate(
    "T",
    Complex(1.0, 0.0), Complex(0.0, 0.0),
    Complex(0.0, 0.0), Complex(gmath.cos(PI/4), gmath.sin(PI/4))
)


def RX(theta: float) -> Gate:
    """
    Rotation around X-axis.
    
    RX(θ) = cos(θ/2)I - i*sin(θ/2)X
    
    Args:
        theta: Rotation angle in radians.
        
    Returns:
        RX gate.
    """
    c = gmath.cos(theta / 2)
    s = gmath.sin(theta / 2)
    return _make_single_gate(
        f"RX({theta:.3f})",
        Complex(c, 0.0), Complex(0.0, -s),
        Complex(0.0, -s), Complex(c, 0.0)
    )


def RY(theta: float) -> Gate:
    """
    Rotation around Y-axis.
    
    RY(θ) = cos(θ/2)I - i*sin(θ/2)Y
    
    Args:
        theta: Rotation angle in radians.
        
    Returns:
        RY gate.
    """
    c = gmath.cos(theta / 2)
    s = gmath.sin(theta / 2)
    return _make_single_gate(
        f"RY({theta:.3f})",
        Complex(c, 0.0), Complex(-s, 0.0),
        Complex(s, 0.0), Complex(c, 0.0)
    )


def RZ(theta: float) -> Gate:
    """
    Rotation around Z-axis.
    
    RZ(θ) = exp(-iθZ/2) = diag(e^{-iθ/2}, e^{iθ/2})
    
    Args:
        theta: Rotation angle in radians.
        
    Returns:
        RZ gate.
    """
    c = gmath.cos(theta / 2)
    s = gmath.sin(theta / 2)
    return _make_single_gate(
        f"RZ({theta:.3f})",
        Complex(c, -s), Complex(0.0, 0.0),
        Complex(0.0, 0.0), Complex(c, s)
    )


def Phase(phi: float) -> Gate:
    """
    Phase gate.
    
    P(φ) = diag(1, e^{iφ})
    
    Args:
        phi: Phase angle in radians.
        
    Returns:
        Phase gate.
    """
    return _make_single_gate(
        f"P({phi:.3f})",
        Complex(1.0, 0.0), Complex(0.0, 0.0),
        Complex(0.0, 0.0), Complex(gmath.cos(phi), gmath.sin(phi))
    )


def U3(theta: float, phi: float, lam: float) -> Gate:
    """
    General single-qubit rotation.
    
    U3(θ, φ, λ) = RZ(φ) RY(θ) RZ(λ)
    
    Args:
        theta: Polar angle.
        phi: First azimuthal angle.
        lam: Second azimuthal angle.
        
    Returns:
        U3 gate.
    """
    c = gmath.cos(theta / 2)
    s = gmath.sin(theta / 2)
    
    return _make_single_gate(
        f"U3({theta:.3f},{phi:.3f},{lam:.3f})",
        Complex(c, 0.0),
        Complex(
            -s * gmath.cos(lam),
            -s * gmath.sin(lam)
        ),
        Complex(
            s * gmath.cos(phi),
            s * gmath.sin(phi)
        ),
        Complex(
            c * gmath.cos(phi + lam),
            c * gmath.sin(phi + lam)
        )
    )


# =============================================================================
# TWO-QUBIT GATES
# =============================================================================

def _make_two_gate(name: str, matrix: List[List[Complex]]) -> Gate:
    """Helper to create a two-qubit gate."""
    return Gate(name, matrix, 2)


# CNOT (Controlled-X) gate
CNOT = _make_two_gate("CNOT", [
    [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0)],
])

# CZ (Controlled-Z) gate
CZ = _make_two_gate("CZ", [
    [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(-1.0, 0.0)],
])

# SWAP gate
SWAP = _make_two_gate("SWAP", [
    [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
    [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0)],
])


def CRZ(theta: float) -> Gate:
    """
    Controlled RZ gate.
    
    Args:
        theta: Rotation angle.
        
    Returns:
        CRZ gate.
    """
    c = gmath.cos(theta / 2)
    s = gmath.sin(theta / 2)
    return _make_two_gate(f"CRZ({theta:.3f})", [
        [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(c, -s), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(c, s)],
    ])


def iSWAP() -> Gate:
    """
    iSWAP gate.
    
    Returns:
        iSWAP gate.
    """
    return _make_two_gate("iSWAP", [
        [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 1.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 1.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(1.0, 0.0)],
    ])


def FSIM(theta: float, phi: float) -> Gate:
    """
    fSim (fermionic simulation) gate.
    
    Args:
        theta: Swap angle.
        phi: Controlled phase.
        
    Returns:
        fSim gate.
    """
    c = gmath.cos(theta)
    s = gmath.sin(theta)
    cp = gmath.cos(phi)
    sp = gmath.sin(phi)
    
    return _make_two_gate(f"fSim({theta:.3f},{phi:.3f})", [
        [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(c, 0.0), Complex(0.0, -s), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, -s), Complex(c, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(cp, -sp)],
    ])


# =============================================================================
# GATE UTILITIES
# =============================================================================

def controlled(gate: Gate) -> Gate:
    """
    Create a controlled version of a single-qubit gate.
    
    Args:
        gate: The gate to control.
        
    Returns:
        Controlled gate.
    """
    if gate.num_qubits != 1:
        raise ValueError("Can only control single-qubit gates")
    
    matrix = [
        [Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(1.0, 0.0), Complex(0.0, 0.0), Complex(0.0, 0.0)],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), gate.matrix[0][0], gate.matrix[0][1]],
        [Complex(0.0, 0.0), Complex(0.0, 0.0), gate.matrix[1][0], gate.matrix[1][1]],
    ]
    
    return _make_two_gate(f"C{gate.name}", matrix)


def power(gate: Gate, n: float) -> Gate:
    """
    Compute gate raised to a power.
    
    For a gate U with eigendecomposition U = VDV†,
    U^n = V D^n V†
    
    Args:
        gate: The gate.
        n: The power.
        
    Returns:
        Gate raised to the power n.
    """
    # For single-qubit gates, use the rotation decomposition
    if gate.num_qubits != 1:
        raise NotImplementedError("Power only implemented for single-qubit gates")
    
    # TODO: Implement proper eigendecomposition
    # For now, use matrix multiplication for integer powers
    if n == int(n) and n >= 0:
        result = I
        for _ in range(int(n)):
            result = result.compose(gate)
        return result
    
    raise NotImplementedError("Non-integer powers not yet implemented")

"""
GENESIS Core Module

Zero-dependency quantum simulation engine providing:
- Sovereign complex number implementation
- Quantum state vectors
- Quantum gates
- Quantum circuits
- Execution backend
"""

from genesis.core.complex import Complex
from genesis.core.state import QuantumState
from genesis.core.gates import (
    Gate,
    I,
    X,
    Y,
    Z,
    H,
    S,
    T,
    CNOT,
    CZ,
    SWAP,
    RX,
    RY,
    RZ,
)
from genesis.core.circuit import QuantumCircuit
from genesis.core.backend import Backend, SovereignBackend

__all__ = [
    "Complex",
    "QuantumState",
    "Gate",
    "I",
    "X",
    "Y",
    "Z",
    "H",
    "S",
    "T",
    "CNOT",
    "CZ",
    "SWAP",
    "RX",
    "RY",
    "RZ",
    "QuantumCircuit",
    "Backend",
    "SovereignBackend",
]

"""Tests for quantum gates."""

import pytest
from genesis.core.gates import H, X, Y, Z, CNOT
from genesis.core.state import QuantumState


class TestGates:
    def test_x_gate(self):
        zero = QuantumState.zero(1)
        one = X.apply(zero, 0)
        assert abs(one.probability(1) - 1.0) < 1e-10

    def test_hadamard_creates_superposition(self):
        zero = QuantumState.zero(1)
        plus = H.apply(zero, 0)
        assert abs(plus.probability(0) - 0.5) < 1e-10
        assert abs(plus.probability(1) - 0.5) < 1e-10

    def test_hadamard_squared_is_identity(self):
        zero = QuantumState.zero(1)
        result = H.apply(H.apply(zero, 0), 0)
        assert abs(result.probability(0) - 1.0) < 1e-10

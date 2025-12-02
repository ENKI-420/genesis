"""Tests for quantum state implementation."""

import pytest
from genesis.core.state import QuantumState


class TestQuantumState:
    def test_zero_state(self):
        state = QuantumState.zero(1)
        assert abs(state.probability(0) - 1.0) < 1e-10
        assert abs(state.probability(1)) < 1e-10

    def test_one_state(self):
        state = QuantumState.one(1)
        assert abs(state.probability(0)) < 1e-10
        assert abs(state.probability(1) - 1.0) < 1e-10

    def test_plus_state(self):
        state = QuantumState.plus()
        assert abs(state.probability(0) - 0.5) < 1e-10
        assert abs(state.probability(1) - 0.5) < 1e-10

    def test_bell_state(self):
        state = QuantumState.bell()
        assert abs(state.probability(0) - 0.5) < 1e-10  # |00>
        assert abs(state.probability(3) - 0.5) < 1e-10  # |11>

    def test_normalization(self):
        state = QuantumState.zero(2)
        total = sum(state.probabilities())
        assert abs(total - 1.0) < 1e-10

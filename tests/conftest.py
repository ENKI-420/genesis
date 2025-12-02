"""Pytest configuration and fixtures."""

import pytest
from typing import Generator


@pytest.fixture
def sample_organism_code() -> str:
    """Sample DNA-Lang code for testing."""
    return """
organism TestCell {
    gene replicate: hadamard }{ cnot
    trait fitness: 0.95
    trait generation: 1
}
"""


@pytest.fixture
def quantum_state():
    """Create a test quantum state."""
    from genesis.core.state import QuantumState
    return QuantumState.zero(2)


@pytest.fixture
def ccce_metric():
    """Create a CCCE metric instance."""
    from genesis.metrics.ccce import CCCEMetric
    return CCCEMetric()

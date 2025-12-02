"""
Bell State Creation Example

Demonstrates creating and measuring Bell states using the GENESIS quantum core.
"""

from genesis.core.state import QuantumState
from genesis.core.gates import H, CNOT
from genesis.core.circuit import QuantumCircuit


def create_bell_state():
    """Create a Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2"""
    # Method 1: Direct state creation
    bell = QuantumState.bell()
    print("Bell state |Φ+⟩:")
    print(f"  Amplitudes: {bell.amplitudes}")
    print(f"  Probabilities: {bell.probabilities()}")
    
    # Method 2: Using circuit
    circuit = QuantumCircuit(2)
    circuit.h(0)      # Hadamard on qubit 0
    circuit.cnot(0, 1)  # CNOT with control=0, target=1
    
    state = circuit.execute()
    print("\nCircuit-created Bell state:")
    print(f"  Amplitudes: {state.amplitudes}")
    
    # Measure correlations
    print("\nMeasurement outcomes (100 shots):")
    outcomes = {"00": 0, "01": 0, "10": 0, "11": 0}
    for _ in range(100):
        result = state.measure()
        key = format(result, '02b')
        outcomes[key] += 1
    
    for key, count in outcomes.items():
        print(f"  |{key}⟩: {count}%")


if __name__ == "__main__":
    create_bell_state()

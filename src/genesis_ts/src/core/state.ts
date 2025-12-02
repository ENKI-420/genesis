/**
 * Quantum State Implementation
 *
 * Implements quantum state vectors with zero external dependencies.
 */

import { Complex, complex } from './complex';

export class QuantumState {
  readonly amplitudes: Complex[];
  readonly numQubits: number;

  constructor(amplitudes: Complex[]) {
    const n = amplitudes.length;
    if (n === 0 || (n & (n - 1)) !== 0) {
      throw new Error('State dimension must be a power of 2');
    }
    this.amplitudes = amplitudes;
    this.numQubits = Math.log2(n);
  }

  /**
   * Create the |0⟩ state.
   */
  static zero(numQubits: number = 1): QuantumState {
    const dim = 1 << numQubits;
    const amplitudes = new Array(dim).fill(null).map((_, i) =>
      i === 0 ? complex(1, 0) : complex(0, 0)
    );
    return new QuantumState(amplitudes);
  }

  /**
   * Create the |1⟩ state.
   */
  static one(numQubits: number = 1): QuantumState {
    const dim = 1 << numQubits;
    const amplitudes = new Array(dim).fill(null).map((_, i) =>
      i === dim - 1 ? complex(1, 0) : complex(0, 0)
    );
    return new QuantumState(amplitudes);
  }

  /**
   * Create a computational basis state.
   */
  static basis(index: number, numQubits: number): QuantumState {
    const dim = 1 << numQubits;
    if (index < 0 || index >= dim) {
      throw new Error(`Index ${index} out of range for ${numQubits} qubits`);
    }
    const amplitudes = new Array(dim).fill(null).map((_, i) =>
      i === index ? complex(1, 0) : complex(0, 0)
    );
    return new QuantumState(amplitudes);
  }

  /**
   * Create the |+⟩ state.
   */
  static plus(): QuantumState {
    const amp = 1 / Math.SQRT2;
    return new QuantumState([complex(amp), complex(amp)]);
  }

  /**
   * Create the |-⟩ state.
   */
  static minus(): QuantumState {
    const amp = 1 / Math.SQRT2;
    return new QuantumState([complex(amp), complex(-amp)]);
  }

  /**
   * Get the dimension of the state space.
   */
  get dimension(): number {
    return this.amplitudes.length;
  }

  /**
   * Get the amplitude at an index.
   */
  amplitude(index: number): Complex {
    return this.amplitudes[index];
  }

  /**
   * Get the probability of measuring a basis state.
   */
  probability(index: number): number {
    return this.amplitudes[index].magnitudeSquared();
  }

  /**
   * Get all probabilities.
   */
  probabilities(): number[] {
    return this.amplitudes.map(a => a.magnitudeSquared());
  }

  /**
   * Compute the inner product with another state.
   */
  innerProduct(other: QuantumState): Complex {
    if (this.dimension !== other.dimension) {
      throw new Error('States must have same dimension');
    }
    let result = complex(0, 0);
    for (let i = 0; i < this.dimension; i++) {
      result = result.add(this.amplitudes[i].conjugate().mul(other.amplitudes[i]));
    }
    return result;
  }

  /**
   * Compute the fidelity with another state.
   */
  fidelity(other: QuantumState): number {
    const inner = this.innerProduct(other);
    return inner.magnitudeSquared();
  }

  /**
   * Normalize the state.
   */
  normalize(): QuantumState {
    let norm = 0;
    for (const a of this.amplitudes) {
      norm += a.magnitudeSquared();
    }
    norm = Math.sqrt(norm);
    if (norm < 1e-10) {
      throw new Error('Cannot normalize zero state');
    }
    const newAmplitudes = this.amplitudes.map(a => a.scale(1 / norm));
    return new QuantumState(newAmplitudes);
  }

  /**
   * Add another state (not normalized).
   */
  add(other: QuantumState): QuantumState {
    if (this.dimension !== other.dimension) {
      throw new Error('States must have same dimension');
    }
    const newAmplitudes = this.amplitudes.map((a, i) => a.add(other.amplitudes[i]));
    return new QuantumState(newAmplitudes);
  }

  /**
   * Scale by a complex factor.
   */
  scale(factor: Complex): QuantumState {
    const newAmplitudes = this.amplitudes.map(a => a.mul(factor));
    return new QuantumState(newAmplitudes);
  }

  /**
   * Tensor product with another state.
   */
  tensor(other: QuantumState): QuantumState {
    const newDim = this.dimension * other.dimension;
    const newAmplitudes: Complex[] = [];
    for (let i = 0; i < this.dimension; i++) {
      for (let j = 0; j < other.dimension; j++) {
        newAmplitudes.push(this.amplitudes[i].mul(other.amplitudes[j]));
      }
    }
    return new QuantumState(newAmplitudes);
  }

  /**
   * Measure in the computational basis (simulated).
   * Returns the measured index and collapsed state.
   */
  measure(): { index: number; state: QuantumState } {
    const probs = this.probabilities();
    let r = Math.random();
    let index = 0;
    for (let i = 0; i < probs.length; i++) {
      r -= probs[i];
      if (r <= 0) {
        index = i;
        break;
      }
    }
    return {
      index,
      state: QuantumState.basis(index, this.numQubits),
    };
  }

  /**
   * String representation.
   */
  toString(): string {
    const terms: string[] = [];
    for (let i = 0; i < this.dimension; i++) {
      const a = this.amplitudes[i];
      if (a.magnitudeSquared() > 1e-10) {
        const basisLabel = i.toString(2).padStart(this.numQubits, '0');
        terms.push(`${a.toString()}|${basisLabel}⟩`);
      }
    }
    return terms.join(' + ') || '0';
  }
}

/**
 * Create a Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2
 */
export function bellState(): QuantumState {
  const amp = 1 / Math.SQRT2;
  return new QuantumState([
    complex(amp, 0),  // |00⟩
    complex(0, 0),    // |01⟩
    complex(0, 0),    // |10⟩
    complex(amp, 0),  // |11⟩
  ]);
}

/**
 * Create a GHZ state for n qubits.
 */
export function ghzState(numQubits: number): QuantumState {
  const dim = 1 << numQubits;
  const amp = 1 / Math.SQRT2;
  const amplitudes = new Array(dim).fill(null).map((_, i) =>
    i === 0 || i === dim - 1 ? complex(amp, 0) : complex(0, 0)
  );
  return new QuantumState(amplitudes);
}

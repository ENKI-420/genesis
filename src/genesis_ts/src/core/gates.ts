/**
 * Quantum Gates Implementation
 *
 * Implements standard quantum gates for the GENESIS platform.
 */

import { Complex, complex } from './complex';
import { QuantumState } from './state';
import { SQRT2_INV, PI } from '../constants';

/**
 * A quantum gate represented as a unitary matrix.
 */
export class Gate {
  readonly name: string;
  readonly matrix: Complex[][];
  readonly numQubits: number;

  constructor(name: string, matrix: Complex[][]) {
    this.name = name;
    this.matrix = matrix;
    const dim = matrix.length;
    if (dim === 0 || (dim & (dim - 1)) !== 0) {
      throw new Error('Gate dimension must be a power of 2');
    }
    this.numQubits = Math.log2(dim);
  }

  /**
   * Apply the gate to a state.
   */
  apply(state: QuantumState): QuantumState {
    if (state.numQubits !== this.numQubits) {
      throw new Error('Gate and state dimensions must match');
    }
    const newAmplitudes: Complex[] = [];
    for (let i = 0; i < this.matrix.length; i++) {
      let sum = complex(0, 0);
      for (let j = 0; j < this.matrix[i].length; j++) {
        sum = sum.add(this.matrix[i][j].mul(state.amplitudes[j]));
      }
      newAmplitudes.push(sum);
    }
    return new QuantumState(newAmplitudes);
  }

  /**
   * Get the adjoint (conjugate transpose) of the gate.
   */
  adjoint(): Gate {
    const dim = this.matrix.length;
    const newMatrix: Complex[][] = [];
    for (let i = 0; i < dim; i++) {
      newMatrix.push([]);
      for (let j = 0; j < dim; j++) {
        newMatrix[i].push(this.matrix[j][i].conjugate());
      }
    }
    return new Gate(`${this.name}†`, newMatrix);
  }

  /**
   * String representation.
   */
  toString(): string {
    return this.name;
  }
}

// Standard single-qubit gates

/** Identity gate */
export const I = new Gate('I', [
  [complex(1, 0), complex(0, 0)],
  [complex(0, 0), complex(1, 0)],
]);

/** Pauli-X gate (NOT) */
export const X = new Gate('X', [
  [complex(0, 0), complex(1, 0)],
  [complex(1, 0), complex(0, 0)],
]);

/** Pauli-Y gate */
export const Y = new Gate('Y', [
  [complex(0, 0), complex(0, -1)],
  [complex(0, 1), complex(0, 0)],
]);

/** Pauli-Z gate */
export const Z = new Gate('Z', [
  [complex(1, 0), complex(0, 0)],
  [complex(0, 0), complex(-1, 0)],
]);

/** Hadamard gate */
export const H = new Gate('H', [
  [complex(SQRT2_INV, 0), complex(SQRT2_INV, 0)],
  [complex(SQRT2_INV, 0), complex(-SQRT2_INV, 0)],
]);

/** S gate (phase gate) */
export const S = new Gate('S', [
  [complex(1, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 1)],
]);

/** T gate (π/8 gate) */
export const T = new Gate('T', [
  [complex(1, 0), complex(0, 0)],
  [complex(0, 0), Complex.exp(PI / 4)],
]);

/**
 * Create a rotation gate around the X axis.
 */
export function RX(theta: number): Gate {
  const c = Math.cos(theta / 2);
  const s = Math.sin(theta / 2);
  return new Gate(`RX(${theta})`, [
    [complex(c, 0), complex(0, -s)],
    [complex(0, -s), complex(c, 0)],
  ]);
}

/**
 * Create a rotation gate around the Y axis.
 */
export function RY(theta: number): Gate {
  const c = Math.cos(theta / 2);
  const s = Math.sin(theta / 2);
  return new Gate(`RY(${theta})`, [
    [complex(c, 0), complex(-s, 0)],
    [complex(s, 0), complex(c, 0)],
  ]);
}

/**
 * Create a rotation gate around the Z axis.
 */
export function RZ(theta: number): Gate {
  return new Gate(`RZ(${theta})`, [
    [Complex.exp(-theta / 2), complex(0, 0)],
    [complex(0, 0), Complex.exp(theta / 2)],
  ]);
}

/**
 * Create a phase gate.
 */
export function Phase(phi: number): Gate {
  return new Gate(`P(${phi})`, [
    [complex(1, 0), complex(0, 0)],
    [complex(0, 0), Complex.exp(phi)],
  ]);
}

// Two-qubit gates

/** CNOT (Controlled-NOT) gate */
export const CNOT = new Gate('CNOT', [
  [complex(1, 0), complex(0, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(1, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 0), complex(0, 0), complex(1, 0)],
  [complex(0, 0), complex(0, 0), complex(1, 0), complex(0, 0)],
]);

/** CZ (Controlled-Z) gate */
export const CZ = new Gate('CZ', [
  [complex(1, 0), complex(0, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(1, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 0), complex(1, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 0), complex(0, 0), complex(-1, 0)],
]);

/** SWAP gate */
export const SWAP = new Gate('SWAP', [
  [complex(1, 0), complex(0, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 0), complex(1, 0), complex(0, 0)],
  [complex(0, 0), complex(1, 0), complex(0, 0), complex(0, 0)],
  [complex(0, 0), complex(0, 0), complex(0, 0), complex(1, 0)],
]);

/**
 * Apply a single-qubit gate to a specific qubit in a multi-qubit state.
 */
export function applySingleQubitGate(
  state: QuantumState,
  gate: Gate,
  target: number
): QuantumState {
  if (gate.numQubits !== 1) {
    throw new Error('Expected a single-qubit gate');
  }
  if (target < 0 || target >= state.numQubits) {
    throw new Error('Target qubit out of range');
  }

  const dim = state.dimension;
  const newAmplitudes: Complex[] = new Array(dim);

  for (let i = 0; i < dim; i++) {
    newAmplitudes[i] = complex(0, 0);
  }

  // Apply gate to target qubit
  const targetMask = 1 << (state.numQubits - 1 - target);

  for (let i = 0; i < dim; i++) {
    const bit = (i & targetMask) ? 1 : 0;
    for (let j = 0; j < 2; j++) {
      const fromBit = j;
      const fromIndex = bit === fromBit ? i : i ^ targetMask;
      newAmplitudes[i] = newAmplitudes[i].add(
        gate.matrix[bit][fromBit].mul(state.amplitudes[fromIndex])
      );
    }
  }

  return new QuantumState(newAmplitudes);
}

/**
 * Apply a controlled gate.
 */
export function applyControlledGate(
  state: QuantumState,
  gate: Gate,
  control: number,
  target: number
): QuantumState {
  if (gate.numQubits !== 1) {
    throw new Error('Expected a single-qubit gate');
  }
  if (control === target) {
    throw new Error('Control and target must be different');
  }
  if (control < 0 || control >= state.numQubits ||
      target < 0 || target >= state.numQubits) {
    throw new Error('Qubit index out of range');
  }

  const dim = state.dimension;
  const newAmplitudes: Complex[] = [...state.amplitudes];

  const controlMask = 1 << (state.numQubits - 1 - control);
  const targetMask = 1 << (state.numQubits - 1 - target);

  // Only apply gate when control qubit is |1⟩
  for (let i = 0; i < dim; i++) {
    if (i & controlMask) {
      // Control is |1⟩, apply gate to target
      const targetBit = (i & targetMask) ? 1 : 0;
      if (targetBit === 0) {
        const i0 = i;
        const i1 = i | targetMask;
        const a0 = state.amplitudes[i0];
        const a1 = state.amplitudes[i1];
        newAmplitudes[i0] = gate.matrix[0][0].mul(a0).add(gate.matrix[0][1].mul(a1));
        newAmplitudes[i1] = gate.matrix[1][0].mul(a0).add(gate.matrix[1][1].mul(a1));
      }
    }
  }

  return new QuantumState(newAmplitudes);
}

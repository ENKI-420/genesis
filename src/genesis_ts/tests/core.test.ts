/**
 * GENESIS TypeScript Tests
 */

import { Complex, complex } from '../src/core/complex';
import { QuantumState, bellState } from '../src/core/state';
import { H, X, CNOT, applySingleQubitGate } from '../src/core/gates';
import { LAMBDA_PHI, PSI_STAR, THETA_LOCK, CHI_PC } from '../src/constants';
import { tokenize, TokenType } from '../src/dna-lang/lexer';
import { parse } from '../src/dna-lang/parser';
import { compile } from '../src/dna-lang/compiler';

describe('Complex Numbers', () => {
  test('should create complex numbers', () => {
    const c = new Complex(3, 4);
    expect(c.real).toBe(3);
    expect(c.imag).toBe(4);
  });

  test('should compute magnitude', () => {
    const c = new Complex(3, 4);
    expect(c.magnitude()).toBe(5);
  });

  test('should add complex numbers', () => {
    const a = new Complex(1, 2);
    const b = new Complex(3, 4);
    const sum = a.add(b);
    expect(sum.real).toBe(4);
    expect(sum.imag).toBe(6);
  });

  test('should multiply complex numbers', () => {
    const a = new Complex(1, 2);
    const b = new Complex(3, 4);
    const prod = a.mul(b);
    expect(prod.real).toBe(-5);
    expect(prod.imag).toBe(10);
  });

  test('should compute conjugate', () => {
    const c = new Complex(3, 4);
    const conj = c.conjugate();
    expect(conj.real).toBe(3);
    expect(conj.imag).toBe(-4);
  });
});

describe('Quantum State', () => {
  test('should create zero state', () => {
    const state = QuantumState.zero();
    expect(state.probability(0)).toBeCloseTo(1);
    expect(state.probability(1)).toBeCloseTo(0);
  });

  test('should create plus state', () => {
    const state = QuantumState.plus();
    expect(state.probability(0)).toBeCloseTo(0.5);
    expect(state.probability(1)).toBeCloseTo(0.5);
  });

  test('should create Bell state', () => {
    const state = bellState();
    expect(state.probability(0)).toBeCloseTo(0.5); // |00⟩
    expect(state.probability(1)).toBeCloseTo(0);   // |01⟩
    expect(state.probability(2)).toBeCloseTo(0);   // |10⟩
    expect(state.probability(3)).toBeCloseTo(0.5); // |11⟩
  });

  test('should compute fidelity', () => {
    const state = QuantumState.zero();
    expect(state.fidelity(state)).toBeCloseTo(1);
  });
});

describe('Quantum Gates', () => {
  test('X gate should flip state', () => {
    const zero = QuantumState.zero();
    const one = X.apply(zero);
    expect(one.probability(0)).toBeCloseTo(0);
    expect(one.probability(1)).toBeCloseTo(1);
  });

  test('H gate should create superposition', () => {
    const zero = QuantumState.zero();
    const plus = H.apply(zero);
    expect(plus.probability(0)).toBeCloseTo(0.5);
    expect(plus.probability(1)).toBeCloseTo(0.5);
  });

  test('H^2 = I', () => {
    const zero = QuantumState.zero();
    const result = H.apply(H.apply(zero));
    expect(result.probability(0)).toBeCloseTo(1);
    expect(result.probability(1)).toBeCloseTo(0);
  });
});

describe('Constants', () => {
  test('should have correct values', () => {
    expect(LAMBDA_PHI).toBeCloseTo(2.176435e-8);
    expect(PSI_STAR).toBeCloseTo(0.973);
    expect(THETA_LOCK).toBeCloseTo(51.843);
    expect(CHI_PC).toBeCloseTo(0.869);
  });
});

describe('DNA-Lang Lexer', () => {
  test('should tokenize simple organism', () => {
    const source = 'organism Test {}';
    const tokens = tokenize(source);
    expect(tokens[0].type).toBe(TokenType.ORGANISM);
    expect(tokens[1].type).toBe(TokenType.IDENTIFIER);
    expect(tokens[1].value).toBe('Test');
    expect(tokens[2].type).toBe(TokenType.LBRACE);
    expect(tokens[3].type).toBe(TokenType.RBRACE);
  });

  test('should tokenize bind operator', () => {
    const source = 'a }{ b';
    const tokens = tokenize(source);
    expect(tokens.some(t => t.type === TokenType.BIND)).toBe(true);
  });
});

describe('DNA-Lang Parser', () => {
  test('should parse simple organism', () => {
    const source = 'organism Test {}';
    const tokens = tokenize(source);
    const ast = parse(tokens);
    expect(ast.type).toBe('Program');
    expect(ast.organisms.length).toBe(1);
    expect(ast.organisms[0].name).toBe('Test');
  });

  test('should parse organism with gene', () => {
    const source = `
      organism Cell {
        gene replicate: 42
      }
    `;
    const tokens = tokenize(source);
    const ast = parse(tokens);
    expect(ast.organisms[0].genes.length).toBe(1);
    expect(ast.organisms[0].genes[0].name).toBe('replicate');
  });
});

describe('DNA-Lang Compiler', () => {
  test('should compile simple organism', () => {
    const source = `
      organism Cell {
        gene replicate: 42
        trait fitness: 0.95
      }
    `;
    const organisms = compile(source);
    expect(organisms.length).toBe(1);
    expect(organisms[0].name).toBe('Cell');
    expect(organisms[0].genes.has('replicate')).toBe(true);
    expect(organisms[0].traits.get('fitness')).toBe(0.95);
  });
});

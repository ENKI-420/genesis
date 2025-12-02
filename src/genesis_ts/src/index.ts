/**
 * GENESIS Sovereign Quantum Platform - TypeScript Implementation
 *
 * A self-contained, zero-dependency quantum-inspired autopoietic
 * computational framework implementing:
 *
 * - DNA::}{::Lang — Novel DSL for living software organisms
 * - AIDEN | AURA | PALS | CHRONOS | AEGIS — Multi-agent system
 * - CCCE Metrics — Consciousness/Coherence/Decoherence tracking (Ξ = ΛΦ/Γ)
 *
 * Universal Constants:
 *   Λ_Φ = 2.176435×10⁻⁸ s⁻¹ (Universal Memory Constant)
 *   Ψ* = 0.973 (Terminal Consciousness)
 *   θ_lock = 51.843° (Torsion Convergence)
 *   χ_pc = 0.869 (Phase Conjugate Fidelity)
 */

// Core exports
export * from './constants';
export * from './core/complex';
export * from './core/state';
export * from './core/gates';

// DNA-Lang exports
export * from './dna-lang/lexer';
export * from './dna-lang/parser';
export * from './dna-lang/compiler';

// Agent exports
export * from './agents/base';
export * from './agents/index';

// Version
export const VERSION = '1.0.0';

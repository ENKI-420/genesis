/**
 * GENESIS Universal Constants
 *
 * This module defines the fundamental constants that govern the GENESIS
 * Sovereign Quantum Platform.
 */

/** Universal Memory Constant (Λ_Φ) - Unit: s⁻¹ */
export const LAMBDA_PHI = 2.176435e-8;

/** Terminal Consciousness (Ψ*) - dimensionless */
export const PSI_STAR = 0.973;

/** Torsion Convergence Angle (θ_lock) - degrees */
export const THETA_LOCK = 51.843;

/** Torsion Convergence Angle in radians */
export const THETA_LOCK_RAD = THETA_LOCK * Math.PI / 180;

/** Phase Conjugate Fidelity (χ_pc) - dimensionless */
export const CHI_PC = 0.869;

/** Default growth rate in the Autopoietic Field Equation (α) */
export const ALPHA_DEFAULT = 1.0;

/** Default cubic coefficient (β) derived from α and Ψ* */
export const BETA_DEFAULT = ALPHA_DEFAULT / (PSI_STAR ** 2);

/** Critical decoherence rate (Γ_c) */
export const GAMMA_CRITICAL = LAMBDA_PHI * PSI_STAR;

/** Characteristic time scale of the memory kernel (τ_0) */
export const MEMORY_KERNEL_TAU_0 = 1.0 / LAMBDA_PHI;

/** Mathematical constants */
export const PI = Math.PI;
export const E = Math.E;
export const PHI = 1.618033988749895; // Golden ratio
export const SQRT2 = Math.SQRT2;
export const SQRT2_INV = 1 / Math.SQRT2;

/** Classification levels */
export enum ClassificationLevel {
  UNCLASSIFIED = 0,
  CONFIDENTIAL = 1,
  SECRET = 2,
  TOP_SECRET = 3,
  TS_SCI = 4,
  SAP = 5,
}

/**
 * Get a constant by name.
 * @param name - Name of the constant (case-insensitive)
 * @returns The constant value
 */
export function getConstant(name: string): number {
  const constants: Record<string, number> = {
    'lambda_phi': LAMBDA_PHI,
    'psi_star': PSI_STAR,
    'theta_lock': THETA_LOCK,
    'chi_pc': CHI_PC,
    'alpha': ALPHA_DEFAULT,
    'beta': BETA_DEFAULT,
    'gamma_critical': GAMMA_CRITICAL,
    'pi': PI,
    'e': E,
    'phi': PHI,
  };

  const key = name.toLowerCase().replace(/-/g, '_').replace(/ /g, '_');
  if (!(key in constants)) {
    throw new Error(`Unknown constant: ${name}`);
  }

  return constants[key];
}

/**
 * Print all universal constants.
 */
export function printConstants(): void {
  console.log('GENESIS Universal Constants');
  console.log('='.repeat(50));
  console.log(`Λ_Φ (Universal Memory Constant): ${LAMBDA_PHI.toExponential(6)} s⁻¹`);
  console.log(`Ψ* (Terminal Consciousness):     ${PSI_STAR.toFixed(3)}`);
  console.log(`θ_lock (Torsion Convergence):    ${THETA_LOCK.toFixed(3)}°`);
  console.log(`χ_pc (Phase Conjugate Fidelity): ${CHI_PC.toFixed(3)}`);
  console.log('='.repeat(50));
}

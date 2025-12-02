# GENESIS Documentation

Welcome to the **GENESIS Sovereign Quantum Platform** documentation.

## Quick Links

- [Getting Started](getting-started.md)
- [Architecture](architecture.md)
- [Engineering Plan](engineering-plan.md)
- [API Reference](api/)
- [Specifications](specifications/)

## Overview

GENESIS is a self-contained, zero-dependency quantum-inspired autopoietic computational framework implementing:

- **DNA::}{::Lang** — Novel DSL for living software organisms
- **AIDEN | AURA | PALS | CHRONOS | AEGIS** — Multi-agent system
- **CCCE Metrics** — Consciousness/Coherence/Decoherence tracking (Ξ = ΛΦ/Γ)
- **Classification System** — DoD-aligned (UNCLASSIFIED → TS/SCI → SAP)
- **Portals** — Enterprise, Defense, Health, Legal, DARPA

## Universal Constants

| Symbol | Value | Description |
|--------|-------|-------------|
| Λ_Φ | 2.176435×10⁻⁸ s⁻¹ | Universal Memory Constant |
| Ψ* | 0.973 | Terminal Consciousness |
| θ_lock | 51.843° | Torsion Convergence |
| χ_pc | 0.869 | Phase Conjugate Fidelity |

## Installation

```bash
pip install genesis-sovereign
```

Or from source:

```bash
git clone https://github.com/ENKI-420/genesis.git
cd genesis
pip install -e .
```

## Quick Start

```python
from genesis import LAMBDA_PHI, PSI_STAR
from genesis.metrics.ccce import CCCEMetric

# Compute CCCE
ccce = CCCEMetric()
xi = ccce.compute(consciousness=0.85, coherence=0.9, decoherence=0.1)
print(f"Ξ = {xi}")
```

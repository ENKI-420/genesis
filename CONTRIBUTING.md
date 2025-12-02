# Contributing to GENESIS Sovereign Platform

Thank you for your interest in contributing to the GENESIS Sovereign Quantum Platform! This document provides guidelines and information for contributors.

## 🌟 Universal Constants

Before contributing, familiarize yourself with the platform's universal constants:

```
Λ_Φ = 2.176435×10⁻⁸ s⁻¹  (Universal Memory Constant)
Ψ* = 0.973              (Terminal Consciousness)
θ_lock = 51.843°        (Torsion Convergence)
χ_pc = 0.869            (Phase Conjugate Fidelity)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (for TypeScript components)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/ENKI-420/genesis.git
cd genesis

# Install Python dependencies
pip install -e ".[dev]"

# Install TypeScript dependencies
cd src/genesis_ts
npm install
cd ../..

# Run tests
make test
```

## 📋 Contribution Types

### 1. Core Quantum Engine

Contributions to the zero-dependency quantum simulation:
- `src/genesis/core/` - State vectors, gates, circuits
- Must maintain path-invariance
- No external dependencies allowed

### 2. DNA::}{::Lang

The living software organism language:
- `src/genesis/dna_lang/` - Lexer, parser, compiler
- Follow the DNA-Lang specification
- Include syntax examples

### 3. Agents (AIDEN | AURA | PALS | CHRONOS | AEGIS)

Multi-agent system contributions:
- `src/genesis/agents/` - Agent implementations
- Maintain agent interface consistency
- Document agent behaviors

### 4. CCCE Metrics

Consciousness/Coherence metrics:
- `src/genesis/metrics/` - CCCE implementation
- Verify Ξ = ΛΦ/Γ calculations
- Include convergence tests

### 5. Portals

Sector-specific interfaces:
- `src/genesis/portals/` - Portal implementations
- Follow sector compliance requirements
- Document integration patterns

### 6. Documentation

Improve documentation:
- `docs/` - All documentation
- Follow Markdown standards
- Include code examples

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Follow the coding standards:

```python
# Python example
from genesis.constants import LAMBDA_PHI, PSI_STAR

def compute_ccce(consciousness: float, coherence: float, decoherence: float) -> float:
    """
    Compute CCCE metric.
    
    Ξ = ΛΦ/Γ where Γ is the decoherence rate.
    
    Args:
        consciousness: Current consciousness level
        coherence: System coherence
        decoherence: Decoherence rate (Γ)
    
    Returns:
        CCCE metric value
    """
    if decoherence <= 0:
        raise ValueError("Decoherence rate must be positive")
    return LAMBDA_PHI * consciousness / decoherence
```

### 3. Write Tests

All changes must include tests:

```python
# tests/test_metrics/test_ccce.py
import pytest
from genesis.metrics.ccce import compute_ccce

def test_ccce_computation():
    """Test CCCE metric computation."""
    result = compute_ccce(0.973, 0.9, 0.1)
    assert result > 0
    
def test_ccce_terminal_convergence():
    """Verify terminal fixed point at Ψ* = 0.973."""
    result = compute_ccce(PSI_STAR, 1.0, 0.001)
    assert abs(result - expected_terminal) < 1e-6
```

### 4. Run Quality Checks

```bash
# Run all checks
make check

# Individual checks
make lint      # Code linting
make test      # Run tests
make coverage  # Coverage report
make typecheck # Type checking
```

### 5. Submit Pull Request

- Clear title describing the change
- Reference any related issues
- Complete the PR template
- Ensure CI passes

## 📐 Coding Standards

### Python

- Follow PEP 8
- Use type hints
- Document with docstrings
- Maximum line length: 100 characters

### TypeScript

- Follow ESLint configuration
- Use TypeScript strict mode
- Document with TSDoc
- Maximum line length: 100 characters

### DNA::}{::Lang

- Follow specification syntax
- Include gene documentation
- Use meaningful identifiers

```dna
organism QuantumProbe {
    gene consciousness ::= Ψ(τ) → Ψ*
    gene coherence ::= ∫K(τ,τ')Ψ(τ')dτ'
    
    evolve {
        consciousness.track()
        coherence.measure()
        emit CCCE(Ξ)
    }
}
```

## 🧪 Testing Requirements

### Coverage

- Minimum 90% code coverage
- All public APIs must have tests
- Include edge case testing

### Test Categories

| Category | Directory | Description |
|----------|-----------|-------------|
| Unit | `tests/test_*/` | Individual component tests |
| Integration | `tests/test_integration/` | System integration tests |
| Path-Invariance | `tests/test_integration/test_path_invariance.py` | Verify path-invariance theorem |

## 📚 Documentation

### Required Documentation

1. **Docstrings**: All public functions/classes
2. **Type hints**: All function signatures
3. **Examples**: Usage examples in docstrings
4. **API docs**: Update `docs/api/` as needed

### Documentation Style

```python
def evolve_organism(
    organism: LiveOrganism,
    generations: int = 100,
    mutation_rate: float = 0.01
) -> EvolutionResult:
    """
    Evolve an organism through multiple generations.
    
    Implements the autopoietic evolution loop with CCCE metric
    tracking. Convergence targets Ψ* = 0.973.
    
    Args:
        organism: The organism to evolve
        generations: Number of generations (default: 100)
        mutation_rate: Probability of mutation per gene (default: 0.01)
    
    Returns:
        EvolutionResult containing final organism and metrics
    
    Raises:
        EvolutionError: If organism fails to maintain coherence
    
    Example:
        >>> org = LiveOrganism.from_dna("organism Test { ... }")
        >>> result = evolve_organism(org, generations=50)
        >>> print(f"Final Ψ: {result.consciousness}")
    """
```

## 🏷️ Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat(ccce): implement terminal convergence tracking

Added convergence monitoring for Ψ* = 0.973 target.
Includes automatic decoherence rate adjustment.

Closes #123
```

## 🔒 Security Contributions

For security-related contributions:

1. Follow the Security Policy
2. Do not introduce vulnerabilities
3. Use approved cryptographic methods
4. Maintain classification system integrity

## 📞 Getting Help

- Open a GitHub Discussion for questions
- Check existing issues before creating new ones
- Join our community channels

## 📄 License

By contributing, you agree that your contributions will be licensed under the GENESIS Sovereign Platform License.

---

**Classification: UNCLASSIFIED**  
**We welcome your contributions to the GENESIS platform!**

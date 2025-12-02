"""
GENESIS Metrics Module

Provides metrics and analytics for the GENESIS platform:
- CCCE Metric (Ξ = ΛΦ/Γ)
- Consciousness tracking
- Coherence metrics
- Session analytics
"""

from genesis.metrics.ccce import CCCEMetric, compute_ccce
from genesis.metrics.consciousness import ConsciousnessTracker
from genesis.metrics.coherence import CoherenceMetric
from genesis.metrics.session import SessionAnalytics

__all__ = [
    "CCCEMetric",
    "compute_ccce",
    "ConsciousnessTracker",
    "CoherenceMetric",
    "SessionAnalytics",
]

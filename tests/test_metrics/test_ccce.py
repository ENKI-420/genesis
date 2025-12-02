"""Tests for CCCE metric."""

import pytest
from genesis.metrics.ccce import CCCEMetric


class TestCCCE:
    def test_compute(self):
        ccce = CCCEMetric()
        xi = ccce.compute(consciousness=0.85, coherence=0.9, decoherence=0.1)
        expected = (0.85 * 0.9) / 0.1
        assert abs(xi - expected) < 1e-10

    def test_zero_decoherence(self):
        ccce = CCCEMetric()
        xi = ccce.compute(consciousness=0.85, coherence=0.9, decoherence=0.0)
        assert xi == float('inf')

    def test_status_optimal(self):
        ccce = CCCEMetric()
        status = ccce.status(10.0)
        assert status == "OPTIMAL"

    def test_status_warning(self):
        ccce = CCCEMetric()
        status = ccce.status(0.3)
        assert status == "WARNING"

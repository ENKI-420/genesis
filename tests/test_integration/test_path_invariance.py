"""Tests for path invariance theorem."""

import pytest
from genesis.constants import PSI_STAR
from genesis.field.afe import AutopoieticFieldEquation


class TestPathInvariance:
    def test_convergence_to_psi_star(self):
        """All initial conditions should converge to Ψ*."""
        afe = AutopoieticFieldEquation()
        
        for psi_0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
            trajectory = afe.evolve_rk4(psi_0, 50.0, dt=0.01)
            final_psi = trajectory[-1][1]
            assert abs(final_psi - PSI_STAR) < 0.01

    def test_fixed_point_stability(self):
        """Ψ* should be a stable fixed point."""
        afe = AutopoieticFieldEquation()
        analysis = afe.stability_analysis()
        
        assert analysis["stable_at_star"] == True
        assert analysis["stable_at_0"] == False

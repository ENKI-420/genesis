"""Tests for core complex number implementation."""

import pytest
from genesis.core.complex import Complex


class TestComplex:
    def test_creation(self):
        c = Complex(3, 4)
        assert c.real == 3
        assert c.imag == 4

    def test_magnitude(self):
        c = Complex(3, 4)
        assert abs(c.magnitude() - 5.0) < 1e-10

    def test_addition(self):
        a = Complex(1, 2)
        b = Complex(3, 4)
        result = a + b
        assert result.real == 4
        assert result.imag == 6

    def test_multiplication(self):
        a = Complex(1, 2)
        b = Complex(3, 4)
        result = a * b
        assert result.real == -5
        assert result.imag == 10

    def test_conjugate(self):
        c = Complex(3, 4)
        conj = c.conjugate()
        assert conj.real == 3
        assert conj.imag == -4

    def test_from_polar(self):
        import math
        c = Complex.from_polar(1, math.pi / 2)
        assert abs(c.real) < 1e-10
        assert abs(c.imag - 1) < 1e-10

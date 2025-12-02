"""
Sovereign Complex Number Implementation

Zero-dependency complex number arithmetic for the GENESIS platform.
This implementation provides all complex number operations needed for
quantum simulation without relying on external libraries.
"""

from __future__ import annotations
from typing import Union
from genesis.constants import PI, E


class Complex:
    """
    Sovereign complex number implementation.
    
    A complex number z = a + bi where a is the real part and b is the
    imaginary part.
    
    This class provides complete complex arithmetic including:
    - Addition, subtraction, multiplication, division
    - Conjugate, modulus, argument
    - Exponential, logarithm, power
    - Trigonometric functions
    
    All operations are implemented without external dependencies.
    
    Attributes:
        real: The real part of the complex number.
        imag: The imaginary part of the complex number.
        
    Example:
        >>> z = Complex(3, 4)
        >>> print(z.modulus())  # 5.0
        >>> print(z.conjugate())  # (3-4j)
    """
    
    __slots__ = ("real", "imag")
    
    def __init__(self, real: float = 0.0, imag: float = 0.0) -> None:
        """
        Initialize a complex number.
        
        Args:
            real: The real part (default 0.0).
            imag: The imaginary part (default 0.0).
        """
        self.real = float(real)
        self.imag = float(imag)
    
    @classmethod
    def from_polar(cls, r: float, theta: float) -> Complex:
        """
        Create a complex number from polar form.
        
        Args:
            r: The modulus (radius).
            theta: The argument (angle in radians).
            
        Returns:
            Complex number z = r * e^(i*theta) = r*(cos(θ) + i*sin(θ)).
        """
        return cls(r * _cos(theta), r * _sin(theta))
    
    @classmethod
    def from_builtin(cls, z: complex) -> Complex:
        """
        Create from Python's built-in complex type.
        
        Args:
            z: A built-in complex number.
            
        Returns:
            Equivalent Complex instance.
        """
        return cls(z.real, z.imag)
    
    def to_builtin(self) -> complex:
        """
        Convert to Python's built-in complex type.
        
        Returns:
            Equivalent built-in complex number.
        """
        return complex(self.real, self.imag)
    
    def conjugate(self) -> Complex:
        """
        Return the complex conjugate.
        
        Returns:
            z* = a - bi for z = a + bi.
        """
        return Complex(self.real, -self.imag)
    
    def modulus(self) -> float:
        """
        Return the modulus (absolute value).
        
        Returns:
            |z| = sqrt(a² + b²).
        """
        return _sqrt(self.real * self.real + self.imag * self.imag)
    
    def modulus_squared(self) -> float:
        """
        Return the squared modulus.
        
        Returns:
            |z|² = a² + b².
        """
        return self.real * self.real + self.imag * self.imag
    
    def argument(self) -> float:
        """
        Return the argument (phase angle).
        
        Returns:
            arg(z) = atan2(b, a) in radians, range (-π, π].
        """
        return _atan2(self.imag, self.real)
    
    def __add__(self, other: Union[Complex, float, int]) -> Complex:
        """Add two complex numbers or a complex and a real."""
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        return Complex(self.real + other, self.imag)
    
    def __radd__(self, other: Union[float, int]) -> Complex:
        """Right addition for real + complex."""
        return Complex(self.real + other, self.imag)
    
    def __sub__(self, other: Union[Complex, float, int]) -> Complex:
        """Subtract two complex numbers or a complex and a real."""
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        return Complex(self.real - other, self.imag)
    
    def __rsub__(self, other: Union[float, int]) -> Complex:
        """Right subtraction for real - complex."""
        return Complex(other - self.real, -self.imag)
    
    def __mul__(self, other: Union[Complex, float, int]) -> Complex:
        """Multiply two complex numbers or a complex and a real."""
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        return Complex(self.real * other, self.imag * other)
    
    def __rmul__(self, other: Union[float, int]) -> Complex:
        """Right multiplication for real * complex."""
        return Complex(self.real * other, self.imag * other)
    
    def __truediv__(self, other: Union[Complex, float, int]) -> Complex:
        """Divide two complex numbers or a complex by a real."""
        if isinstance(other, Complex):
            denom = other.modulus_squared()
            if denom == 0:
                raise ZeroDivisionError("Complex division by zero")
            return Complex(
                (self.real * other.real + self.imag * other.imag) / denom,
                (self.imag * other.real - self.real * other.imag) / denom
            )
        if other == 0:
            raise ZeroDivisionError("Complex division by zero")
        return Complex(self.real / other, self.imag / other)
    
    def __rtruediv__(self, other: Union[float, int]) -> Complex:
        """Right division for real / complex."""
        denom = self.modulus_squared()
        if denom == 0:
            raise ZeroDivisionError("Complex division by zero")
        return Complex(other * self.real / denom, -other * self.imag / denom)
    
    def __neg__(self) -> Complex:
        """Negate the complex number."""
        return Complex(-self.real, -self.imag)
    
    def __pos__(self) -> Complex:
        """Return positive (copy)."""
        return Complex(self.real, self.imag)
    
    def __abs__(self) -> float:
        """Return the modulus."""
        return self.modulus()
    
    def __pow__(self, n: Union[int, float, Complex]) -> Complex:
        """Raise to a power."""
        if isinstance(n, int) and n >= 0:
            # Fast path for non-negative integer powers
            if n == 0:
                return Complex(1.0, 0.0)
            if n == 1:
                return Complex(self.real, self.imag)
            result = Complex(1.0, 0.0)
            base = Complex(self.real, self.imag)
            while n > 0:
                if n & 1:
                    result = result * base
                base = base * base
                n >>= 1
            return result
        
        # General case: z^w = exp(w * ln(z))
        if isinstance(n, (int, float)):
            n = Complex(float(n), 0.0)
        return (n * self.ln()).exp()
    
    def exp(self) -> Complex:
        """
        Compute the exponential e^z.
        
        Returns:
            e^z = e^a * (cos(b) + i*sin(b)) for z = a + bi.
        """
        exp_real = _exp(self.real)
        return Complex(exp_real * _cos(self.imag), exp_real * _sin(self.imag))
    
    def ln(self) -> Complex:
        """
        Compute the natural logarithm.
        
        Returns:
            ln(z) = ln|z| + i*arg(z).
        """
        return Complex(_ln(self.modulus()), self.argument())
    
    def sqrt(self) -> Complex:
        """
        Compute the principal square root.
        
        Returns:
            Principal square root of z.
        """
        r = self.modulus()
        if r == 0:
            return Complex(0.0, 0.0)
        
        # Use the formula that avoids cancellation
        if self.real >= 0:
            t = _sqrt((r + self.real) / 2)
            return Complex(t, self.imag / (2 * t) if t != 0 else 0)
        else:
            t = _sqrt((r - self.real) / 2)
            if self.imag >= 0:
                return Complex(abs(self.imag) / (2 * t) if t != 0 else 0, t)
            else:
                return Complex(abs(self.imag) / (2 * t) if t != 0 else 0, -t)
    
    def sin(self) -> Complex:
        """Compute complex sine."""
        return Complex(
            _sin(self.real) * _cosh(self.imag),
            _cos(self.real) * _sinh(self.imag)
        )
    
    def cos(self) -> Complex:
        """Compute complex cosine."""
        return Complex(
            _cos(self.real) * _cosh(self.imag),
            -_sin(self.real) * _sinh(self.imag)
        )
    
    def __eq__(self, other: object) -> bool:
        """Test equality with tolerance for floating point."""
        if isinstance(other, Complex):
            return (
                abs(self.real - other.real) < 1e-10 and
                abs(self.imag - other.imag) < 1e-10
            )
        if isinstance(other, (int, float)):
            return abs(self.real - other) < 1e-10 and abs(self.imag) < 1e-10
        return NotImplemented
    
    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash((round(self.real, 10), round(self.imag, 10)))
    
    def __repr__(self) -> str:
        """Return string representation."""
        if self.imag >= 0:
            return f"Complex({self.real}, {self.imag})"
        return f"Complex({self.real}, {self.imag})"
    
    def __str__(self) -> str:
        """Return human-readable string."""
        if self.imag == 0:
            return f"{self.real}"
        if self.real == 0:
            return f"{self.imag}j"
        if self.imag > 0:
            return f"({self.real}+{self.imag}j)"
        return f"({self.real}{self.imag}j)"
    
    def __bool__(self) -> bool:
        """Return True if not zero."""
        return self.real != 0 or self.imag != 0
    
    def is_real(self) -> bool:
        """Check if the number is purely real."""
        return abs(self.imag) < 1e-10
    
    def is_imaginary(self) -> bool:
        """Check if the number is purely imaginary."""
        return abs(self.real) < 1e-10
    
    def is_zero(self) -> bool:
        """Check if the number is zero."""
        return abs(self.real) < 1e-10 and abs(self.imag) < 1e-10


# =============================================================================
# ZERO-DEPENDENCY MATH FUNCTIONS
# =============================================================================

def _sqrt(x: float) -> float:
    """Compute square root using Newton's method."""
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number")
    if x == 0:
        return 0.0
    
    # Initial guess
    guess = x / 2
    if guess == 0:
        guess = 1.0
    
    # Newton-Raphson iteration
    for _ in range(50):
        new_guess = 0.5 * (guess + x / guess)
        if abs(new_guess - guess) < 1e-15 * abs(guess):
            return new_guess
        guess = new_guess
    
    return guess


def _exp(x: float) -> float:
    """Compute exponential using Taylor series."""
    if x > 700:
        return float('inf')
    if x < -700:
        return 0.0
    
    # Range reduction: e^x = e^k * e^r where x = k + r, |r| < 0.5
    k = int(x + 0.5) if x > 0 else int(x - 0.5)
    r = x - k
    
    # Taylor series for e^r
    result = 1.0
    term = 1.0
    for n in range(1, 50):
        term *= r / n
        result += term
        if abs(term) < 1e-15:
            break
    
    # Multiply by e^k
    if k > 0:
        e_power = E
        for _ in range(1, k):
            e_power *= E
        result *= e_power
    elif k < 0:
        e_power = E
        for _ in range(1, -k):
            e_power *= E
        result /= e_power
    
    return result


def _ln(x: float) -> float:
    """Compute natural logarithm using Newton's method."""
    if x <= 0:
        raise ValueError("Cannot compute ln of non-positive number")
    
    # Range reduction: ln(x) = ln(m * 2^e) = ln(m) + e*ln(2)
    # where 1 <= m < 2
    ln2 = 0.6931471805599453
    
    e = 0
    m = x
    while m >= 2:
        m /= 2
        e += 1
    while m < 1:
        m *= 2
        e -= 1
    
    # Now compute ln(m) for 1 <= m < 2 using series
    # ln(1+y) = y - y²/2 + y³/3 - ... for |y| < 1
    y = m - 1
    result = 0.0
    term = y
    for n in range(1, 100):
        result += term / n
        term *= -y
        if abs(term / n) < 1e-15:
            break
    
    return result + e * ln2


def _sin(x: float) -> float:
    """Compute sine using Taylor series."""
    # Reduce to [-π, π]
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    elif x < -PI:
        x += 2 * PI
    
    # Taylor series: sin(x) = x - x³/3! + x⁵/5! - ...
    result = 0.0
    term = x
    x2 = x * x
    for n in range(25):
        result += term
        term *= -x2 / ((2 * n + 2) * (2 * n + 3))
        if abs(term) < 1e-15:
            break
    
    return result


def _cos(x: float) -> float:
    """Compute cosine using Taylor series."""
    # Reduce to [-π, π]
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    elif x < -PI:
        x += 2 * PI
    
    # Taylor series: cos(x) = 1 - x²/2! + x⁴/4! - ...
    result = 0.0
    term = 1.0
    x2 = x * x
    for n in range(25):
        result += term
        term *= -x2 / ((2 * n + 1) * (2 * n + 2))
        if abs(term) < 1e-15:
            break
    
    return result


def _atan2(y: float, x: float) -> float:
    """Compute atan2(y, x)."""
    if x == 0:
        if y > 0:
            return PI / 2
        elif y < 0:
            return -PI / 2
        else:
            return 0.0
    
    result = _atan(y / x)
    
    if x < 0:
        if y >= 0:
            result += PI
        else:
            result -= PI
    
    return result


def _atan(x: float) -> float:
    """Compute arctangent using Taylor series."""
    # For |x| > 1, use atan(x) = π/2 - atan(1/x)
    if abs(x) > 1:
        if x > 0:
            return PI / 2 - _atan(1 / x)
        else:
            return -PI / 2 - _atan(1 / x)
    
    # Taylor series: atan(x) = x - x³/3 + x⁵/5 - ...
    result = 0.0
    term = x
    x2 = x * x
    for n in range(100):
        result += term / (2 * n + 1)
        term *= -x2
        if abs(term / (2 * n + 3)) < 1e-15:
            break
    
    return result


def _sinh(x: float) -> float:
    """Compute hyperbolic sine."""
    if abs(x) > 700:
        return float('inf') if x > 0 else float('-inf')
    ex = _exp(x)
    return (ex - 1 / ex) / 2


def _cosh(x: float) -> float:
    """Compute hyperbolic cosine."""
    if abs(x) > 700:
        return float('inf')
    ex = _exp(x)
    return (ex + 1 / ex) / 2


# Common complex constants
ZERO = Complex(0.0, 0.0)
ONE = Complex(1.0, 0.0)
I = Complex(0.0, 1.0)

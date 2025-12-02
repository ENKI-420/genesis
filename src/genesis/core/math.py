"""
Zero-Dependency Math Module

Provides mathematical functions without any external dependencies.
This module is used internally by the GENESIS platform to maintain
sovereignty and enable deployment in any environment.
"""

from __future__ import annotations
from typing import List, Tuple
from genesis.constants import PI, E, SQRT2


def sqrt(x: float) -> float:
    """
    Compute square root using Newton's method.
    
    Args:
        x: Non-negative number.
        
    Returns:
        Square root of x.
        
    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number")
    if x == 0:
        return 0.0
    
    guess = x / 2 if x > 1 else 1.0
    
    for _ in range(50):
        new_guess = 0.5 * (guess + x / guess)
        if abs(new_guess - guess) < 1e-15 * abs(guess):
            return new_guess
        guess = new_guess
    
    return guess


def exp(x: float) -> float:
    """
    Compute exponential e^x.
    
    Args:
        x: The exponent.
        
    Returns:
        e raised to the power x.
    """
    if x > 700:
        return float('inf')
    if x < -700:
        return 0.0
    
    # Range reduction
    k = int(round(x))
    r = x - k
    
    # Taylor series for e^r
    result = 1.0
    term = 1.0
    for n in range(1, 50):
        term *= r / n
        result += term
        if abs(term) < 1e-15:
            break
    
    # Compute e^k efficiently
    if k != 0:
        e_power = 1.0
        base = E if k > 0 else 1 / E
        k = abs(k)
        while k > 0:
            if k & 1:
                e_power *= base
            base *= base
            k >>= 1
        result *= e_power
    
    return result


def ln(x: float) -> float:
    """
    Compute natural logarithm.
    
    Args:
        x: Positive number.
        
    Returns:
        Natural logarithm of x.
        
    Raises:
        ValueError: If x is not positive.
    """
    if x <= 0:
        raise ValueError("Cannot compute ln of non-positive number")
    
    ln2 = 0.6931471805599453
    
    # Range reduction
    e = 0
    m = x
    while m >= 2:
        m /= 2
        e += 1
    while m < 1:
        m *= 2
        e -= 1
    
    # Series expansion
    y = (m - 1) / (m + 1)
    y2 = y * y
    result = 0.0
    term = y
    for n in range(50):
        result += term / (2 * n + 1)
        term *= y2
        if abs(term) < 1e-15:
            break
    
    return 2 * result + e * ln2


def log(x: float, base: float = E) -> float:
    """
    Compute logarithm with arbitrary base.
    
    Args:
        x: Positive number.
        base: Logarithm base (default e).
        
    Returns:
        Logarithm of x in the given base.
    """
    return ln(x) / ln(base)


def pow(x: float, y: float) -> float:
    """
    Compute x raised to power y.
    
    Args:
        x: Base.
        y: Exponent.
        
    Returns:
        x^y.
    """
    if y == 0:
        return 1.0
    if x == 0:
        return 0.0 if y > 0 else float('inf')
    if x < 0 and y != int(y):
        raise ValueError("Cannot compute negative base to non-integer power")
    
    if x < 0:
        result = exp(y * ln(-x))
        return result if int(y) % 2 == 0 else -result
    
    return exp(y * ln(x))


def sin(x: float) -> float:
    """
    Compute sine.
    
    Args:
        x: Angle in radians.
        
    Returns:
        Sine of x.
    """
    # Reduce to [-π, π]
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    elif x < -PI:
        x += 2 * PI
    
    result = 0.0
    term = x
    x2 = x * x
    for n in range(25):
        result += term
        term *= -x2 / ((2 * n + 2) * (2 * n + 3))
        if abs(term) < 1e-15:
            break
    
    return result


def cos(x: float) -> float:
    """
    Compute cosine.
    
    Args:
        x: Angle in radians.
        
    Returns:
        Cosine of x.
    """
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    elif x < -PI:
        x += 2 * PI
    
    result = 0.0
    term = 1.0
    x2 = x * x
    for n in range(25):
        result += term
        term *= -x2 / ((2 * n + 1) * (2 * n + 2))
        if abs(term) < 1e-15:
            break
    
    return result


def tan(x: float) -> float:
    """Compute tangent."""
    c = cos(x)
    if abs(c) < 1e-10:
        raise ValueError("Tangent undefined at this angle")
    return sin(x) / c


def asin(x: float) -> float:
    """
    Compute arcsine.
    
    Args:
        x: Value in [-1, 1].
        
    Returns:
        Arcsine in radians.
    """
    if abs(x) > 1:
        raise ValueError("asin argument must be in [-1, 1]")
    
    if abs(x) > 0.5:
        # Use identity: asin(x) = π/2 - 2*asin(sqrt((1-x)/2))
        sign = 1 if x > 0 else -1
        return sign * (PI / 2 - 2 * asin(sqrt((1 - abs(x)) / 2)))
    
    # Taylor series
    result = x
    term = x
    x2 = x * x
    for n in range(1, 50):
        term *= x2 * (2 * n - 1) * (2 * n - 1) / (2 * n * (2 * n + 1))
        result += term
        if abs(term) < 1e-15:
            break
    
    return result


def acos(x: float) -> float:
    """Compute arccosine."""
    return PI / 2 - asin(x)


def atan(x: float) -> float:
    """Compute arctangent."""
    if abs(x) > 1:
        if x > 0:
            return PI / 2 - atan(1 / x)
        else:
            return -PI / 2 - atan(1 / x)
    
    result = 0.0
    term = x
    x2 = x * x
    for n in range(100):
        result += term / (2 * n + 1)
        term *= -x2
        if abs(term / (2 * n + 3)) < 1e-15:
            break
    
    return result


def atan2(y: float, x: float) -> float:
    """Compute atan2(y, x)."""
    if x == 0:
        if y > 0:
            return PI / 2
        elif y < 0:
            return -PI / 2
        return 0.0
    
    result = atan(y / x)
    if x < 0:
        result += PI if y >= 0 else -PI
    
    return result


def sinh(x: float) -> float:
    """Compute hyperbolic sine."""
    if abs(x) > 700:
        return float('inf') if x > 0 else float('-inf')
    ex = exp(x)
    return (ex - 1 / ex) / 2


def cosh(x: float) -> float:
    """Compute hyperbolic cosine."""
    if abs(x) > 700:
        return float('inf')
    ex = exp(x)
    return (ex + 1 / ex) / 2


def tanh(x: float) -> float:
    """Compute hyperbolic tangent."""
    if x > 20:
        return 1.0
    if x < -20:
        return -1.0
    ex = exp(2 * x)
    return (ex - 1) / (ex + 1)


def floor(x: float) -> int:
    """Return floor of x."""
    i = int(x)
    return i if x >= 0 or x == i else i - 1


def ceil(x: float) -> int:
    """Return ceiling of x."""
    i = int(x)
    return i if x <= 0 or x == i else i + 1


def factorial(n: int) -> int:
    """Compute factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def gcd(a: int, b: int) -> int:
    """Compute greatest common divisor."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Compute least common multiple."""
    return abs(a * b) // gcd(a, b)


def dot_product(v1: List[float], v2: List[float]) -> float:
    """Compute dot product of two vectors."""
    if len(v1) != len(v2):
        raise ValueError("Vectors must have same length")
    return sum(a * b for a, b in zip(v1, v2))


def norm(v: List[float]) -> float:
    """Compute Euclidean norm of a vector."""
    return sqrt(sum(x * x for x in v))


def normalize(v: List[float]) -> List[float]:
    """Normalize a vector to unit length."""
    n = norm(v)
    if n == 0:
        raise ValueError("Cannot normalize zero vector")
    return [x / n for x in v]


def matrix_multiply(
    a: List[List[float]], 
    b: List[List[float]]
) -> List[List[float]]:
    """Multiply two matrices."""
    if len(a[0]) != len(b):
        raise ValueError("Matrix dimensions incompatible")
    
    rows_a, cols_a = len(a), len(a[0])
    cols_b = len(b[0])
    
    result = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result


def matrix_vector_multiply(
    m: List[List[float]], 
    v: List[float]
) -> List[float]:
    """Multiply a matrix by a vector."""
    if len(m[0]) != len(v):
        raise ValueError("Matrix and vector dimensions incompatible")
    
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]


def transpose(m: List[List[float]]) -> List[List[float]]:
    """Transpose a matrix."""
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def identity_matrix(n: int) -> List[List[float]]:
    """Create an n×n identity matrix."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def kronecker_product(
    a: List[List[float]], 
    b: List[List[float]]
) -> List[List[float]]:
    """Compute Kronecker (tensor) product of two matrices."""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    result = [[0.0] * (cols_a * cols_b) for _ in range(rows_a * rows_b)]
    
    for i in range(rows_a):
        for j in range(cols_a):
            for k in range(rows_b):
                for l in range(cols_b):
                    result[i * rows_b + k][j * cols_b + l] = a[i][j] * b[k][l]
    
    return result

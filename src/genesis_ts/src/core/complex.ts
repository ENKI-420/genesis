/**
 * Sovereign Complex Number Implementation
 *
 * Zero-dependency complex number arithmetic for quantum state representation.
 */

export class Complex {
  readonly real: number;
  readonly imag: number;

  constructor(real: number, imag: number = 0) {
    this.real = real;
    this.imag = imag;
  }

  /**
   * Create a complex number from polar form.
   */
  static fromPolar(r: number, theta: number): Complex {
    return new Complex(r * Math.cos(theta), r * Math.sin(theta));
  }

  /**
   * Create the imaginary unit i.
   */
  static i(): Complex {
    return new Complex(0, 1);
  }

  /**
   * Create zero.
   */
  static zero(): Complex {
    return new Complex(0, 0);
  }

  /**
   * Create one.
   */
  static one(): Complex {
    return new Complex(1, 0);
  }

  /**
   * Add two complex numbers.
   */
  add(other: Complex): Complex {
    return new Complex(this.real + other.real, this.imag + other.imag);
  }

  /**
   * Subtract a complex number.
   */
  sub(other: Complex): Complex {
    return new Complex(this.real - other.real, this.imag - other.imag);
  }

  /**
   * Multiply two complex numbers.
   */
  mul(other: Complex): Complex {
    return new Complex(
      this.real * other.real - this.imag * other.imag,
      this.real * other.imag + this.imag * other.real
    );
  }

  /**
   * Divide by a complex number.
   */
  div(other: Complex): Complex {
    const denom = other.real * other.real + other.imag * other.imag;
    if (denom === 0) {
      throw new Error('Division by zero');
    }
    return new Complex(
      (this.real * other.real + this.imag * other.imag) / denom,
      (this.imag * other.real - this.real * other.imag) / denom
    );
  }

  /**
   * Scale by a real number.
   */
  scale(factor: number): Complex {
    return new Complex(this.real * factor, this.imag * factor);
  }

  /**
   * Get the complex conjugate.
   */
  conjugate(): Complex {
    return new Complex(this.real, -this.imag);
  }

  /**
   * Get the magnitude (absolute value).
   */
  magnitude(): number {
    return Math.sqrt(this.real * this.real + this.imag * this.imag);
  }

  /**
   * Get the magnitude squared.
   */
  magnitudeSquared(): number {
    return this.real * this.real + this.imag * this.imag;
  }

  /**
   * Get the phase angle in radians.
   */
  phase(): number {
    return Math.atan2(this.imag, this.real);
  }

  /**
   * Get the complex exponential e^(i*theta).
   */
  static exp(theta: number): Complex {
    return new Complex(Math.cos(theta), Math.sin(theta));
  }

  /**
   * Compute e^z for a complex number z.
   */
  exp(): Complex {
    const r = Math.exp(this.real);
    return new Complex(r * Math.cos(this.imag), r * Math.sin(this.imag));
  }

  /**
   * Check if equal to another complex number.
   */
  equals(other: Complex, tolerance: number = 1e-10): boolean {
    return (
      Math.abs(this.real - other.real) < tolerance &&
      Math.abs(this.imag - other.imag) < tolerance
    );
  }

  /**
   * String representation.
   */
  toString(): string {
    if (this.imag === 0) {
      return `${this.real}`;
    } else if (this.real === 0) {
      return `${this.imag}i`;
    } else if (this.imag > 0) {
      return `${this.real}+${this.imag}i`;
    } else {
      return `${this.real}${this.imag}i`;
    }
  }
}

/**
 * Convenience function to create complex numbers.
 */
export function complex(real: number, imag: number = 0): Complex {
  return new Complex(real, imag);
}

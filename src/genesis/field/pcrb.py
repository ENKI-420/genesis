"""
Phase Conjugate Recursion Bus (PCRB)

Implements the PCRB for information preservation during temporal evolution.
The PCRB uses phase conjugation to reverse information degradation and
maintain coherence across the autopoietic field.

Key concept: Phase conjugation creates a "time-reversed" replica of the
input signal, allowing for perfect reconstruction in ideal conditions.

Universal Constants:
- χ_pc = 0.869 (Phase Conjugate Fidelity)
"""

from typing import Optional
from genesis.constants import CHI_PC, LAMBDA_PHI, PI
from genesis.core.complex import Complex
from genesis.core.math import cos, sin, exp, sqrt


class PhaseConjugateRecursionBus:
    """
    Phase Conjugate Recursion Bus for information preservation.
    
    The PCRB implements phase conjugation to maintain quantum coherence
    during temporal evolution. It achieves this by:
    
    1. Recording the phase history of signals
    2. Computing phase conjugates to reverse degradation
    3. Recursively refining the signal through multiple passes
    
    Attributes:
        fidelity: Maximum achievable fidelity (χ_pc ≈ 0.869).
        recursion_depth: Number of conjugation passes.
        phase_history: History of phase values.
    """
    
    def __init__(
        self,
        fidelity: float = CHI_PC,
        recursion_depth: int = 3,
    ) -> None:
        """
        Initialize the PCRB.
        
        Args:
            fidelity: Maximum fidelity per conjugation pass.
            recursion_depth: Number of recursive conjugation passes.
        """
        self.fidelity = fidelity
        self.recursion_depth = recursion_depth
        self.phase_history: list[float] = []
    
    def conjugate(self, signal: Complex) -> Complex:
        """
        Compute the phase conjugate of a complex signal.
        
        The phase conjugate reverses the phase: e^{iφ} → e^{-iφ}
        
        Args:
            signal: Input complex signal.
            
        Returns:
            Phase-conjugated signal.
        """
        return signal.conjugate()
    
    def process(
        self,
        signal: Complex,
        time: float,
        degradation: float = 0.0,
    ) -> Complex:
        """
        Process a signal through the PCRB.
        
        Applies phase conjugation and fidelity correction to recover
        information degraded by decoherence.
        
        Args:
            signal: Input signal (possibly degraded).
            time: Current temporal coordinate.
            degradation: Amount of phase degradation to correct.
            
        Returns:
            Recovered signal with improved fidelity.
        """
        # Record phase history
        self.phase_history.append(signal.phase())
        
        # Apply degradation model
        if degradation > 0:
            # Degradation reduces amplitude and scrambles phase
            noise_phase = degradation * LAMBDA_PHI * time
            degraded = Complex(
                signal.magnitude() * exp(-degradation * time) * cos(noise_phase),
                signal.magnitude() * exp(-degradation * time) * sin(noise_phase),
            )
            signal = degraded
        
        # Recursive phase conjugation
        recovered = signal
        for _ in range(self.recursion_depth):
            # Conjugate and scale by fidelity
            conjugated = self.conjugate(recovered)
            
            # Mix original and conjugate
            mix_factor = self.fidelity
            recovered = Complex(
                mix_factor * signal.real + (1 - mix_factor) * conjugated.real,
                mix_factor * signal.imag + (1 - mix_factor) * conjugated.imag,
            )
        
        return recovered
    
    def estimate_fidelity(
        self,
        original: Complex,
        recovered: Complex,
    ) -> float:
        """
        Estimate the fidelity between original and recovered signals.
        
        Fidelity is defined as:
            F = |⟨original|recovered⟩|² / (|original|² × |recovered|²)
        
        Args:
            original: Original undegraded signal.
            recovered: Signal after PCRB processing.
            
        Returns:
            Fidelity value in [0, 1].
        """
        # Inner product
        inner = original.conjugate() * recovered
        
        # Magnitudes
        mag_orig = original.magnitude()
        mag_recv = recovered.magnitude()
        
        if mag_orig < 1e-10 or mag_recv < 1e-10:
            return 0.0
        
        fidelity = (inner.magnitude() ** 2) / (mag_orig ** 2 * mag_recv ** 2)
        return min(1.0, fidelity)
    
    def optimal_recursion_depth(
        self,
        degradation: float,
        target_fidelity: float = 0.99,
    ) -> int:
        """
        Compute optimal recursion depth for target fidelity.
        
        Args:
            degradation: Input degradation level.
            target_fidelity: Desired output fidelity.
            
        Returns:
            Optimal number of recursion passes.
        """
        if degradation <= 0:
            return 1
        
        # Each pass improves fidelity by approximately χ_pc
        # After n passes: fidelity ≈ 1 - (1 - χ_pc)^n × degradation
        
        current_fidelity = 1.0 - degradation
        depth = 0
        
        while current_fidelity < target_fidelity and depth < 100:
            improvement = (1.0 - current_fidelity) * self.fidelity
            current_fidelity += improvement
            depth += 1
        
        return max(1, depth)
    
    def reset(self) -> None:
        """Clear the phase history."""
        self.phase_history = []


def conjugate_phase(signal: Complex) -> Complex:
    """
    Convenience function for phase conjugation.
    
    Args:
        signal: Input complex signal.
        
    Returns:
        Phase-conjugated signal.
    """
    return signal.conjugate()


class PCRBChannel:
    """
    A full PCRB communication channel with encoding and decoding.
    
    This class models a complete information channel using phase conjugation
    for error correction. It includes:
    
    - Encoding: Maps classical data to phase-encoded signals
    - Transmission: Simulates noisy channel propagation
    - Decoding: Recovers data using phase conjugation
    """
    
    def __init__(
        self,
        fidelity: float = CHI_PC,
        channel_length: float = 1.0,
        noise_strength: float = 0.1,
    ) -> None:
        """
        Initialize the PCRB channel.
        
        Args:
            fidelity: PCRB fidelity parameter.
            channel_length: Effective channel length.
            noise_strength: Channel noise strength.
        """
        self.pcrb = PhaseConjugateRecursionBus(fidelity)
        self.channel_length = channel_length
        self.noise_strength = noise_strength
    
    def encode(self, data: list[float]) -> list[Complex]:
        """
        Encode classical data as phase-encoded signals.
        
        Args:
            data: List of values in [0, 1].
            
        Returns:
            List of complex phase-encoded signals.
        """
        encoded: list[Complex] = []
        for value in data:
            # Map value to phase angle
            phase = 2 * PI * value
            signal = Complex(cos(phase), sin(phase))
            encoded.append(signal)
        return encoded
    
    def transmit(self, signals: list[Complex]) -> list[Complex]:
        """
        Transmit signals through noisy channel.
        
        Args:
            signals: Encoded signals.
            
        Returns:
            Signals after channel transmission.
        """
        transmitted: list[Complex] = []
        for i, signal in enumerate(signals):
            # Apply channel noise
            t = i * self.channel_length / max(1, len(signals) - 1)
            degraded = self.pcrb.process(
                signal, t, self.noise_strength
            )
            transmitted.append(degraded)
        return transmitted
    
    def decode(self, signals: list[Complex]) -> list[float]:
        """
        Decode signals back to classical data.
        
        Args:
            signals: Received signals.
            
        Returns:
            Recovered classical data.
        """
        decoded: list[float] = []
        for signal in signals:
            # Extract phase and map back to value
            phase = signal.phase()
            # Normalize to [0, 1]
            value = (phase / (2 * PI)) % 1.0
            if value < 0:
                value += 1.0
            decoded.append(value)
        return decoded
    
    def channel_capacity(self) -> float:
        """
        Estimate the channel capacity.
        
        Returns:
            Estimated bits per symbol capacity.
        """
        # Shannon capacity with effective SNR
        snr = self.pcrb.fidelity / max(0.01, self.noise_strength)
        
        # C = log2(1 + SNR)
        from genesis.core.math import log2
        return log2(1.0 + snr)

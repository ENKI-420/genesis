"""
Compartments and Compartmentalization

Implements compartmented access control for SCI and SAP programs
in the GENESIS platform. Compartments provide need-to-know isolation
beyond classification level.

Key concepts:
- Compartments: Isolated containers of information
- Read-in: Process of granting compartment access
- Need-to-know: Verification of access requirement
- Codewords: Short names for compartments
"""

from typing import Optional
from genesis.classification.levels import (
    ClassificationLevel,
    TS_SCI,
    SAP,
)


class Compartment:
    """
    A classified compartment for information isolation.
    
    Compartments are used to isolate sensitive information beyond
    classification level. Access requires specific read-in and
    need-to-know verification.
    
    Attributes:
        name: Compartment name.
        codeword: Short codeword for the compartment.
        level: Minimum classification level.
        description: Description of the compartment.
        sub_compartments: Sub-compartments within this compartment.
    """
    
    def __init__(
        self,
        name: str,
        codeword: str,
        level: ClassificationLevel = TS_SCI,
        description: Optional[str] = None,
        parent: Optional["Compartment"] = None,
    ) -> None:
        """
        Initialize a compartment.
        
        Args:
            name: Full compartment name.
            codeword: Short identifier.
            level: Minimum classification level.
            description: Description of compartment purpose.
            parent: Parent compartment if this is a sub-compartment.
        """
        self.name = name
        self.codeword = codeword
        self.level = level
        self.description = description or ""
        self.parent = parent
        self.sub_compartments: list["Compartment"] = []
        
        if parent:
            parent.sub_compartments.append(self)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.codeword}: {self.name}"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"Compartment(codeword='{self.codeword}', name='{self.name}')"
    
    def __eq__(self, other: object) -> bool:
        """Check equality by codeword."""
        if not isinstance(other, Compartment):
            return False
        return self.codeword == other.codeword
    
    def __hash__(self) -> int:
        """Hash by codeword."""
        return hash(self.codeword)
    
    def full_path(self) -> str:
        """Get full compartment path including parents."""
        if self.parent:
            return f"{self.parent.full_path()}/{self.codeword}"
        return self.codeword
    
    def is_subcompartment(self, potential_parent: "Compartment") -> bool:
        """Check if this is a sub-compartment of another."""
        current = self.parent
        while current:
            if current == potential_parent:
                return True
            current = current.parent
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "codeword": self.codeword,
            "level": self.level.name,
            "description": self.description,
            "parent": self.parent.codeword if self.parent else None,
            "sub_compartments": [
                c.codeword for c in self.sub_compartments
            ],
        }


class CompartmentSet:
    """
    A set of compartments for access control.
    
    Used to represent a user's compartment access or a document's
    compartment requirements.
    """
    
    def __init__(
        self,
        compartments: Optional[list[Compartment]] = None,
    ) -> None:
        """
        Initialize a compartment set.
        
        Args:
            compartments: Initial compartments in the set.
        """
        self._compartments: set[Compartment] = set(compartments or [])
    
    def __contains__(self, item: Compartment) -> bool:
        """Check if compartment is in set."""
        return item in self._compartments
    
    def __iter__(self):
        """Iterate over compartments."""
        return iter(self._compartments)
    
    def __len__(self) -> int:
        """Number of compartments."""
        return len(self._compartments)
    
    def __str__(self) -> str:
        """String representation."""
        codewords = sorted(c.codeword for c in self._compartments)
        return "/".join(codewords) if codewords else "(none)"
    
    def add(self, compartment: Compartment) -> None:
        """Add a compartment to the set."""
        self._compartments.add(compartment)
    
    def remove(self, compartment: Compartment) -> None:
        """Remove a compartment from the set."""
        self._compartments.discard(compartment)
    
    def covers(self, other: "CompartmentSet") -> bool:
        """
        Check if this set covers (contains all compartments of) another.
        
        Used for access control: user's set must cover document's set.
        
        Args:
            other: The set to check coverage against.
            
        Returns:
            True if all compartments in other are in self.
        """
        return all(c in self._compartments for c in other)
    
    def intersection(self, other: "CompartmentSet") -> "CompartmentSet":
        """Get compartments in both sets."""
        return CompartmentSet(
            [c for c in self._compartments if c in other._compartments]
        )
    
    def union(self, other: "CompartmentSet") -> "CompartmentSet":
        """Get compartments in either set."""
        return CompartmentSet(
            list(self._compartments | other._compartments)
        )
    
    def to_list(self) -> list[str]:
        """Get list of codewords."""
        return sorted(c.codeword for c in self._compartments)


def create_compartment(
    name: str,
    codeword: str,
    level: str = "TS_SCI",
    description: Optional[str] = None,
) -> Compartment:
    """
    Create a new compartment.
    
    Args:
        name: Compartment name.
        codeword: Short identifier.
        level: Classification level name.
        description: Description.
        
    Returns:
        New Compartment instance.
    """
    from genesis.classification.levels import get_level
    
    return Compartment(
        name=name,
        codeword=codeword,
        level=get_level(level),
        description=description,
    )


# Standard compartments for GENESIS
GENESIS_COMPARTMENTS = {
    "AIDEN": Compartment(
        name="AIDEN Optimizer Intelligence",
        codeword="AIDEN",
        level=TS_SCI,
        description="Access to AIDEN optimizer algorithms and parameters",
    ),
    "AURA": Compartment(
        name="AURA Geometric Intelligence",
        codeword="AURA",
        level=TS_SCI,
        description="Access to AURA geometer and consciousness geometry",
    ),
    "PALS": Compartment(
        name="PALS Sentinel Operations",
        codeword="PALS",
        level=TS_SCI,
        description="Access to PALS security and monitoring",
    ),
    "CHRONOS": Compartment(
        name="CHRONOS Temporal Operations",
        codeword="CHRONOS",
        level=SAP,
        description="Access to temporal prediction and analysis",
    ),
    "AEGIS": Compartment(
        name="AEGIS Security Shield",
        codeword="AEGIS",
        level=SAP,
        description="Access to AEGIS security protocols",
    ),
    "DNARHO": Compartment(
        name="DNA-Lang Research Operations",
        codeword="DNARHO",
        level=TS_SCI,
        description="Access to DNA-Lang development and research",
    ),
    "QUBIT": Compartment(
        name="Quantum Infrastructure",
        codeword="QUBIT",
        level=TS_SCI,
        description="Access to quantum simulation infrastructure",
    ),
}


def get_genesis_compartment(codeword: str) -> Optional[Compartment]:
    """
    Get a standard GENESIS compartment by codeword.
    
    Args:
        codeword: The compartment codeword.
        
    Returns:
        The compartment or None if not found.
    """
    return GENESIS_COMPARTMENTS.get(codeword.upper())


def list_genesis_compartments() -> list[Compartment]:
    """Get all standard GENESIS compartments."""
    return list(GENESIS_COMPARTMENTS.values())

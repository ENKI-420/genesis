"""
Access Validator

Implements access validation for the GENESIS classification system.
Validates that users have appropriate clearance, compartment access,
and need-to-know before granting access to information.

Key validation steps:
1. Clearance level check
2. Compartment access verification
3. Need-to-know verification
4. Additional controls (NOFORN, etc.)
"""

from typing import Optional
from genesis.classification.levels import (
    ClassificationLevel,
    dominates,
    UNCLASSIFIED,
)
from genesis.classification.compartments import (
    Compartment,
    CompartmentSet,
)


class Clearance:
    """
    A security clearance for access control.
    
    Represents a person's security clearance including:
    - Maximum classification level
    - Compartment access
    - Nationality/citizenship
    - Additional access attributes
    """
    
    def __init__(
        self,
        level: ClassificationLevel,
        compartments: Optional[CompartmentSet] = None,
        nationality: str = "USA",
        contractor: bool = False,
        sci_access: bool = False,
    ) -> None:
        """
        Initialize a clearance.
        
        Args:
            level: Maximum classification level.
            compartments: Set of compartments with access.
            nationality: Citizenship/nationality.
            contractor: Whether holder is a contractor.
            sci_access: Whether holder has SCI access.
        """
        self.level = level
        self.compartments = compartments or CompartmentSet()
        self.nationality = nationality
        self.contractor = contractor
        self.sci_access = sci_access
    
    def __str__(self) -> str:
        """String representation."""
        parts = [self.level.name]
        
        if self.sci_access:
            parts.append("SCI")
        
        if len(self.compartments) > 0:
            parts.append(str(self.compartments))
        
        return "/".join(parts)
    
    def can_access_level(self, level: ClassificationLevel) -> bool:
        """Check if clearance covers a classification level."""
        return dominates(self.level, level)
    
    def can_access_compartment(self, compartment: Compartment) -> bool:
        """Check if clearance includes compartment access."""
        return compartment in self.compartments
    
    def add_compartment(self, compartment: Compartment) -> None:
        """Add compartment access (read-in)."""
        self.compartments.add(compartment)
    
    def remove_compartment(self, compartment: Compartment) -> None:
        """Remove compartment access (debriefing)."""
        self.compartments.remove(compartment)
    
    def is_us_person(self) -> bool:
        """Check if holder is a US person."""
        return self.nationality == "USA"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "level": self.level.name,
            "compartments": self.compartments.to_list(),
            "nationality": self.nationality,
            "contractor": self.contractor,
            "sci_access": self.sci_access,
        }


class AccessRequirement:
    """
    Access requirements for a piece of information.
    
    Specifies what clearance, compartments, and other conditions
    are required to access the information.
    """
    
    def __init__(
        self,
        level: ClassificationLevel = UNCLASSIFIED,
        compartments: Optional[CompartmentSet] = None,
        noforn: bool = False,
        nocontractor: bool = False,
        orcon: bool = False,
        releasable_to: Optional[list[str]] = None,
        need_to_know_verified: bool = False,
    ) -> None:
        """
        Initialize access requirements.
        
        Args:
            level: Classification level.
            compartments: Required compartment access.
            noforn: No foreign nationals.
            nocontractor: No contractors.
            orcon: Originator controlled.
            releasable_to: List of releasable nationalities.
            need_to_know_verified: Whether NTK has been verified.
        """
        self.level = level
        self.compartments = compartments or CompartmentSet()
        self.noforn = noforn
        self.nocontractor = nocontractor
        self.orcon = orcon
        self.releasable_to = releasable_to or []
        self.need_to_know_verified = need_to_know_verified
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "level": self.level.name,
            "compartments": self.compartments.to_list(),
            "noforn": self.noforn,
            "nocontractor": self.nocontractor,
            "orcon": self.orcon,
            "releasable_to": self.releasable_to,
        }


class AccessValidator:
    """
    Validates access to classified information.
    
    Performs comprehensive access validation including:
    - Classification level
    - Compartment access
    - Nationality restrictions
    - Contractor restrictions
    - Need-to-know
    """
    
    def __init__(
        self,
        require_need_to_know: bool = True,
        audit_log: bool = True,
    ) -> None:
        """
        Initialize the access validator.
        
        Args:
            require_need_to_know: Whether to enforce NTK.
            audit_log: Whether to log access decisions.
        """
        self.require_need_to_know = require_need_to_know
        self.audit_log = audit_log
        self._log: list[dict] = []
    
    def validate(
        self,
        clearance: Clearance,
        requirement: AccessRequirement,
        need_to_know: bool = False,
        purpose: Optional[str] = None,
    ) -> tuple[bool, str]:
        """
        Validate access.
        
        Args:
            clearance: The user's clearance.
            requirement: The information's access requirements.
            need_to_know: Whether NTK has been established.
            purpose: Purpose for access (for audit).
            
        Returns:
            Tuple of (granted: bool, reason: str).
        """
        # Check classification level
        if not clearance.can_access_level(requirement.level):
            return self._deny(
                clearance, requirement, purpose,
                f"Clearance level {clearance.level.name} insufficient for "
                f"{requirement.level.name}"
            )
        
        # Check compartments
        if not clearance.compartments.covers(requirement.compartments):
            missing = [
                c.codeword for c in requirement.compartments
                if c not in clearance.compartments
            ]
            return self._deny(
                clearance, requirement, purpose,
                f"Missing compartment access: {', '.join(missing)}"
            )
        
        # Check NOFORN
        if requirement.noforn and not clearance.is_us_person():
            return self._deny(
                clearance, requirement, purpose,
                "NOFORN restriction - US persons only"
            )
        
        # Check releasability
        if requirement.releasable_to:
            if clearance.nationality not in requirement.releasable_to:
                return self._deny(
                    clearance, requirement, purpose,
                    f"Not releasable to {clearance.nationality}"
                )
        
        # Check contractor restriction
        if requirement.nocontractor and clearance.contractor:
            return self._deny(
                clearance, requirement, purpose,
                "NOCONTRACTOR restriction"
            )
        
        # Check need-to-know
        if self.require_need_to_know and requirement.level > UNCLASSIFIED:
            if not need_to_know and not requirement.need_to_know_verified:
                return self._deny(
                    clearance, requirement, purpose,
                    "Need-to-know not established"
                )
        
        # Access granted
        return self._grant(clearance, requirement, purpose)
    
    def _grant(
        self,
        clearance: Clearance,
        requirement: AccessRequirement,
        purpose: Optional[str],
    ) -> tuple[bool, str]:
        """Log and return grant decision."""
        if self.audit_log:
            self._log.append({
                "decision": "GRANTED",
                "clearance": str(clearance),
                "requirement_level": requirement.level.name,
                "purpose": purpose,
            })
        return (True, "Access granted")
    
    def _deny(
        self,
        clearance: Clearance,
        requirement: AccessRequirement,
        purpose: Optional[str],
        reason: str,
    ) -> tuple[bool, str]:
        """Log and return deny decision."""
        if self.audit_log:
            self._log.append({
                "decision": "DENIED",
                "clearance": str(clearance),
                "requirement_level": requirement.level.name,
                "purpose": purpose,
                "reason": reason,
            })
        return (False, reason)
    
    def get_audit_log(self) -> list[dict]:
        """Get the audit log."""
        return self._log.copy()
    
    def clear_audit_log(self) -> None:
        """Clear the audit log."""
        self._log = []


def validate_access(
    user_level: str,
    info_level: str,
    user_compartments: Optional[list[str]] = None,
    info_compartments: Optional[list[str]] = None,
    need_to_know: bool = True,
) -> tuple[bool, str]:
    """
    Convenience function for access validation.
    
    Args:
        user_level: User's clearance level name.
        info_level: Information's classification level name.
        user_compartments: User's compartment codewords.
        info_compartments: Information's compartment requirements.
        need_to_know: Whether NTK is established.
        
    Returns:
        Tuple of (granted: bool, reason: str).
    """
    from genesis.classification.levels import get_level
    from genesis.classification.compartments import (
        get_genesis_compartment,
        CompartmentSet,
    )
    
    # Build clearance
    user_comps = CompartmentSet()
    for cw in (user_compartments or []):
        comp = get_genesis_compartment(cw)
        if comp:
            user_comps.add(comp)
    
    clearance = Clearance(
        level=get_level(user_level),
        compartments=user_comps,
        sci_access=get_level(user_level).value >= 4,
    )
    
    # Build requirement
    info_comps = CompartmentSet()
    for cw in (info_compartments or []):
        comp = get_genesis_compartment(cw)
        if comp:
            info_comps.add(comp)
    
    requirement = AccessRequirement(
        level=get_level(info_level),
        compartments=info_comps,
    )
    
    # Validate
    validator = AccessValidator()
    return validator.validate(clearance, requirement, need_to_know)

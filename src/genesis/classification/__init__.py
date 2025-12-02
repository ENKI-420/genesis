"""
GENESIS Classification Module

This module implements the DoD-aligned classification system for the
GENESIS platform. It provides:

- Classification levels (UNCLASSIFIED → TS/SCI → SAP)
- Compartmentalization and need-to-know access
- Classification markings and handling
- Access validation and control

The classification system is designed to be compatible with:
- Executive Order 13526
- ICD 705 (Sensitive Compartmented Information Facilities)
- DoD Manual 5200.01 (Information Security Program)
"""

from genesis.classification.levels import (
    ClassificationLevel,
    UNCLASSIFIED,
    CONFIDENTIAL,
    SECRET,
    TOP_SECRET,
    TS_SCI,
    SAP,
    get_level,
    compare_levels,
)
from genesis.classification.markings import (
    ClassificationMarking,
    PortionMarking,
    BannerLine,
    create_marking,
)
from genesis.classification.compartments import (
    Compartment,
    CompartmentSet,
    create_compartment,
)
from genesis.classification.validator import (
    AccessValidator,
    Clearance,
    validate_access,
)

__all__ = [
    # Levels
    "ClassificationLevel",
    "UNCLASSIFIED",
    "CONFIDENTIAL", 
    "SECRET",
    "TOP_SECRET",
    "TS_SCI",
    "SAP",
    "get_level",
    "compare_levels",
    # Markings
    "ClassificationMarking",
    "PortionMarking",
    "BannerLine",
    "create_marking",
    # Compartments
    "Compartment",
    "CompartmentSet",
    "create_compartment",
    # Validation
    "AccessValidator",
    "Clearance",
    "validate_access",
]

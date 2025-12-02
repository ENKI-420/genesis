"""
Classification Levels

Implements the DoD-aligned classification hierarchy for the GENESIS platform.

Classification Levels (ascending order):
1. UNCLASSIFIED (U)
2. CONFIDENTIAL (C)
3. SECRET (S)
4. TOP SECRET (TS)
5. TOP SECRET/SCI (TS/SCI)
6. Special Access Program (SAP)

Each level represents increasing sensitivity and requires correspondingly
higher clearances and need-to-know verification.
"""

from enum import IntEnum
from typing import Optional


class ClassificationLevel(IntEnum):
    """
    DoD-aligned classification levels.
    
    The integer values represent the hierarchy, with higher values
    indicating higher classification.
    """
    
    UNCLASSIFIED = 0
    """Publicly releasable information."""
    
    CONFIDENTIAL = 1
    """Could cause damage to national security if disclosed."""
    
    SECRET = 2
    """Could cause serious damage to national security if disclosed."""
    
    TOP_SECRET = 3
    """Could cause exceptionally grave damage to national security if disclosed."""
    
    TS_SCI = 4
    """
    Top Secret with Sensitive Compartmented Information.
    Requires SCI access and specific compartment read-in.
    """
    
    SAP = 5
    """
    Special Access Program.
    Most restricted access, requires program-specific read-in.
    """


# Convenient aliases
UNCLASSIFIED = ClassificationLevel.UNCLASSIFIED
CONFIDENTIAL = ClassificationLevel.CONFIDENTIAL
SECRET = ClassificationLevel.SECRET
TOP_SECRET = ClassificationLevel.TOP_SECRET
TS_SCI = ClassificationLevel.TS_SCI
SAP = ClassificationLevel.SAP


def get_level(name: str) -> ClassificationLevel:
    """
    Get classification level by name.
    
    Args:
        name: Level name (case-insensitive).
              Accepts common abbreviations (U, C, S, TS, TS/SCI).
    
    Returns:
        The corresponding ClassificationLevel.
        
    Raises:
        ValueError: If the name is not recognized.
    """
    name = name.upper().strip().replace("/", "_").replace("-", "_")
    
    # Handle common abbreviations
    abbreviations = {
        "U": "UNCLASSIFIED",
        "C": "CONFIDENTIAL",
        "S": "SECRET",
        "TS": "TOP_SECRET",
        "TOPSECRET": "TOP_SECRET",
        "TOP_SECRET": "TOP_SECRET",
        "TS_SCI": "TS_SCI",
        "TSSCI": "TS_SCI",
        "SCI": "TS_SCI",
        "SAP": "SAP",
    }
    
    if name in abbreviations:
        name = abbreviations[name]
    
    try:
        return ClassificationLevel[name]
    except KeyError:
        valid = ", ".join(level.name for level in ClassificationLevel)
        raise ValueError(f"Unknown classification level: {name}. Valid: {valid}")


def compare_levels(
    level1: ClassificationLevel,
    level2: ClassificationLevel,
) -> int:
    """
    Compare two classification levels.
    
    Args:
        level1: First classification level.
        level2: Second classification level.
        
    Returns:
        -1 if level1 < level2
         0 if level1 == level2
         1 if level1 > level2
    """
    if level1 < level2:
        return -1
    elif level1 > level2:
        return 1
    else:
        return 0


def get_abbreviation(level: ClassificationLevel) -> str:
    """
    Get the standard abbreviation for a classification level.
    
    Args:
        level: The classification level.
        
    Returns:
        Standard abbreviation string.
    """
    abbreviations = {
        ClassificationLevel.UNCLASSIFIED: "U",
        ClassificationLevel.CONFIDENTIAL: "C",
        ClassificationLevel.SECRET: "S",
        ClassificationLevel.TOP_SECRET: "TS",
        ClassificationLevel.TS_SCI: "TS/SCI",
        ClassificationLevel.SAP: "SAP",
    }
    return abbreviations.get(level, "?")


def get_color(level: ClassificationLevel) -> str:
    """
    Get the standard color code for a classification level.
    
    Args:
        level: The classification level.
        
    Returns:
        Color name (green, blue, red, orange, yellow).
    """
    colors = {
        ClassificationLevel.UNCLASSIFIED: "green",
        ClassificationLevel.CONFIDENTIAL: "blue",
        ClassificationLevel.SECRET: "red",
        ClassificationLevel.TOP_SECRET: "orange",
        ClassificationLevel.TS_SCI: "orange",
        ClassificationLevel.SAP: "yellow",
    }
    return colors.get(level, "white")


def is_classified(level: ClassificationLevel) -> bool:
    """
    Check if a level represents classified information.
    
    Args:
        level: The classification level.
        
    Returns:
        True if the level is CONFIDENTIAL or higher.
    """
    return level > ClassificationLevel.UNCLASSIFIED


def dominates(
    higher: ClassificationLevel,
    lower: ClassificationLevel,
) -> bool:
    """
    Check if one classification level dominates another.
    
    A level dominates another if it is greater than or equal to it.
    This is used for access control: a person with a higher clearance
    can access information at lower levels.
    
    Args:
        higher: The potentially dominating level.
        lower: The potentially dominated level.
        
    Returns:
        True if higher >= lower.
    """
    return higher >= lower


class LevelPolicy:
    """
    Classification level policy configuration.
    
    Defines the rules and requirements for each classification level
    in the GENESIS system.
    """
    
    def __init__(self, level: ClassificationLevel) -> None:
        """
        Initialize policy for a classification level.
        
        Args:
            level: The classification level.
        """
        self.level = level
    
    def requires_need_to_know(self) -> bool:
        """Check if need-to-know verification is required."""
        return self.level >= ClassificationLevel.CONFIDENTIAL
    
    def requires_clearance(self) -> bool:
        """Check if security clearance is required."""
        return self.level >= ClassificationLevel.CONFIDENTIAL
    
    def requires_sci_access(self) -> bool:
        """Check if SCI access is required."""
        return self.level >= ClassificationLevel.TS_SCI
    
    def requires_program_access(self) -> bool:
        """Check if program-specific access is required."""
        return self.level >= ClassificationLevel.SAP
    
    def max_network(self) -> str:
        """Get the maximum network for this classification."""
        if self.level == ClassificationLevel.UNCLASSIFIED:
            return "NIPRNET"
        elif self.level <= ClassificationLevel.SECRET:
            return "SIPRNET"
        else:
            return "JWICS"
    
    def retention_years(self) -> int:
        """Get the retention period in years."""
        periods = {
            ClassificationLevel.UNCLASSIFIED: 0,  # No mandatory retention
            ClassificationLevel.CONFIDENTIAL: 10,
            ClassificationLevel.SECRET: 25,
            ClassificationLevel.TOP_SECRET: 50,
            ClassificationLevel.TS_SCI: 75,
            ClassificationLevel.SAP: 75,
        }
        return periods.get(self.level, 10)
    
    def banner_text(self) -> str:
        """Get the banner text for document marking."""
        banners = {
            ClassificationLevel.UNCLASSIFIED: "UNCLASSIFIED",
            ClassificationLevel.CONFIDENTIAL: "CONFIDENTIAL",
            ClassificationLevel.SECRET: "SECRET",
            ClassificationLevel.TOP_SECRET: "TOP SECRET",
            ClassificationLevel.TS_SCI: "TOP SECRET//SCI",
            ClassificationLevel.SAP: "TOP SECRET//SAP",
        }
        return banners.get(self.level, "UNKNOWN")

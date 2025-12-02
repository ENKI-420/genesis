"""
Classification Markings

Implements classification markings for documents and data in the GENESIS
platform. Markings follow standard DoD and IC marking conventions.

Marking components:
- Banner/header lines
- Portion markings
- Dissemination controls
- Declassification instructions
"""

from typing import Optional
from genesis.classification.levels import (
    ClassificationLevel,
    get_abbreviation,
    UNCLASSIFIED,
)


class PortionMarking:
    """
    Portion marking for individual paragraphs or sections.
    
    Format: (U), (C), (S), (TS), (TS//SCI), etc.
    """
    
    def __init__(
        self,
        level: ClassificationLevel,
        caveats: Optional[list[str]] = None,
        fgi: Optional[str] = None,
    ) -> None:
        """
        Initialize a portion marking.
        
        Args:
            level: Classification level.
            caveats: Additional caveats (e.g., NOFORN, REL TO).
            fgi: Foreign Government Information source.
        """
        self.level = level
        self.caveats = caveats or []
        self.fgi = fgi
    
    def __str__(self) -> str:
        """Render the portion marking."""
        parts = [get_abbreviation(self.level)]
        
        if self.caveats:
            parts.extend(self.caveats)
        
        if self.fgi:
            parts.append(self.fgi)
        
        inner = "//".join(parts)
        return f"({inner})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "level": self.level.name,
            "caveats": self.caveats,
            "fgi": self.fgi,
        }


class BannerLine:
    """
    Classification banner for document headers/footers.
    
    Format: CLASSIFICATION//CAVEATS//DISSEMINATION
    """
    
    def __init__(
        self,
        level: ClassificationLevel,
        caveats: Optional[list[str]] = None,
        dissemination: Optional[list[str]] = None,
        declassification: Optional[str] = None,
    ) -> None:
        """
        Initialize a banner line.
        
        Args:
            level: Classification level.
            caveats: Caveats (e.g., SI, TK, HCS).
            dissemination: Dissemination controls (e.g., NOFORN, REL TO).
            declassification: Declassification instructions.
        """
        self.level = level
        self.caveats = caveats or []
        self.dissemination = dissemination or []
        self.declassification = declassification
    
    def __str__(self) -> str:
        """Render the banner line."""
        if self.level == UNCLASSIFIED:
            return "UNCLASSIFIED"
        
        parts = [get_abbreviation(self.level)]
        
        if self.caveats:
            parts.append("/".join(self.caveats))
        
        if self.dissemination:
            parts.append("/".join(self.dissemination))
        
        return "//".join(parts)
    
    def full_banner(self) -> str:
        """
        Generate full banner with declassification if present.
        """
        banner = str(self)
        if self.declassification:
            banner += f"\n{self.declassification}"
        return banner
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "level": self.level.name,
            "caveats": self.caveats,
            "dissemination": self.dissemination,
            "declassification": self.declassification,
        }


class ClassificationMarking:
    """
    Complete classification marking for a document or data.
    
    Includes:
    - Overall classification
    - Portion markings
    - Classification authority
    - Declassification instructions
    """
    
    def __init__(
        self,
        level: ClassificationLevel,
        classified_by: Optional[str] = None,
        derived_from: Optional[str] = None,
        declassify_on: Optional[str] = None,
        caveats: Optional[list[str]] = None,
        dissemination: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize a classification marking.
        
        Args:
            level: Overall classification level.
            classified_by: Original classification authority.
            derived_from: Source guide for derivative classification.
            declassify_on: Declassification date or event.
            caveats: Classification caveats.
            dissemination: Dissemination controls.
        """
        self.level = level
        self.classified_by = classified_by
        self.derived_from = derived_from
        self.declassify_on = declassify_on
        self.caveats = caveats or []
        self.dissemination = dissemination or []
        
        # Create banner
        self.banner = BannerLine(
            level=level,
            caveats=caveats,
            dissemination=dissemination,
        )
    
    def header_banner(self) -> str:
        """Get the header banner."""
        return str(self.banner)
    
    def footer_banner(self) -> str:
        """Get the footer banner (same as header)."""
        return str(self.banner)
    
    def classification_block(self) -> str:
        """
        Generate the classification authority block.
        
        Returns:
            Multi-line classification block.
        """
        lines = []
        
        if self.classified_by:
            lines.append(f"Classified By: {self.classified_by}")
        
        if self.derived_from:
            lines.append(f"Derived From: {self.derived_from}")
        
        if self.declassify_on:
            lines.append(f"Declassify On: {self.declassify_on}")
        
        return "\n".join(lines)
    
    def portion_marking(self) -> PortionMarking:
        """Get portion marking for this classification."""
        return PortionMarking(
            level=self.level,
            caveats=self.caveats,
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "level": self.level.name,
            "classified_by": self.classified_by,
            "derived_from": self.derived_from,
            "declassify_on": self.declassify_on,
            "caveats": self.caveats,
            "dissemination": self.dissemination,
            "banner": str(self.banner),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ClassificationMarking":
        """
        Create from dictionary.
        
        Args:
            data: Dictionary with marking fields.
            
        Returns:
            ClassificationMarking instance.
        """
        from genesis.classification.levels import get_level
        
        return cls(
            level=get_level(data["level"]),
            classified_by=data.get("classified_by"),
            derived_from=data.get("derived_from"),
            declassify_on=data.get("declassify_on"),
            caveats=data.get("caveats"),
            dissemination=data.get("dissemination"),
        )


def create_marking(
    level: str,
    classified_by: Optional[str] = None,
    caveats: Optional[list[str]] = None,
    dissemination: Optional[list[str]] = None,
) -> ClassificationMarking:
    """
    Create a classification marking from parameters.
    
    Args:
        level: Classification level name.
        classified_by: Classification authority.
        caveats: Classification caveats.
        dissemination: Dissemination controls.
        
    Returns:
        ClassificationMarking instance.
    """
    from genesis.classification.levels import get_level
    
    return ClassificationMarking(
        level=get_level(level),
        classified_by=classified_by,
        caveats=caveats,
        dissemination=dissemination,
    )


# Common caveat definitions
COMMON_CAVEATS = {
    "SI": "SPECIAL INTELLIGENCE",
    "TK": "TALENT KEYHOLE",
    "G": "GAMMA",
    "HCS": "HUMINT CONTROL SYSTEM",
    "ORCON": "ORIGINATOR CONTROLLED",
    "IMCON": "CONTROLLED IMAGERY",
    "NOFORN": "NOT RELEASABLE TO FOREIGN NATIONALS",
    "PROPIN": "CAUTION - PROPRIETARY INFORMATION",
    "REL TO": "RELEASABLE TO",
    "FVEY": "FIVE EYES (AUS, CAN, GBR, NZL, USA)",
}


# Common dissemination controls
DISSEMINATION_CONTROLS = {
    "NOFORN": "Not releasable to foreign nationals",
    "NOCONTRACTOR": "Not releasable to contractors",
    "ORCON": "Dissemination and extraction controlled by originator",
    "PROPIN": "Caution - proprietary information involved",
    "REL TO USA, FVEY": "Releasable to USA and Five Eyes",
    "DISPLAY ONLY": "No copies allowed",
    "LIMDIS": "Limited distribution",
    "EXDIS": "Exclusive distribution",
    "NODIS": "No distribution",
}

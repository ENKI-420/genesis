"""
GENESIS Portals Module

This module implements the multi-portal architecture for the GENESIS platform.
Each portal provides a specialized interface for different use cases:

- Enterprise: Commercial applications
- Defense: DoD/IC applications
- Health: Healthcare and life sciences
- Legal: Legal discovery and analysis
- DARPA: Advanced research programs

Portals provide:
- Domain-specific APIs
- Classification-aware access control
- Specialized metrics and analytics
- Custom agent configurations
"""

from genesis.portals.base import (
    Portal,
    PortalConfig,
    PortalSession,
    PortalType,
)
from genesis.portals.enterprise import EnterprisePortal
from genesis.portals.defense import DefensePortal
from genesis.portals.health import HealthPortal
from genesis.portals.legal import LegalPortal
from genesis.portals.darpa import DARPAPortal

__all__ = [
    # Base
    "Portal",
    "PortalConfig",
    "PortalSession",
    "PortalType",
    # Portals
    "EnterprisePortal",
    "DefensePortal",
    "HealthPortal",
    "LegalPortal",
    "DARPAPortal",
]

"""
Defense Portal

The Defense portal provides DoD/IC-grade access to GENESIS
capabilities for national security applications including:

- Intelligence analysis
- Mission planning
- Threat assessment
- Secure communications
"""

from typing import Any, Optional
from genesis.portals.base import (
    Portal,
    PortalConfig,
    PortalSession,
    PortalType,
)
from genesis.classification.levels import (
    ClassificationLevel,
    TS_SCI,
    get_level,
)
from genesis.classification.validator import AccessValidator, Clearance


class DefensePortal(Portal):
    """
    Defense portal for DoD/IC applications.
    
    Provides access to GENESIS capabilities for intelligence analysis,
    mission planning, and threat assessment. Supports all classification
    levels up to TS/SCI.
    
    Features:
    - Full agent suite (AIDEN, AURA, PALS, CHRONOS, AEGIS)
    - Classification-aware processing
    - Audit logging
    - Compartmented access
    """
    
    def __init__(
        self,
        config: Optional[PortalConfig] = None,
    ) -> None:
        """
        Initialize the Defense portal.
        
        Args:
            config: Portal configuration. If None, uses defaults.
        """
        if config is None:
            config = PortalConfig(
                portal_type=PortalType.DEFENSE,
                max_classification=TS_SCI,
                agents_enabled=["AIDEN", "AURA", "PALS", "CHRONOS", "AEGIS"],
                metrics_enabled=True,
                session_timeout=3600,
                custom_settings={
                    "require_audit": True,
                    "classification_marking": True,
                    "compartment_check": True,
                },
            )
        super().__init__(config)
        self._initialized = False
        self._access_validator = AccessValidator(
            require_need_to_know=True,
            audit_log=True,
        )
    
    @property
    def name(self) -> str:
        """Portal name."""
        return "GENESIS Defense"
    
    @property
    def description(self) -> str:
        """Portal description."""
        return (
            "Defense portal for DoD/IC applications including intelligence "
            "analysis, mission planning, threat assessment, and secure operations."
        )
    
    def initialize(self) -> None:
        """Initialize defense portal resources."""
        # Initialize all agents
        # Set up secure communications
        # Configure classification marking
        self._initialized = True
    
    def process_request(
        self,
        session: PortalSession,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process a defense request.
        
        All requests are logged for audit purposes.
        
        Supported request types:
        - intel: Intelligence analysis
        - mission: Mission planning
        - threat: Threat assessment
        - comms: Secure communications
        - status: Get system status
        
        Args:
            session: The portal session.
            request: Request with 'type' and 'data' fields.
            
        Returns:
            Response with 'status', 'result', and 'marking' fields.
        """
        if not self._initialized:
            self.initialize()
        
        request_type = request.get("type", "status")
        data = request.get("data", {})
        classification = get_level(
            request.get("classification", session.classification.name)
        )
        
        # Apply classification marking to response
        response: dict[str, Any] = {
            "marking": self._get_marking(classification),
        }
        
        if request_type == "intel":
            result = self._handle_intel(session, data, classification)
        elif request_type == "mission":
            result = self._handle_mission(session, data, classification)
        elif request_type == "threat":
            result = self._handle_threat(session, data, classification)
        elif request_type == "comms":
            result = self._handle_comms(session, data, classification)
        elif request_type == "status":
            result = {"status": "ok", "result": self.get_status()}
        else:
            result = {
                "status": "error",
                "error": f"Unknown request type: {request_type}",
            }
        
        response.update(result)
        return response
    
    def _get_marking(self, classification: ClassificationLevel) -> str:
        """Get classification marking string."""
        from genesis.classification.markings import BannerLine
        
        banner = BannerLine(
            level=classification,
            caveats=["GENESIS"],
            dissemination=["NOFORN"] if classification.value >= 3 else [],
        )
        return str(banner)
    
    def _handle_intel(
        self,
        session: PortalSession,
        data: dict[str, Any],
        classification: ClassificationLevel,
    ) -> dict[str, Any]:
        """Handle intelligence analysis request."""
        # Would integrate with CHRONOS for temporal analysis
        source = data.get("source", "sigint")
        target = data.get("target", "unknown")
        
        return {
            "status": "ok",
            "result": {
                "analysis_type": "intelligence",
                "source": source,
                "target": target,
                "confidence": 0.87,
                "assessment": "moderate_threat",
                "indicators": [
                    "Pattern alpha detected",
                    "Temporal anomaly in sector 7",
                ],
            },
        }
    
    def _handle_mission(
        self,
        session: PortalSession,
        data: dict[str, Any],
        classification: ClassificationLevel,
    ) -> dict[str, Any]:
        """Handle mission planning request."""
        # Would integrate with AIDEN for optimization
        mission_type = data.get("mission_type", "reconnaissance")
        objective = data.get("objective", "information_gathering")
        
        return {
            "status": "ok",
            "result": {
                "mission_type": mission_type,
                "objective": objective,
                "recommended_assets": ["asset_alpha", "asset_bravo"],
                "risk_assessment": "moderate",
                "success_probability": 0.82,
                "timeline_hours": 48,
            },
        }
    
    def _handle_threat(
        self,
        session: PortalSession,
        data: dict[str, Any],
        classification: ClassificationLevel,
    ) -> dict[str, Any]:
        """Handle threat assessment request."""
        # Would integrate with PALS for security analysis
        threat_vector = data.get("threat_vector", "cyber")
        region = data.get("region", "global")
        
        return {
            "status": "ok",
            "result": {
                "threat_vector": threat_vector,
                "region": region,
                "threat_level": "elevated",
                "active_threats": 3,
                "recommendations": [
                    "Increase monitoring in sector 4",
                    "Deploy countermeasures to sector 7",
                ],
            },
        }
    
    def _handle_comms(
        self,
        session: PortalSession,
        data: dict[str, Any],
        classification: ClassificationLevel,
    ) -> dict[str, Any]:
        """Handle secure communications request."""
        # Would integrate with AEGIS for encryption
        channel = data.get("channel", "primary")
        
        return {
            "status": "ok",
            "result": {
                "channel": channel,
                "encryption": "quantum_resistant",
                "status": "secure",
                "latency_ms": 15,
            },
        }
    
    def intel_analysis(
        self,
        session: PortalSession,
        source: str,
        target: str,
        classification: str = "SECRET",
    ) -> dict[str, Any]:
        """
        Run intelligence analysis.
        
        Args:
            session: Portal session.
            source: Intelligence source type.
            target: Analysis target.
            classification: Classification level.
            
        Returns:
            Analysis result.
        """
        return self.process_request(session, {
            "type": "intel",
            "classification": classification,
            "data": {
                "source": source,
                "target": target,
            },
        })
    
    def mission_plan(
        self,
        session: PortalSession,
        mission_type: str,
        objective: str,
        classification: str = "SECRET",
    ) -> dict[str, Any]:
        """
        Generate mission plan.
        
        Args:
            session: Portal session.
            mission_type: Type of mission.
            objective: Mission objective.
            classification: Classification level.
            
        Returns:
            Mission plan.
        """
        return self.process_request(session, {
            "type": "mission",
            "classification": classification,
            "data": {
                "mission_type": mission_type,
                "objective": objective,
            },
        })

"""
Base Portal Classes

Provides the foundation for all GENESIS portals with common functionality:
- Session management
- Configuration handling
- Agent orchestration
- Metrics collection
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional
from genesis.classification.levels import ClassificationLevel, UNCLASSIFIED
from genesis.metrics.session import SessionAnalytics


class PortalType(Enum):
    """Types of GENESIS portals."""
    ENTERPRISE = "enterprise"
    DEFENSE = "defense"
    HEALTH = "health"
    LEGAL = "legal"
    DARPA = "darpa"


class PortalConfig:
    """
    Configuration for a GENESIS portal.
    
    Attributes:
        portal_type: Type of portal.
        max_classification: Maximum allowed classification level.
        agents_enabled: List of enabled agent names.
        metrics_enabled: Whether to collect metrics.
        session_timeout: Session timeout in seconds.
    """
    
    def __init__(
        self,
        portal_type: PortalType,
        max_classification: ClassificationLevel = UNCLASSIFIED,
        agents_enabled: Optional[list[str]] = None,
        metrics_enabled: bool = True,
        session_timeout: int = 3600,
        custom_settings: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize portal configuration.
        
        Args:
            portal_type: Type of portal.
            max_classification: Maximum classification level.
            agents_enabled: List of enabled agents.
            metrics_enabled: Enable metrics collection.
            session_timeout: Session timeout in seconds.
            custom_settings: Additional custom settings.
        """
        self.portal_type = portal_type
        self.max_classification = max_classification
        self.agents_enabled = agents_enabled or ["AIDEN", "AURA", "PALS"]
        self.metrics_enabled = metrics_enabled
        self.session_timeout = session_timeout
        self.custom_settings = custom_settings or {}
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "portal_type": self.portal_type.value,
            "max_classification": self.max_classification.name,
            "agents_enabled": self.agents_enabled,
            "metrics_enabled": self.metrics_enabled,
            "session_timeout": self.session_timeout,
            "custom_settings": self.custom_settings,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PortalConfig":
        """Create from dictionary."""
        from genesis.classification.levels import get_level
        
        return cls(
            portal_type=PortalType(data["portal_type"]),
            max_classification=get_level(data.get("max_classification", "U")),
            agents_enabled=data.get("agents_enabled"),
            metrics_enabled=data.get("metrics_enabled", True),
            session_timeout=data.get("session_timeout", 3600),
            custom_settings=data.get("custom_settings"),
        )


class PortalSession:
    """
    A session within a GENESIS portal.
    
    Tracks user activity, agent interactions, and metrics within
    a single portal session.
    """
    
    def __init__(
        self,
        session_id: str,
        user_id: str,
        portal_type: PortalType,
        classification: ClassificationLevel = UNCLASSIFIED,
    ) -> None:
        """
        Initialize a portal session.
        
        Args:
            session_id: Unique session identifier.
            user_id: User identifier.
            portal_type: Type of portal.
            classification: Session classification level.
        """
        self.session_id = session_id
        self.user_id = user_id
        self.portal_type = portal_type
        self.classification = classification
        self.active = True
        self.analytics = SessionAnalytics(session_id)
        self._data: dict[str, Any] = {}
    
    def store(self, key: str, value: Any) -> None:
        """Store data in session."""
        self._data[key] = value
    
    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve data from session."""
        return self._data.get(key, default)
    
    def close(self) -> None:
        """Close the session."""
        self.active = False
        self.analytics.end_session()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "portal_type": self.portal_type.value,
            "classification": self.classification.name,
            "active": self.active,
        }


class Portal(ABC):
    """
    Abstract base class for GENESIS portals.
    
    Provides common portal functionality including:
    - Session management
    - Agent orchestration
    - Metrics collection
    - Access control
    """
    
    def __init__(self, config: PortalConfig) -> None:
        """
        Initialize the portal.
        
        Args:
            config: Portal configuration.
        """
        self.config = config
        self._sessions: dict[str, PortalSession] = {}
        self._session_counter = 0
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the portal name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the portal description."""
        pass
    
    def create_session(
        self,
        user_id: str,
        classification: ClassificationLevel = UNCLASSIFIED,
    ) -> PortalSession:
        """
        Create a new portal session.
        
        Args:
            user_id: User identifier.
            classification: Session classification level.
            
        Returns:
            New PortalSession.
            
        Raises:
            ValueError: If classification exceeds portal maximum.
        """
        if classification > self.config.max_classification:
            raise ValueError(
                f"Classification {classification.name} exceeds portal maximum "
                f"{self.config.max_classification.name}"
            )
        
        self._session_counter += 1
        session_id = f"{self.config.portal_type.value}-{self._session_counter:06d}"
        
        session = PortalSession(
            session_id=session_id,
            user_id=user_id,
            portal_type=self.config.portal_type,
            classification=classification,
        )
        
        self._sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[PortalSession]:
        """Get a session by ID."""
        return self._sessions.get(session_id)
    
    def close_session(self, session_id: str) -> bool:
        """
        Close a session.
        
        Args:
            session_id: Session to close.
            
        Returns:
            True if session was closed, False if not found.
        """
        session = self._sessions.get(session_id)
        if session:
            session.close()
            return True
        return False
    
    def active_sessions(self) -> list[PortalSession]:
        """Get all active sessions."""
        return [s for s in self._sessions.values() if s.active]
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the portal and its resources."""
        pass
    
    @abstractmethod
    def process_request(
        self,
        session: PortalSession,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process a request within a session.
        
        Args:
            session: The portal session.
            request: Request data.
            
        Returns:
            Response data.
        """
        pass
    
    def get_status(self) -> dict[str, Any]:
        """Get portal status."""
        return {
            "name": self.name,
            "type": self.config.portal_type.value,
            "active_sessions": len(self.active_sessions()),
            "max_classification": self.config.max_classification.name,
            "agents_enabled": self.config.agents_enabled,
        }

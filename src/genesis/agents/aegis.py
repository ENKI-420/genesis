"""
AEGIS - Autonomous Encrypted Guardian Intelligence System

The security agent responsible for access control, encryption,
classification enforcement, and threat detection.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from genesis.agents.base import Agent, AgentMessage
from genesis.constants import CHI_PC


class ThreatLevel(Enum):
    """Threat severity levels."""
    
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class SecurityEvent:
    """
    A security event detected by AEGIS.
    
    Attributes:
        event_type: Type of security event.
        threat_level: Assessed threat level.
        description: Event description.
        source: Event source.
        timestamp: When detected.
        metadata: Additional data.
    """
    event_type: str
    threat_level: ThreatLevel
    description: str
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessRequest:
    """
    An access request for validation.
    
    Attributes:
        subject: Who is requesting access.
        resource: What resource is being accessed.
        action: What action is being performed.
        classification: Classification level required.
        timestamp: When the request was made.
    """
    subject: str
    resource: str
    action: str
    classification: str = "UNCLASSIFIED"
    timestamp: datetime = field(default_factory=datetime.now)


class AEGIS(Agent):
    """
    AEGIS: Autonomous Encrypted Guardian Intelligence System
    
    Security agent responsible for:
    - Access control
    - Classification enforcement
    - Encryption management
    - Threat detection
    - Audit logging
    - Security policy enforcement
    
    Example:
        >>> aegis = AEGIS()
        >>> aegis.activate()
        >>> allowed = aegis.validate_access(user, resource, "read")
    """
    
    def __init__(self, name: str = "AEGIS") -> None:
        """Initialize AEGIS."""
        super().__init__(name)
        self._security_events: List[SecurityEvent] = []
        self._audit_log: List[Dict[str, Any]] = []
        self._access_rules: Dict[str, Set[str]] = {}
        self._classification_levels = [
            "UNCLASSIFIED",
            "CONFIDENTIAL",
            "SECRET",
            "TOP_SECRET",
            "TS_SCI",
            "SAP",
        ]
        self._clearances: Dict[str, str] = {}
    
    @property
    def description(self) -> str:
        return "Autonomous Encrypted Guardian Intelligence System - Security Agent"
    
    @property
    def capabilities(self) -> List[str]:
        return [
            "access_control",
            "classification_enforcement",
            "encryption_management",
            "threat_detection",
            "audit_logging",
            "policy_enforcement",
            "intrusion_detection",
        ]
    
    def handle_message(self, message: AgentMessage) -> Any:
        """Handle incoming messages."""
        content = message.content
        
        if isinstance(content, dict):
            action = content.get("action")
            
            if action == "validate_access":
                return self.validate_access(
                    content.get("subject"),
                    content.get("resource"),
                    content.get("action_type", "read")
                )
            elif action == "report_threat":
                return self.report_threat(
                    content.get("threat_type"),
                    content.get("source"),
                    content.get("severity", "LOW")
                )
            elif action == "audit":
                return self.get_audit_log(content.get("limit", 100))
        
        return {"status": "unknown_action"}
    
    def step(self) -> None:
        """Perform one security check step."""
        self.process_inbox()
        self._scan_for_threats()
    
    def validate_access(
        self,
        subject: str,
        resource: str,
        action_type: str = "read"
    ) -> Dict[str, Any]:
        """
        Validate an access request.
        
        Args:
            subject: Who is requesting access.
            resource: What resource is being accessed.
            action_type: Type of action (read, write, execute).
            
        Returns:
            Access validation result.
        """
        if subject is None or resource is None:
            return {"allowed": False, "reason": "Invalid request"}
        
        request = AccessRequest(
            subject=subject,
            resource=resource,
            action=action_type
        )
        
        # Check clearance level
        subject_clearance = self._clearances.get(subject, "UNCLASSIFIED")
        resource_classification = self._get_resource_classification(resource)
        
        clearance_valid = self._validate_clearance(
            subject_clearance, 
            resource_classification
        )
        
        # Check access rules
        rules_allow = self._check_access_rules(subject, resource, action_type)
        
        allowed = clearance_valid and rules_allow
        
        # Log the access attempt
        self._log_audit(
            "access_attempt",
            {
                "subject": subject,
                "resource": resource,
                "action": action_type,
                "allowed": allowed,
                "clearance": subject_clearance,
                "classification": resource_classification,
            }
        )
        
        if not allowed:
            self._record_security_event(
                "access_denied",
                ThreatLevel.LOW,
                f"Access denied: {subject} -> {resource}",
                subject
            )
        
        self.metrics.tasks_completed += 1
        
        return {
            "allowed": allowed,
            "subject": subject,
            "resource": resource,
            "action": action_type,
            "clearance_valid": clearance_valid,
            "rules_allow": rules_allow,
        }
    
    def _validate_clearance(
        self,
        subject_clearance: str,
        resource_classification: str
    ) -> bool:
        """Check if clearance level is sufficient."""
        try:
            subject_level = self._classification_levels.index(subject_clearance)
            resource_level = self._classification_levels.index(resource_classification)
            return subject_level >= resource_level
        except ValueError:
            return False
    
    def _get_resource_classification(self, resource: str) -> str:
        """Get classification level of a resource."""
        # Default to UNCLASSIFIED
        return "UNCLASSIFIED"
    
    def _check_access_rules(
        self,
        subject: str,
        resource: str,
        action: str
    ) -> bool:
        """Check if access rules allow the action."""
        # Default: allow all
        if resource in self._access_rules:
            allowed_subjects = self._access_rules[resource]
            return subject in allowed_subjects
        return True
    
    def set_clearance(self, subject: str, level: str) -> bool:
        """
        Set clearance level for a subject.
        
        Args:
            subject: Subject identifier.
            level: Clearance level.
            
        Returns:
            Success status.
        """
        if level not in self._classification_levels:
            return False
        
        self._clearances[subject] = level
        self._log_audit("clearance_set", {"subject": subject, "level": level})
        return True
    
    def set_access_rule(
        self,
        resource: str,
        allowed_subjects: Set[str]
    ) -> None:
        """
        Set access rule for a resource.
        
        Args:
            resource: Resource identifier.
            allowed_subjects: Set of allowed subject identifiers.
        """
        self._access_rules[resource] = allowed_subjects
        self._log_audit(
            "access_rule_set",
            {"resource": resource, "allowed": list(allowed_subjects)}
        )
    
    def report_threat(
        self,
        threat_type: str,
        source: str,
        severity: str = "LOW"
    ) -> Dict[str, Any]:
        """
        Report a security threat.
        
        Args:
            threat_type: Type of threat.
            source: Threat source.
            severity: Threat severity.
            
        Returns:
            Threat report.
        """
        threat_level = ThreatLevel[severity.upper()]
        
        event = self._record_security_event(
            threat_type,
            threat_level,
            f"Threat reported: {threat_type}",
            source
        )
        
        # Send alerts for high-severity threats
        if threat_level in (ThreatLevel.HIGH, ThreatLevel.CRITICAL):
            self.send(
                "PALS",
                {
                    "action": "alert",
                    "type": threat_type,
                    "severity": severity,
                    "source": source,
                },
                priority=10
            )
        
        return {
            "reported": True,
            "threat_type": threat_type,
            "severity": severity,
            "event_id": len(self._security_events),
        }
    
    def _record_security_event(
        self,
        event_type: str,
        threat_level: ThreatLevel,
        description: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SecurityEvent:
        """Record a security event."""
        event = SecurityEvent(
            event_type=event_type,
            threat_level=threat_level,
            description=description,
            source=source,
            metadata=metadata or {}
        )
        self._security_events.append(event)
        return event
    
    def _scan_for_threats(self) -> None:
        """Scan for potential threats."""
        # Placeholder for threat detection logic
        pass
    
    def _log_audit(
        self,
        action: str,
        details: Dict[str, Any]
    ) -> None:
        """Log an audit entry."""
        entry = {
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
        }
        self._audit_log.append(entry)
    
    def get_audit_log(
        self,
        limit: int = 100,
        action_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get audit log entries.
        
        Args:
            limit: Maximum entries to return.
            action_filter: Filter by action type.
            
        Returns:
            List of audit entries.
        """
        entries = self._audit_log
        if action_filter:
            entries = [e for e in entries if e["action"] == action_filter]
        
        return entries[-limit:]
    
    def get_security_events(
        self,
        limit: int = 100,
        min_severity: ThreatLevel = ThreatLevel.NONE
    ) -> List[Dict[str, Any]]:
        """
        Get security events.
        
        Args:
            limit: Maximum events to return.
            min_severity: Minimum severity to include.
            
        Returns:
            List of security events.
        """
        events = [
            e for e in self._security_events
            if e.threat_level.value >= min_severity.value
        ]
        
        return [
            {
                "event_type": e.event_type,
                "threat_level": e.threat_level.name,
                "description": e.description,
                "source": e.source,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in events[-limit:]
        ]
    
    def compute_fidelity(self) -> float:
        """
        Compute phase conjugate fidelity for security operations.
        
        Returns:
            Current security fidelity.
        """
        # Based on CHI_PC constant
        total_events = len(self._security_events)
        if total_events == 0:
            return CHI_PC
        
        high_severity = sum(
            1 for e in self._security_events
            if e.threat_level.value >= ThreatLevel.HIGH.value
        )
        
        return CHI_PC * (1 - high_severity / total_events)

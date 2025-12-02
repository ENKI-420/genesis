"""
Session Analytics

Provides analytics for tracking GENESIS platform sessions,
including performance metrics, resource usage, and evolution tracking.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from genesis.metrics.ccce import CCCEMetric
from genesis.metrics.consciousness import ConsciousnessTracker


@dataclass
class SessionEvent:
    """
    An event within a session.
    
    Attributes:
        event_type: Type of event.
        timestamp: When the event occurred.
        data: Event data.
    """
    event_type: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)


class SessionAnalytics:
    """
    Analytics for a GENESIS platform session.
    
    Tracks session duration, events, CCCE metrics, and provides
    summary analytics for monitoring system performance.
    
    Example:
        >>> session = SessionAnalytics()
        >>> session.start()
        >>> session.record_event("evolution_start", {"generations": 100})
        >>> session.end()
        >>> print(session.summary())
    """
    
    def __init__(self, session_id: Optional[str] = None) -> None:
        """
        Initialize session analytics.
        
        Args:
            session_id: Optional session identifier.
        """
        self.session_id = session_id or self._generate_id()
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self._events: List[SessionEvent] = []
        self._metrics = {
            "ccce": CCCEMetric(),
            "consciousness": ConsciousnessTracker(),
        }
        self._counters: Dict[str, int] = {}
        self._timers: Dict[str, float] = {}
    
    def _generate_id(self) -> str:
        """Generate a session ID."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def start(self) -> None:
        """Start the session."""
        self.start_time = datetime.now()
        self.record_event("session_start")
    
    def end(self) -> None:
        """End the session."""
        self.end_time = datetime.now()
        self.record_event("session_end")
    
    @property
    def duration(self) -> Optional[timedelta]:
        """Get session duration."""
        if self.start_time is None:
            return None
        end = self.end_time or datetime.now()
        return end - self.start_time
    
    @property
    def is_active(self) -> bool:
        """Check if session is active."""
        return self.start_time is not None and self.end_time is None
    
    def record_event(
        self,
        event_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> SessionEvent:
        """
        Record a session event.
        
        Args:
            event_type: Type of event.
            data: Event data.
            
        Returns:
            The recorded event.
        """
        event = SessionEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            data=data or {}
        )
        self._events.append(event)
        
        # Update counters
        self._counters[event_type] = self._counters.get(event_type, 0) + 1
        
        return event
    
    def increment(self, counter: str, amount: int = 1) -> int:
        """
        Increment a counter.
        
        Args:
            counter: Counter name.
            amount: Amount to increment.
            
        Returns:
            New counter value.
        """
        self._counters[counter] = self._counters.get(counter, 0) + amount
        return self._counters[counter]
    
    def get_counter(self, counter: str) -> int:
        """Get counter value."""
        return self._counters.get(counter, 0)
    
    def start_timer(self, name: str) -> None:
        """Start a timer."""
        self._timers[f"{name}_start"] = datetime.now().timestamp()
    
    def stop_timer(self, name: str) -> float:
        """
        Stop a timer.
        
        Args:
            name: Timer name.
            
        Returns:
            Elapsed time in seconds.
        """
        start_key = f"{name}_start"
        if start_key not in self._timers:
            return 0.0
        
        start_time = self._timers[start_key]
        elapsed = datetime.now().timestamp() - start_time
        self._timers[name] = self._timers.get(name, 0) + elapsed
        del self._timers[start_key]
        
        return elapsed
    
    def get_timer(self, name: str) -> float:
        """Get total timer value."""
        return self._timers.get(name, 0.0)
    
    def update_ccce(
        self,
        consciousness: float,
        coherence: float,
        decoherence: float
    ) -> None:
        """
        Update CCCE metrics.
        
        Args:
            consciousness: Consciousness level.
            coherence: Coherence factor.
            decoherence: Decoherence rate.
        """
        self._metrics["ccce"].update(
            consciousness=consciousness,
            coherence=coherence,
            decoherence=decoherence
        )
    
    def update_consciousness(
        self,
        value: float,
        generation: int
    ) -> None:
        """
        Update consciousness tracking.
        
        Args:
            value: Consciousness level.
            generation: Current generation.
        """
        self._metrics["consciousness"].record(value, generation)
    
    def get_events(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get session events.
        
        Args:
            event_type: Filter by type.
            limit: Maximum events.
            
        Returns:
            List of events.
        """
        events = self._events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return [
            {
                "type": e.event_type,
                "timestamp": e.timestamp.isoformat(),
                "data": e.data,
            }
            for e in events[-limit:]
        ]
    
    def summary(self) -> Dict[str, Any]:
        """
        Get session summary.
        
        Returns:
            Summary statistics.
        """
        duration = self.duration
        duration_seconds = duration.total_seconds() if duration else 0
        
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": duration_seconds,
            "is_active": self.is_active,
            "total_events": len(self._events),
            "event_counts": self._counters.copy(),
            "timers": {k: v for k, v in self._timers.items() if not k.endswith("_start")},
            "ccce": self._metrics["ccce"].summary(),
            "consciousness": self._metrics["consciousness"].statistics(),
        }
    
    def performance_report(self) -> Dict[str, Any]:
        """
        Get performance report.
        
        Returns:
            Performance metrics.
        """
        duration = self.duration
        duration_seconds = duration.total_seconds() if duration else 1
        
        # Calculate rates
        total_events = len(self._events)
        events_per_second = total_events / duration_seconds
        
        generations = self.get_counter("generation")
        generations_per_second = generations / duration_seconds if generations else 0
        
        return {
            "session_id": self.session_id,
            "duration_seconds": duration_seconds,
            "total_events": total_events,
            "events_per_second": events_per_second,
            "generations": generations,
            "generations_per_second": generations_per_second,
            "timers": {k: v for k, v in self._timers.items() if not k.endswith("_start")},
        }
    
    def reset(self) -> None:
        """Reset session analytics."""
        self.start_time = None
        self.end_time = None
        self._events.clear()
        self._counters.clear()
        self._timers.clear()
        self._metrics["ccce"].reset()
        self._metrics["consciousness"].reset()

"""
CHRONOS - Contextual Holistic Resource Orchestration Network for Optimal Sequencing

The temporal agent responsible for time management, scheduling,
and temporal pattern analysis.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from genesis.agents.base import Agent, AgentMessage
from genesis.constants import LAMBDA_PHI, MEMORY_KERNEL_TAU_0


@dataclass
class TemporalEvent:
    """
    A temporal event tracked by CHRONOS.
    
    Attributes:
        name: Event name.
        timestamp: When the event occurred.
        duration: Event duration.
        data: Associated data.
    """
    name: str
    timestamp: datetime
    duration: Optional[float] = None
    data: Dict[str, Any] = field(default_factory=dict)


class CHRONOS(Agent):
    """
    CHRONOS: Contextual Holistic Resource Orchestration Network
              for Optimal Sequencing
    
    Temporal agent responsible for:
    - Time management
    - Scheduling
    - Temporal pattern analysis
    - Memory decay modeling
    - Evolution timeline tracking
    
    Example:
        >>> chronos = CHRONOS()
        >>> chronos.activate()
        >>> schedule = chronos.schedule_evolution(organisms, 100)
    """
    
    def __init__(self, name: str = "CHRONOS") -> None:
        """Initialize CHRONOS."""
        super().__init__(name)
        self._timeline: List[TemporalEvent] = []
        self._scheduled_tasks: List[Dict[str, Any]] = []
        self._temporal_patterns: Dict[str, List[float]] = {}
    
    @property
    def description(self) -> str:
        return "Contextual Holistic Resource Orchestration Network for Optimal Sequencing - Temporal Agent"
    
    @property
    def capabilities(self) -> List[str]:
        return [
            "time_management",
            "scheduling",
            "temporal_pattern_analysis",
            "memory_decay_modeling",
            "timeline_tracking",
            "sequence_optimization",
            "periodic_analysis",
        ]
    
    def handle_message(self, message: AgentMessage) -> Any:
        """Handle incoming messages."""
        content = message.content
        
        if isinstance(content, dict):
            action = content.get("action")
            
            if action == "record_event":
                return self.record_event(
                    content.get("name", "unnamed"),
                    content.get("data", {})
                )
            elif action == "analyze_timeline":
                return self.analyze_timeline()
            elif action == "schedule":
                return self.schedule_task(
                    content.get("task"),
                    content.get("delay", 0)
                )
        
        return {"status": "unknown_action"}
    
    def step(self) -> None:
        """Perform one temporal step."""
        self.process_inbox()
        self._process_scheduled_tasks()
    
    def record_event(
        self,
        name: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record a temporal event.
        
        Args:
            name: Event name.
            data: Associated data.
            
        Returns:
            Recorded event info.
        """
        event = TemporalEvent(
            name=name,
            timestamp=datetime.now(),
            data=data or {}
        )
        self._timeline.append(event)
        
        # Track pattern
        if name not in self._temporal_patterns:
            self._temporal_patterns[name] = []
        self._temporal_patterns[name].append(event.timestamp.timestamp())
        
        return {
            "event": name,
            "timestamp": event.timestamp.isoformat(),
            "timeline_length": len(self._timeline),
        }
    
    def analyze_timeline(self) -> Dict[str, Any]:
        """
        Analyze the temporal timeline.
        
        Returns:
            Timeline analysis.
        """
        if not self._timeline:
            return {"error": "Empty timeline"}
        
        # Calculate statistics
        total_events = len(self._timeline)
        
        # Time span
        first_event = min(self._timeline, key=lambda e: e.timestamp)
        last_event = max(self._timeline, key=lambda e: e.timestamp)
        time_span = (last_event.timestamp - first_event.timestamp).total_seconds()
        
        # Event frequency
        event_counts = {}
        for event in self._timeline:
            event_counts[event.name] = event_counts.get(event.name, 0) + 1
        
        # Calculate inter-event intervals
        if len(self._timeline) > 1:
            sorted_timeline = sorted(self._timeline, key=lambda e: e.timestamp)
            intervals = []
            for i in range(1, len(sorted_timeline)):
                interval = (sorted_timeline[i].timestamp - 
                           sorted_timeline[i-1].timestamp).total_seconds()
                intervals.append(interval)
            avg_interval = sum(intervals) / len(intervals)
        else:
            avg_interval = 0
        
        self.metrics.tasks_completed += 1
        
        return {
            "total_events": total_events,
            "time_span_seconds": time_span,
            "event_counts": event_counts,
            "avg_interval": avg_interval,
            "first_event": first_event.timestamp.isoformat(),
            "last_event": last_event.timestamp.isoformat(),
        }
    
    def schedule_task(
        self,
        task: Callable[[], Any],
        delay: float = 0
    ) -> Dict[str, Any]:
        """
        Schedule a task for future execution.
        
        Args:
            task: Task to execute.
            delay: Delay in seconds.
            
        Returns:
            Schedule info.
        """
        if task is None:
            return {"error": "No task provided"}
        
        execute_at = datetime.now() + timedelta(seconds=delay)
        
        task_info = {
            "task": task,
            "execute_at": execute_at,
            "scheduled_at": datetime.now(),
        }
        self._scheduled_tasks.append(task_info)
        
        return {
            "scheduled": True,
            "execute_at": execute_at.isoformat(),
            "delay": delay,
        }
    
    def _process_scheduled_tasks(self) -> None:
        """Process scheduled tasks that are due."""
        now = datetime.now()
        remaining = []
        
        for task_info in self._scheduled_tasks:
            if task_info["execute_at"] <= now:
                try:
                    task_info["task"]()
                    self.metrics.tasks_completed += 1
                except Exception:
                    self.metrics.errors += 1
            else:
                remaining.append(task_info)
        
        self._scheduled_tasks = remaining
    
    def compute_memory_decay(
        self,
        tau: float,
        tau_prime: float
    ) -> float:
        """
        Compute memory kernel decay K(τ, τ').
        
        The memory kernel determines how strongly past states
        influence the current state.
        
        Args:
            tau: Current time.
            tau_prime: Past time.
            
        Returns:
            Memory kernel value.
        """
        import genesis.core.math as gmath
        
        delta_tau = abs(tau - tau_prime)
        
        # K(τ,τ') = exp(-Λ_Φ × |τ-τ'|²)
        exponent = -LAMBDA_PHI * (delta_tau ** 2)
        return gmath.exp(exponent)
    
    def analyze_periodicity(
        self,
        event_name: str
    ) -> Dict[str, Any]:
        """
        Analyze periodicity of a specific event type.
        
        Args:
            event_name: Name of event to analyze.
            
        Returns:
            Periodicity analysis.
        """
        timestamps = self._temporal_patterns.get(event_name, [])
        
        if len(timestamps) < 2:
            return {"error": "Need at least 2 events"}
        
        # Calculate intervals
        intervals = []
        for i in range(1, len(timestamps)):
            intervals.append(timestamps[i] - timestamps[i-1])
        
        avg_interval = sum(intervals) / len(intervals)
        
        # Check for periodicity (low variance in intervals)
        variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        is_periodic = std_dev / (avg_interval + 1e-10) < 0.1
        
        return {
            "event_name": event_name,
            "count": len(timestamps),
            "avg_interval": avg_interval,
            "std_dev": std_dev,
            "is_periodic": is_periodic,
            "estimated_period": avg_interval if is_periodic else None,
        }
    
    def get_tau_0(self) -> float:
        """Get the characteristic memory time scale."""
        return MEMORY_KERNEL_TAU_0
    
    def get_timeline(
        self,
        limit: int = 100,
        event_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get timeline events.
        
        Args:
            limit: Maximum events to return.
            event_name: Filter by event name.
            
        Returns:
            List of events.
        """
        events = self._timeline
        if event_name:
            events = [e for e in events if e.name == event_name]
        
        # Sort by timestamp descending
        events = sorted(events, key=lambda e: e.timestamp, reverse=True)[:limit]
        
        return [
            {
                "name": e.name,
                "timestamp": e.timestamp.isoformat(),
                "data": e.data,
            }
            for e in events
        ]

"""
Base Agent Implementation

Provides the base agent class and common infrastructure for
the GENESIS multi-agent system.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime


class AgentState(Enum):
    """Agent operational states."""
    
    IDLE = auto()
    ACTIVE = auto()
    PROCESSING = auto()
    WAITING = auto()
    ERROR = auto()
    TERMINATED = auto()


@dataclass
class AgentMessage:
    """
    Message passed between agents.
    
    Attributes:
        sender: Name of sending agent.
        recipient: Name of receiving agent.
        content: Message content.
        priority: Message priority (0-10).
        timestamp: When the message was created.
        metadata: Additional metadata.
    """
    sender: str
    recipient: str
    content: Any
    priority: int = 5
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self) -> str:
        return f"AgentMessage({self.sender} -> {self.recipient}: {type(self.content).__name__})"


@dataclass
class AgentMetrics:
    """
    Agent performance metrics.
    
    Attributes:
        messages_sent: Total messages sent.
        messages_received: Total messages received.
        tasks_completed: Number of tasks completed.
        errors: Number of errors encountered.
        uptime: Time since activation.
    """
    messages_sent: int = 0
    messages_received: int = 0
    tasks_completed: int = 0
    errors: int = 0
    uptime: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "tasks_completed": self.tasks_completed,
            "errors": self.errors,
            "uptime": self.uptime,
        }


class Agent(ABC):
    """
    Base class for all GENESIS agents.
    
    Agents are autonomous entities that can process messages,
    perform tasks, and communicate with other agents.
    
    Attributes:
        name: Agent identifier.
        state: Current operational state.
        metrics: Performance metrics.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize the agent.
        
        Args:
            name: Agent identifier.
        """
        self.name = name
        self.state = AgentState.IDLE
        self.metrics = AgentMetrics()
        self._inbox: List[AgentMessage] = []
        self._outbox: List[AgentMessage] = []
        self._handlers: Dict[str, Callable[..., Any]] = {}
        self._activated_at: Optional[datetime] = None
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Agent description."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """List of agent capabilities."""
        pass
    
    def activate(self) -> None:
        """Activate the agent."""
        self.state = AgentState.ACTIVE
        self._activated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.state = AgentState.IDLE
        self._update_uptime()
    
    def terminate(self) -> None:
        """Terminate the agent."""
        self.state = AgentState.TERMINATED
        self._update_uptime()
    
    def _update_uptime(self) -> None:
        """Update uptime metric."""
        if self._activated_at:
            delta = datetime.now() - self._activated_at
            self.metrics.uptime += delta.total_seconds()
    
    def receive(self, message: AgentMessage) -> None:
        """
        Receive a message.
        
        Args:
            message: The message to receive.
        """
        self._inbox.append(message)
        self.metrics.messages_received += 1
    
    def send(
        self,
        recipient: str,
        content: Any,
        priority: int = 5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentMessage:
        """
        Send a message to another agent.
        
        Args:
            recipient: Name of receiving agent.
            content: Message content.
            priority: Message priority.
            metadata: Additional metadata.
            
        Returns:
            The created message.
        """
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            content=content,
            priority=priority,
            metadata=metadata or {}
        )
        self._outbox.append(message)
        self.metrics.messages_sent += 1
        return message
    
    def get_outgoing_messages(self) -> List[AgentMessage]:
        """Get and clear outgoing messages."""
        messages = self._outbox.copy()
        self._outbox.clear()
        return messages
    
    def process_inbox(self) -> List[Any]:
        """
        Process all messages in the inbox.
        
        Returns:
            List of results from processing.
        """
        results = []
        self.state = AgentState.PROCESSING
        
        # Sort by priority (higher first)
        self._inbox.sort(key=lambda m: m.priority, reverse=True)
        
        for message in self._inbox:
            try:
                result = self.handle_message(message)
                results.append(result)
            except Exception as e:
                self.metrics.errors += 1
                results.append({"error": str(e)})
        
        self._inbox.clear()
        self.state = AgentState.ACTIVE
        return results
    
    @abstractmethod
    def handle_message(self, message: AgentMessage) -> Any:
        """
        Handle a single message.
        
        Args:
            message: The message to handle.
            
        Returns:
            Result of handling the message.
        """
        pass
    
    @abstractmethod
    def step(self) -> None:
        """Perform one step of agent processing."""
        pass
    
    def register_handler(self, message_type: str, handler: Callable[..., Any]) -> None:
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: Type of message to handle.
            handler: Handler function.
        """
        self._handlers[message_type] = handler
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "name": self.name,
            "state": self.state.name,
            "metrics": self.metrics.to_dict(),
            "inbox_size": len(self._inbox),
            "outbox_size": len(self._outbox),
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.state.name})"


class AgentSwarm:
    """
    A collection of agents that can communicate with each other.
    """
    
    def __init__(self) -> None:
        """Initialize the swarm."""
        self.agents: Dict[str, Agent] = {}
    
    def add(self, agent: Agent) -> None:
        """Add an agent to the swarm."""
        self.agents[agent.name] = agent
    
    def remove(self, name: str) -> Optional[Agent]:
        """Remove an agent from the swarm."""
        return self.agents.pop(name, None)
    
    def get(self, name: str) -> Optional[Agent]:
        """Get an agent by name."""
        return self.agents.get(name)
    
    def broadcast(self, sender: str, content: Any, priority: int = 5) -> None:
        """
        Broadcast a message to all agents.
        
        Args:
            sender: Sending agent name.
            content: Message content.
            priority: Message priority.
        """
        for name, agent in self.agents.items():
            if name != sender:
                message = AgentMessage(
                    sender=sender,
                    recipient=name,
                    content=content,
                    priority=priority
                )
                agent.receive(message)
    
    def route_messages(self) -> int:
        """
        Route messages between agents.
        
        Returns:
            Number of messages routed.
        """
        count = 0
        
        for agent in self.agents.values():
            messages = agent.get_outgoing_messages()
            for message in messages:
                recipient = self.agents.get(message.recipient)
                if recipient:
                    recipient.receive(message)
                    count += 1
        
        return count
    
    def step_all(self) -> None:
        """Run one step for all agents."""
        for agent in self.agents.values():
            if agent.state == AgentState.ACTIVE:
                agent.step()
        self.route_messages()
    
    def activate_all(self) -> None:
        """Activate all agents."""
        for agent in self.agents.values():
            agent.activate()
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "agents": {name: agent.get_status() for name, agent in self.agents.items()},
            "total_agents": len(self.agents),
        }

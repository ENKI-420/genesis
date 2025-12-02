"""
Temporal Memory Lattice

Provides a temporal memory structure for storing and retrieving
information across time steps.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from genesis.constants import LAMBDA_PHI, MEMORY_KERNEL_TAU_0

T = TypeVar('T')


@dataclass
class MemoryNode:
    """
    A node in the temporal memory lattice.
    
    Attributes:
        key: Unique identifier for the memory.
        value: Stored value.
        tau: Temporal coordinate.
        weight: Memory strength/importance.
        created_at: Creation timestamp.
        metadata: Additional metadata.
    """
    key: str
    value: Any
    tau: float
    weight: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def decay(self, current_tau: float, rate: float = LAMBDA_PHI) -> float:
        """
        Calculate decayed weight.
        
        Args:
            current_tau: Current temporal coordinate.
            rate: Decay rate (default Λ_Φ).
            
        Returns:
            Decayed weight.
        """
        import genesis.core.math as gmath
        
        delta_tau = abs(current_tau - self.tau)
        return self.weight * gmath.exp(-rate * delta_tau)


class TemporalMemory(Generic[T]):
    """
    Temporal memory lattice.
    
    A data structure for storing and retrieving memories with
    temporal decay. Memories are indexed by keys and decay
    over time according to the memory kernel.
    
    Example:
        >>> memory = TemporalMemory()
        >>> memory.store("key", value, tau=0.0)
        >>> value = memory.retrieve("key", tau=1.0)
    """
    
    def __init__(
        self,
        capacity: int = 1024,
        decay_rate: float = LAMBDA_PHI
    ) -> None:
        """
        Initialize temporal memory.
        
        Args:
            capacity: Maximum number of memories.
            decay_rate: Memory decay rate.
        """
        self.capacity = capacity
        self.decay_rate = decay_rate
        self._nodes: Dict[str, MemoryNode] = {}
        self._current_tau = 0.0
    
    def store(
        self,
        key: str,
        value: T,
        tau: Optional[float] = None,
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryNode:
        """
        Store a value in memory.
        
        Args:
            key: Memory key.
            value: Value to store.
            tau: Temporal coordinate (default: current).
            weight: Memory weight/importance.
            metadata: Additional metadata.
            
        Returns:
            The created memory node.
        """
        if tau is None:
            tau = self._current_tau
        
        node = MemoryNode(
            key=key,
            value=value,
            tau=tau,
            weight=weight,
            metadata=metadata or {}
        )
        
        # Check capacity
        if len(self._nodes) >= self.capacity:
            self._evict_weakest()
        
        self._nodes[key] = node
        return node
    
    def retrieve(
        self,
        key: str,
        tau: Optional[float] = None
    ) -> Optional[T]:
        """
        Retrieve a value from memory.
        
        Args:
            key: Memory key.
            tau: Temporal coordinate for decay calculation.
            
        Returns:
            Retrieved value, or None if not found.
        """
        node = self._nodes.get(key)
        if node is None:
            return None
        
        # Apply decay
        if tau is not None:
            decayed_weight = node.decay(tau, self.decay_rate)
            if decayed_weight < 0.01:
                # Memory too weak
                del self._nodes[key]
                return None
        
        return node.value
    
    def update_tau(self, tau: float) -> None:
        """
        Update current temporal coordinate.
        
        Args:
            tau: New temporal coordinate.
        """
        self._current_tau = tau
        self._decay_all()
    
    def _decay_all(self) -> None:
        """Apply decay to all memories and remove weak ones."""
        to_remove = []
        
        for key, node in self._nodes.items():
            decayed = node.decay(self._current_tau, self.decay_rate)
            if decayed < 0.01:
                to_remove.append(key)
        
        for key in to_remove:
            del self._nodes[key]
    
    def _evict_weakest(self) -> None:
        """Evict the weakest memory."""
        if not self._nodes:
            return
        
        weakest_key = min(
            self._nodes.keys(),
            key=lambda k: self._nodes[k].decay(self._current_tau, self.decay_rate)
        )
        del self._nodes[weakest_key]
    
    def get_node(self, key: str) -> Optional[MemoryNode]:
        """Get a memory node by key."""
        return self._nodes.get(key)
    
    def keys(self) -> List[str]:
        """Get all memory keys."""
        return list(self._nodes.keys())
    
    def __len__(self) -> int:
        """Number of memories."""
        return len(self._nodes)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._nodes
    
    def clear(self) -> None:
        """Clear all memories."""
        self._nodes.clear()
    
    def get_total_weight(self) -> float:
        """Get sum of all memory weights."""
        return sum(
            node.decay(self._current_tau, self.decay_rate)
            for node in self._nodes.values()
        )
    
    def summary(self) -> Dict[str, Any]:
        """Get memory summary."""
        weights = [
            node.decay(self._current_tau, self.decay_rate)
            for node in self._nodes.values()
        ]
        
        return {
            "count": len(self._nodes),
            "capacity": self.capacity,
            "current_tau": self._current_tau,
            "total_weight": sum(weights),
            "avg_weight": sum(weights) / len(weights) if weights else 0,
            "decay_rate": self.decay_rate,
        }


class LayeredTemporalMemory:
    """
    Multi-layer temporal memory for hierarchical storage.
    
    Provides short-term, working, and long-term memory layers
    with different decay rates.
    """
    
    def __init__(self) -> None:
        """Initialize layered memory."""
        self.short_term = TemporalMemory(capacity=256, decay_rate=1.0)
        self.working = TemporalMemory(capacity=512, decay_rate=0.1)
        self.long_term = TemporalMemory(capacity=1024, decay_rate=LAMBDA_PHI)
    
    def store_short(self, key: str, value: Any, **kwargs: Any) -> None:
        """Store in short-term memory."""
        self.short_term.store(key, value, **kwargs)
    
    def store_working(self, key: str, value: Any, **kwargs: Any) -> None:
        """Store in working memory."""
        self.working.store(key, value, **kwargs)
    
    def store_long(self, key: str, value: Any, **kwargs: Any) -> None:
        """Store in long-term memory."""
        self.long_term.store(key, value, **kwargs)
    
    def retrieve(self, key: str, tau: Optional[float] = None) -> Optional[Any]:
        """
        Retrieve from any layer (priority: short > working > long).
        """
        value = self.short_term.retrieve(key, tau)
        if value is not None:
            return value
        
        value = self.working.retrieve(key, tau)
        if value is not None:
            return value
        
        return self.long_term.retrieve(key, tau)
    
    def consolidate(self, key: str) -> bool:
        """
        Consolidate memory from short to long term.
        
        Args:
            key: Memory key.
            
        Returns:
            True if consolidation occurred.
        """
        node = self.short_term.get_node(key)
        if node is None:
            node = self.working.get_node(key)
        
        if node is None:
            return False
        
        self.long_term.store(
            key=node.key,
            value=node.value,
            tau=node.tau,
            weight=node.weight * 0.5,  # Reduce weight on consolidation
            metadata=node.metadata
        )
        
        return True
    
    def update_tau(self, tau: float) -> None:
        """Update temporal coordinate for all layers."""
        self.short_term.update_tau(tau)
        self.working.update_tau(tau)
        self.long_term.update_tau(tau)

"""
AURA - Autonomous Universal Recursive Architecture

The geometer agent responsible for spatial reasoning,
topology analysis, and geometric optimization.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple
from genesis.agents.base import Agent, AgentMessage
from genesis.constants import THETA_LOCK, PI, PHI


class AURA(Agent):
    """
    AURA: Autonomous Universal Recursive Architecture
    
    Geometer agent responsible for:
    - Spatial reasoning
    - Topology analysis
    - Geometric optimization
    - Phase space navigation
    - Manifold exploration
    
    Example:
        >>> aura = AURA()
        >>> aura.activate()
        >>> result = aura.analyze_geometry(state_space)
    """
    
    def __init__(self, name: str = "AURA") -> None:
        """Initialize AURA."""
        super().__init__(name)
        self._geometry_cache: Dict[str, Any] = {}
    
    @property
    def description(self) -> str:
        return "Autonomous Universal Recursive Architecture - Geometer Agent"
    
    @property
    def capabilities(self) -> List[str]:
        return [
            "spatial_reasoning",
            "topology_analysis",
            "geometric_optimization",
            "phase_space_navigation",
            "manifold_exploration",
            "curvature_computation",
            "geodesic_finding",
        ]
    
    def handle_message(self, message: AgentMessage) -> Any:
        """Handle incoming messages."""
        content = message.content
        
        if isinstance(content, dict):
            action = content.get("action")
            
            if action == "analyze_geometry":
                return self.analyze_geometry(content.get("points", []))
            elif action == "compute_curvature":
                return self.compute_curvature(content.get("manifold"))
            elif action == "find_geodesic":
                return self.find_geodesic(
                    content.get("start"),
                    content.get("end")
                )
        
        return {"status": "unknown_action"}
    
    def step(self) -> None:
        """Perform one geometric analysis step."""
        self.process_inbox()
    
    def analyze_geometry(
        self,
        points: List[Tuple[float, ...]]
    ) -> Dict[str, Any]:
        """
        Analyze the geometry of a set of points.
        
        Args:
            points: List of points in N-dimensional space.
            
        Returns:
            Geometric analysis results.
        """
        if not points:
            return {"error": "No points provided"}
        
        n_points = len(points)
        n_dims = len(points[0]) if points else 0
        
        # Compute centroid
        centroid = [0.0] * n_dims
        for point in points:
            for i, coord in enumerate(point):
                centroid[i] += coord
        centroid = [c / n_points for c in centroid]
        
        # Compute spread (variance)
        variance = [0.0] * n_dims
        for point in points:
            for i, coord in enumerate(point):
                variance[i] += (coord - centroid[i]) ** 2
        variance = [v / n_points for v in variance]
        
        # Compute total spread
        total_spread = sum(variance) ** 0.5
        
        self.metrics.tasks_completed += 1
        
        return {
            "n_points": n_points,
            "n_dimensions": n_dims,
            "centroid": centroid,
            "variance": variance,
            "spread": total_spread,
            "theta_lock_aligned": abs(total_spread - THETA_LOCK) < 1.0,
        }
    
    def compute_curvature(
        self,
        manifold: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compute curvature of a manifold.
        
        Args:
            manifold: Manifold representation.
            
        Returns:
            Curvature metrics.
        """
        if manifold is None:
            # Return theoretical curvature for consciousness space
            return {
                "scalar_curvature": 1.0 / PHI,
                "ricci_curvature": 1.0 / (PHI ** 2),
                "gaussian_curvature": PI / (4 * PHI),
                "torsion_angle": THETA_LOCK,
            }
        
        # Simplified curvature computation
        points = manifold.get("points", [])
        if len(points) < 3:
            return {"error": "Need at least 3 points"}
        
        # Estimate local curvature
        curvatures = []
        for i in range(1, len(points) - 1):
            p1, p2, p3 = points[i-1], points[i], points[i+1]
            
            # Compute vectors
            v1 = [p2[j] - p1[j] for j in range(len(p1))]
            v2 = [p3[j] - p2[j] for j in range(len(p2))]
            
            # Estimate curvature as angle change
            dot = sum(a * b for a, b in zip(v1, v2))
            mag1 = sum(a ** 2 for a in v1) ** 0.5
            mag2 = sum(a ** 2 for a in v2) ** 0.5
            
            if mag1 > 0 and mag2 > 0:
                cos_angle = dot / (mag1 * mag2)
                cos_angle = max(-1, min(1, cos_angle))
                curvatures.append(1 - cos_angle)
        
        avg_curvature = sum(curvatures) / len(curvatures) if curvatures else 0
        
        self.metrics.tasks_completed += 1
        
        return {
            "scalar_curvature": avg_curvature,
            "max_curvature": max(curvatures) if curvatures else 0,
            "min_curvature": min(curvatures) if curvatures else 0,
        }
    
    def find_geodesic(
        self,
        start: Optional[Tuple[float, ...]],
        end: Optional[Tuple[float, ...]]
    ) -> Dict[str, Any]:
        """
        Find geodesic (shortest path) between two points.
        
        Args:
            start: Starting point.
            end: Ending point.
            
        Returns:
            Geodesic path information.
        """
        if start is None or end is None:
            return {"error": "Need start and end points"}
        
        if len(start) != len(end):
            return {"error": "Points must have same dimension"}
        
        # For flat space, geodesic is straight line
        distance = sum((a - b) ** 2 for a, b in zip(start, end)) ** 0.5
        
        # Generate path points
        n_steps = 10
        path = []
        for i in range(n_steps + 1):
            t = i / n_steps
            point = tuple(a + t * (b - a) for a, b in zip(start, end))
            path.append(point)
        
        self.metrics.tasks_completed += 1
        
        return {
            "start": start,
            "end": end,
            "distance": distance,
            "path": path,
            "n_steps": n_steps,
        }
    
    def compute_golden_spiral(
        self,
        n_points: int = 100,
        scale: float = 1.0
    ) -> List[Tuple[float, float]]:
        """
        Compute points on a golden spiral.
        
        The golden spiral is fundamental to the geometry of
        consciousness evolution.
        
        Args:
            n_points: Number of points to generate.
            scale: Scaling factor.
            
        Returns:
            List of (x, y) points on the spiral.
        """
        import genesis.core.math as gmath
        
        points = []
        golden_angle = PI * (3 - 5 ** 0.5)  # ~137.5 degrees
        
        for i in range(n_points):
            r = scale * (i ** 0.5)
            theta = i * golden_angle
            x = r * gmath.cos(theta)
            y = r * gmath.sin(theta)
            points.append((x, y))
        
        return points
    
    def analyze_torsion_convergence(
        self,
        angles: List[float]
    ) -> Dict[str, Any]:
        """
        Analyze torsion angles for convergence to θ_lock.
        
        Args:
            angles: List of torsion angles in degrees.
            
        Returns:
            Convergence analysis.
        """
        if not angles:
            return {"error": "No angles provided"}
        
        # Check convergence to THETA_LOCK
        deviations = [abs(a - THETA_LOCK) for a in angles]
        avg_deviation = sum(deviations) / len(deviations)
        
        converged_count = sum(1 for d in deviations if d < 1.0)
        convergence_ratio = converged_count / len(angles)
        
        return {
            "theta_lock": THETA_LOCK,
            "avg_deviation": avg_deviation,
            "convergence_ratio": convergence_ratio,
            "is_converged": convergence_ratio > 0.9,
            "angles_analyzed": len(angles),
        }

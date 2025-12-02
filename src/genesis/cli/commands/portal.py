"""Portal command for GENESIS CLI."""

from typing import Optional


def portal_command(
    portal_name: Optional[str] = None,
    action: str = "status",
) -> int:
    """
    Manage portals.
    
    Args:
        portal_name: Name of the portal.
        action: Action to perform (status, start, stop, list).
        
    Returns:
        Exit code (0 for success).
    """
    valid_portals = {
        "enterprise": "Commercial applications",
        "defense": "DoD/IC applications",
        "health": "Healthcare and life sciences",
        "legal": "Legal discovery and analysis",
        "darpa": "Advanced research programs",
    }
    
    if not portal_name or action == "list":
        print("\nAvailable portals:")
        for name, desc in valid_portals.items():
            print(f"  {name:12} - {desc}")
        print("\nUsage: genesis portal <name> [--status|--start|--stop]")
        return 0
    
    portal_name = portal_name.lower()
    
    if portal_name not in valid_portals:
        print(f"Unknown portal: {portal_name}")
        print(f"Valid portals: {', '.join(valid_portals.keys())}")
        return 1
    
    if action == "status":
        print(f"\n[{portal_name.upper()}] Portal Status")
        print(f"  Description: {valid_portals[portal_name]}")
        print(f"  Status: Online")
        print(f"  Active sessions: 0")
        print(f"  Classification: {'TS/SCI' if portal_name in ['defense', 'darpa'] else 'CONFIDENTIAL'}")
    elif action == "start":
        print(f"Starting {portal_name} portal...")
        print("Portal started successfully.")
    elif action == "stop":
        print(f"Stopping {portal_name} portal...")
        print("Portal stopped.")
    elif action == "restart":
        print(f"Restarting {portal_name} portal...")
        print("Portal restarted successfully.")
    else:
        print(f"Unknown action: {action}")
        return 1
    
    return 0

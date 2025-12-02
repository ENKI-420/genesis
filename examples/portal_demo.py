"""
Portal Demonstration

Shows how to use the various GENESIS portals.
"""

from genesis.portals import (
    EnterprisePortal,
    DefensePortal,
    HealthPortal,
    LegalPortal,
    DARPAPortal,
)
from genesis.classification.levels import UNCLASSIFIED, SECRET


def demo_enterprise():
    """Demonstrate enterprise portal."""
    print("=== Enterprise Portal ===")
    portal = EnterprisePortal()
    portal.initialize()
    
    session = portal.create_session("user_001")
    
    # Run optimization
    result = portal.optimize(session, "minimize_cost")
    print(f"Optimization result: {result}")
    
    # Run analysis
    result = portal.analyze(session, "geometric")
    print(f"Analysis result: {result}")
    
    portal.close_session(session.session_id)


def demo_defense():
    """Demonstrate defense portal."""
    print("\n=== Defense Portal ===")
    portal = DefensePortal()
    portal.initialize()
    
    session = portal.create_session("analyst_001", SECRET)
    
    # Run intel analysis
    result = portal.intel_analysis(session, "sigint", "target_alpha")
    print(f"Intel result: {result}")
    
    portal.close_session(session.session_id)


def demo_darpa():
    """Demonstrate DARPA portal."""
    print("\n=== DARPA Portal ===")
    portal = DARPAPortal()
    portal.initialize()
    
    session = portal.create_session("researcher_001")
    
    # Run readiness assessment
    result = portal.darpa_readiness_assessment(session)
    print(f"Readiness: {result}")
    
    portal.close_session(session.session_id)


if __name__ == "__main__":
    demo_enterprise()
    demo_defense()
    demo_darpa()

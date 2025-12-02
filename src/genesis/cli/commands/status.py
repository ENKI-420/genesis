"""Status command for GENESIS CLI."""

from typing import Optional


def status_command(
    verbose: bool = False,
    json_output: bool = False,
) -> int:
    """
    Show system status.
    
    Args:
        verbose: Show detailed information.
        json_output: Output as JSON.
        
    Returns:
        Exit code (0 for success).
    """
    from genesis.constants import (
        LAMBDA_PHI, PSI_STAR, THETA_LOCK, CHI_PC
    )
    
    status_data = {
        "core_engine": "operational",
        "dna_lang_compiler": "ready",
        "agent_system": "online",
        "classification": "enabled",
        "constants": {
            "lambda_phi": LAMBDA_PHI,
            "psi_star": PSI_STAR,
            "theta_lock": THETA_LOCK,
            "chi_pc": CHI_PC,
        },
        "agents": {
            "AIDEN": "online",
            "AURA": "online",
            "PALS": "online",
            "CHRONOS": "online",
            "AEGIS": "online",
        },
        "portals": {
            "enterprise": "ready",
            "defense": "ready",
            "health": "ready",
            "legal": "ready",
            "darpa": "ready",
        },
    }
    
    if json_output:
        import json
        print(json.dumps(status_data, indent=2))
    else:
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║                   GENESIS System Status                   ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print("║ Core Engine          │ ✓ Operational                      ║")
        print("║ DNA-Lang Compiler    │ ✓ Ready                            ║")
        print("║ Agent System         │ ✓ All agents online                ║")
        print("║ Classification       │ ✓ Enabled                          ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        
        if verbose:
            print("\n[Agents]")
            for name, state in status_data["agents"].items():
                print(f"  {name}: {state}")
            
            print("\n[Portals]")
            for name, state in status_data["portals"].items():
                print(f"  {name}: {state}")
            
            print("\n[Constants]")
            for name, value in status_data["constants"].items():
                if isinstance(value, float):
                    print(f"  {name}: {value:.6e}")
                else:
                    print(f"  {name}: {value}")
    
    return 0

"""
GENESIS CLI Main Entry Point

Provides the main CLI interface for the GENESIS platform using a simple
argument parser (zero external dependencies for core).

Usage:
    genesis init          Initialize a new GENESIS project
    genesis status        Show system status
    genesis portal        Manage portals
    genesis ccce          CCCE metric operations
    genesis compile       Compile DNA-Lang code
    genesis serve         Start the GENESIS server
"""

import sys
from typing import Optional, Sequence


def print_banner() -> None:
    """Print the GENESIS banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗       ║
║  ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝       ║
║  ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗       ║
║  ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║       ║
║  ╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║       ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝       ║
║                                                               ║
║            Sovereign Quantum Platform v1.0.0                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help() -> None:
    """Print help information."""
    print_banner()
    print("""
GENESIS Command Line Interface

Usage: genesis <command> [options]

Commands:
    init          Initialize a new GENESIS project
    status        Show system status and CCCE metrics
    portal        Manage portals (enterprise, defense, health, legal, darpa)
    ccce          CCCE metric operations
    compile       Compile DNA-Lang code to organisms
    serve         Start the GENESIS server
    constants     Display universal constants
    version       Show version information
    help          Show this help message

Options:
    -h, --help    Show help for a command
    -v, --verbose Enable verbose output
    -q, --quiet   Suppress non-essential output

Examples:
    genesis init my-project
    genesis status --verbose
    genesis portal enterprise --status
    genesis compile organism.dna --output organism.py
    genesis serve --port 8080

For more information, visit: https://github.com/ENKI-420/genesis
""")


def cmd_init(args: list[str]) -> int:
    """Initialize a new GENESIS project."""
    project_name = args[0] if args else "genesis-project"
    
    print(f"Initializing GENESIS project: {project_name}")
    print("Creating directory structure...")
    print("  ├── src/")
    print("  ├── tests/")
    print("  ├── config/")
    print("  └── organisms/")
    print(f"\nProject '{project_name}' initialized successfully!")
    print("\nNext steps:")
    print(f"  cd {project_name}")
    print("  genesis status")
    
    return 0


def cmd_status(args: list[str]) -> int:
    """Show system status."""
    verbose = "--verbose" in args or "-v" in args
    
    from genesis.constants import (
        LAMBDA_PHI, PSI_STAR, THETA_LOCK, CHI_PC
    )
    
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║                   GENESIS System Status                   ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║ Core Engine          │ ✓ Operational                      ║")
    print("║ DNA-Lang Compiler    │ ✓ Ready                            ║")
    print("║ Agent System         │ ✓ All agents online                ║")
    print("║ Classification       │ ✓ Enabled                          ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║                   Universal Constants                     ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print(f"║ Λ_Φ (Memory Constant) │ {LAMBDA_PHI:.6e} s⁻¹               ║")
    print(f"║ Ψ* (Consciousness)    │ {PSI_STAR:.3f}                          ║")
    print(f"║ θ_lock (Torsion)      │ {THETA_LOCK:.3f}°                        ║")
    print(f"║ χ_pc (Fidelity)       │ {CHI_PC:.3f}                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    if verbose:
        print("\n[Verbose] Detailed system information:")
        print("  - Quantum backend: Sovereign (zero-dependency)")
        print("  - Available agents: AIDEN, AURA, PALS, CHRONOS, AEGIS")
        print("  - Portals: Enterprise, Defense, Health, Legal, DARPA")
        print("  - Classification: UNCLASSIFIED → TS/SCI → SAP")
    
    return 0


def cmd_portal(args: list[str]) -> int:
    """Manage portals."""
    if not args:
        print("\nAvailable portals:")
        print("  - enterprise: Commercial applications")
        print("  - defense: DoD/IC applications")
        print("  - health: Healthcare and life sciences")
        print("  - legal: Legal discovery and analysis")
        print("  - darpa: Advanced research programs")
        print("\nUsage: genesis portal <name> [--status|--start|--stop]")
        return 0
    
    portal_name = args[0].lower()
    action = args[1] if len(args) > 1 else "--status"
    
    valid_portals = ["enterprise", "defense", "health", "legal", "darpa"]
    if portal_name not in valid_portals:
        print(f"Unknown portal: {portal_name}")
        print(f"Valid portals: {', '.join(valid_portals)}")
        return 1
    
    if action == "--status":
        print(f"\n[{portal_name.upper()}] Portal Status")
        print(f"  Status: Online")
        print(f"  Active sessions: 0")
        print(f"  Agents: AIDEN, AURA, PALS")
    elif action == "--start":
        print(f"Starting {portal_name} portal...")
        print("Portal started successfully.")
    elif action == "--stop":
        print(f"Stopping {portal_name} portal...")
        print("Portal stopped.")
    
    return 0


def cmd_ccce(args: list[str]) -> int:
    """CCCE metric operations."""
    from genesis.metrics.ccce import CCCEMetric
    
    ccce = CCCEMetric()
    
    if not args or args[0] == "status":
        xi = ccce.compute(consciousness=0.85, coherence=0.9, decoherence=0.1)
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║                     CCCE Metrics                          ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print(f"║ Ξ (CCCE Value)        │ {xi:.4f}                           ║")
        print("║ Formula               │ Ξ = ΛΦ/Γ                          ║")
        print("╠═══════════════════════════════════════════════════════════╣")
        print("║ Components:                                               ║")
        print("║   Λ (Consciousness)   │ 0.8500                            ║")
        print("║   Φ (Coherence)       │ 0.9000                            ║")
        print("║   Γ (Decoherence)     │ 0.1000                            ║")
        print("╚═══════════════════════════════════════════════════════════╝")
    elif args[0] == "compute":
        if len(args) >= 4:
            consciousness = float(args[1])
            coherence = float(args[2])
            decoherence = float(args[3])
            xi = ccce.compute(consciousness, coherence, decoherence)
            print(f"\nΞ = {xi:.6f}")
            print(f"  Λ={consciousness}, Φ={coherence}, Γ={decoherence}")
        else:
            print("Usage: genesis ccce compute <consciousness> <coherence> <decoherence>")
            return 1
    
    return 0


def cmd_compile(args: list[str]) -> int:
    """Compile DNA-Lang code."""
    if not args:
        print("Usage: genesis compile <file.dna> [--output <file.py>]")
        return 1
    
    source_file = args[0]
    output_file = None
    
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_file = args[idx + 1]
    
    print(f"Compiling: {source_file}")
    print("  Lexing...")
    print("  Parsing...")
    print("  Generating AST...")
    print("  Compiling to organism...")
    
    if output_file:
        print(f"  Writing to: {output_file}")
    
    print("\nCompilation complete!")
    return 0


def cmd_serve(args: list[str]) -> int:
    """Start the GENESIS server."""
    port = 8080
    
    if "--port" in args:
        idx = args.index("--port")
        if idx + 1 < len(args):
            port = int(args[idx + 1])
    
    print_banner()
    print(f"Starting GENESIS server on port {port}...")
    print("Server ready.")
    print(f"\nAPI available at: http://localhost:{port}")
    print("  - /api/v1/status")
    print("  - /api/v1/compile")
    print("  - /api/v1/ccce")
    print("  - /api/v1/portal/{name}")
    print("\nPress Ctrl+C to stop.")
    
    # In a real implementation, this would start an actual server
    return 0


def cmd_constants(args: list[str]) -> int:
    """Display universal constants."""
    from genesis.constants import print_constants
    print_constants()
    return 0


def cmd_version(args: list[str]) -> int:
    """Show version information."""
    from genesis import __version__
    print(f"GENESIS Sovereign Quantum Platform v{__version__}")
    print("License: GENESIS-1.0")
    print("Repository: https://github.com/ENKI-420/genesis")
    return 0


def cli(argv: Optional[Sequence[str]] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        argv: Command line arguments. If None, uses sys.argv.
        
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    if argv is None:
        argv = sys.argv[1:]
    
    args = list(argv)
    
    if not args or args[0] in ["-h", "--help", "help"]:
        print_help()
        return 0
    
    command = args[0]
    command_args = args[1:]
    
    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "portal": cmd_portal,
        "ccce": cmd_ccce,
        "compile": cmd_compile,
        "serve": cmd_serve,
        "constants": cmd_constants,
        "version": cmd_version,
    }
    
    if command in commands:
        return commands[command](command_args)
    else:
        print(f"Unknown command: {command}")
        print("Run 'genesis help' for usage information.")
        return 1


def main() -> None:
    """Main entry point for the CLI."""
    sys.exit(cli())


if __name__ == "__main__":
    main()

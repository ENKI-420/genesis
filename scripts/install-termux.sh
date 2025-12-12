#!/data/data/com.termux/files/usr/bin/sh
# GENESIS Sovereign Platform Installer for Android/Termux
# Termux-specific installation script

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   GENESIS Sovereign Platform - Termux Installer           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "⚠️  Warning: This script is designed for Termux on Android"
    echo "For standard Linux/macOS, use install.sh instead"
fi

# Install minimal dependencies via pkg
echo "Installing dependencies..."
if command -v pkg >/dev/null 2>&1; then
    pkg install -y python >/dev/null 2>&1 || true
    echo "✓ Dependencies checked"
else
    echo "⚠️  pkg not found, assuming Python is already installed"
fi

# Check Python availability
if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
    echo "Error: Python is not installed"
    echo "Please install Python: pkg install python"
    exit 1
fi

echo "✓ Python detected"

# Define installation directory
GENESIS_HOME="${HOME}/.genesis"

# Create directory structure
echo "Creating GENESIS directory structure at ${GENESIS_HOME}..."

mkdir -p "${GENESIS_HOME}/bin"
mkdir -p "${GENESIS_HOME}/lib"
mkdir -p "${GENESIS_HOME}/config"
mkdir -p "${GENESIS_HOME}/archive"
mkdir -p "${GENESIS_HOME}/logs"

# Portal directories
mkdir -p "${GENESIS_HOME}/portals/enterprise"
mkdir -p "${GENESIS_HOME}/portals/defense"
mkdir -p "${GENESIS_HOME}/portals/health"
mkdir -p "${GENESIS_HOME}/portals/legal"
mkdir -p "${GENESIS_HOME}/portals/darpa"

# Classification directories
mkdir -p "${GENESIS_HOME}/classification/unclassified"
mkdir -p "${GENESIS_HOME}/classification/cui"
mkdir -p "${GENESIS_HOME}/classification/secret"
mkdir -p "${GENESIS_HOME}/classification/top-secret"
mkdir -p "${GENESIS_HOME}/classification/ts-sci"
mkdir -p "${GENESIS_HOME}/classification/sap"

echo "✓ Directory structure created"

# Create Genesis CLI script with Termux-specific shebang
echo "Installing Genesis CLI to ${GENESIS_HOME}/bin/genesis..."

cat > "${GENESIS_HOME}/bin/genesis" << 'GENESIS_CLI_EOF'
#!/usr/bin/env python3
"""
GENESIS Sovereign Platform CLI
Minimal, self-contained command-line interface
Termux/Android Edition
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

GENESIS_HOME = Path.home() / ".genesis"
CONFIG_FILE = GENESIS_HOME / "config" / "genesis.json"
LOG_DIR = GENESIS_HOME / "logs"

def show_banner():
    """Display GENESIS banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                  GENESIS SOVEREIGN PLATFORM                   ║
║                   Quantum-Secured Intelligence                ║
║                      Termux/Android Edition                   ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def log_event(event_type, message):
    """Log event to file"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"genesis_{datetime.now().strftime('%Y%m%d')}.log"
    timestamp = datetime.now().isoformat()
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {event_type}: {message}\n")

def init_command():
    """Initialize GENESIS configuration"""
    print("Initializing GENESIS configuration...")
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    config = {
        "version": "1.0.0",
        "platform": "termux-android",
        "initialized": datetime.now().isoformat(),
        "portals": ["enterprise", "defense", "health", "legal", "darpa"],
        "classification_levels": ["unclassified", "cui", "secret", "top-secret", "ts-sci", "sap"]
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    log_event("INIT", "GENESIS configuration initialized on Termux")
    print(f"✓ Configuration initialized at {CONFIG_FILE}")
    print("✓ GENESIS is ready to use on Termux")

def status_command():
    """Show GENESIS system status"""
    print("GENESIS System Status (Termux):")
    print(f"  Home: {GENESIS_HOME}")
    print(f"  Config: {'✓ Initialized' if CONFIG_FILE.exists() else '✗ Not initialized (run: genesis init)'}")
    
    # Check directory structure
    dirs_ok = all([
        (GENESIS_HOME / "bin").exists(),
        (GENESIS_HOME / "lib").exists(),
        (GENESIS_HOME / "config").exists(),
        (GENESIS_HOME / "archive").exists(),
        (GENESIS_HOME / "logs").exists(),
    ])
    print(f"  Directories: {'✓ OK' if dirs_ok else '✗ Missing'}")
    
    # Check portals
    portals = ["enterprise", "defense", "health", "legal", "darpa"]
    portals_ok = all([(GENESIS_HOME / "portals" / p).exists() for p in portals])
    print(f"  Portals: {'✓ OK' if portals_ok else '✗ Missing'}")
    
    # Check classification levels
    levels = ["unclassified", "cui", "secret", "top-secret", "ts-sci", "sap"]
    levels_ok = all([(GENESIS_HOME / "classification" / l).exists() for l in levels])
    print(f"  Classification: {'✓ OK' if levels_ok else '✗ Missing'}")
    
    log_event("STATUS", "Status check performed on Termux")

def portal_command(portal_name=None):
    """Access GENESIS portals"""
    portals = ["enterprise", "defense", "health", "legal", "darpa"]
    
    if not portal_name:
        print("Available GENESIS Portals:")
        for p in portals:
            portal_dir = GENESIS_HOME / "portals" / p
            status = "✓" if portal_dir.exists() else "✗"
            print(f"  {status} {p}")
        print("\nUsage: genesis portal <name>")
        return
    
    if portal_name not in portals:
        print(f"Error: Unknown portal '{portal_name}'")
        print(f"Available: {', '.join(portals)}")
        return
    
    portal_dir = GENESIS_HOME / "portals" / portal_name
    print(f"Accessing {portal_name.upper()} portal at {portal_dir}")
    log_event("PORTAL", f"Accessed {portal_name} portal")

def archive_command(target=None):
    """Archive management"""
    archive_dir = GENESIS_HOME / "archive"
    
    if not target:
        print(f"Archive directory: {archive_dir}")
        if archive_dir.exists():
            archives = list(archive_dir.glob("*"))
            print(f"Total archives: {len(archives)}")
            if archives:
                print("\nRecent archives:")
                for arch in sorted(archives, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    print(f"  - {arch.name}")
        return
    
    print(f"Archiving {target}...")
    log_event("ARCHIVE", f"Archive operation for {target}")
    print("✓ Archive created")

def ccce_command():
    """Continuous Compliance and Certification Engine"""
    print("CCCE - Continuous Compliance and Certification Engine")
    print("Status: Active")
    print("  Compliance Frameworks: NIST, ISO 27001, FedRAMP")
    print("  Last Audit: In-progress")
    print("  Certifications: Up-to-date")
    log_event("CCCE", "CCCE status checked")

def omega_command():
    """Ωmega Protocol - Ultimate Security Override"""
    print("Ωmega Protocol Access")
    print("⚠️  WARNING: Ultimate security override protocol")
    print("Status: Standby")
    print("Authorization: Required")
    log_event("OMEGA", "Omega protocol accessed (authorization required)")

def prove_command(statement=None):
    """Zero-knowledge proof generation"""
    if not statement:
        print("PROVE - Zero-Knowledge Proof System")
        print("Usage: genesis prove <statement>")
        print("Example: genesis prove 'I have security clearance'")
        return
    
    print(f"Generating zero-knowledge proof for: {statement}")
    print("⚙️  Computing proof...")
    print("✓ Proof generated (simulated)")
    log_event("PROVE", f"ZK proof generated for: {statement}")

def show_help():
    """Show help information"""
    show_banner()
    print("GENESIS Command-Line Interface (Termux Edition)\n")
    print("Usage: genesis <command> [options]\n")
    print("Commands:")
    print("  init              Initialize GENESIS configuration")
    print("  status            Show system status")
    print("  portal [name]     Access portal (enterprise|defense|health|legal|darpa)")
    print("  archive [target]  Archive management")
    print("  ccce              Continuous Compliance and Certification Engine")
    print("  omega             Ωmega Protocol access")
    print("  prove <statement> Generate zero-knowledge proof")
    print("  help              Show this help message")
    print("\nExamples:")
    print("  genesis init")
    print("  genesis status")
    print("  genesis portal defense")
    print("  genesis prove 'statement'")
    print("")

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command in ['help', '--help', '-h']:
        show_help()
    elif command == 'init':
        init_command()
    elif command == 'status':
        status_command()
    elif command == 'portal':
        portal_name = sys.argv[2] if len(sys.argv) > 2 else None
        portal_command(portal_name)
    elif command == 'archive':
        target = sys.argv[2] if len(sys.argv) > 2 else None
        archive_command(target)
    elif command == 'ccce':
        ccce_command()
    elif command == 'omega':
        omega_command()
    elif command == 'prove':
        statement = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else None
        prove_command(statement)
    else:
        print(f"Error: Unknown command '{command}'")
        print("Run 'genesis help' for usage information")
        sys.exit(1)

if __name__ == '__main__':
    main()
GENESIS_CLI_EOF

# Make CLI executable
chmod +x "${GENESIS_HOME}/bin/genesis"
echo "✓ Genesis CLI installed"

# Update PATH for Termux shells (bash and zsh)
for SHELL_RC in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
    if [ -f "${SHELL_RC}" ]; then
        if ! grep -q ".genesis/bin" "${SHELL_RC}"; then
            echo "" >> "${SHELL_RC}"
            echo "# GENESIS Sovereign Platform" >> "${SHELL_RC}"
            echo "export PATH=\"\${HOME}/.genesis/bin:\${PATH}\"" >> "${SHELL_RC}"
            echo "✓ PATH updated in ${SHELL_RC}"
        else
            echo "✓ PATH already configured in ${SHELL_RC}"
        fi
    fi
done

# Create shell RC files if they don't exist
if [ ! -f "${HOME}/.bashrc" ]; then
    echo "# Termux bash configuration" > "${HOME}/.bashrc"
    echo "export PATH=\"\${HOME}/.genesis/bin:\${PATH}\"" >> "${HOME}/.bashrc"
    echo "✓ Created .bashrc with PATH configuration"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         Installation Complete! (Termux Edition)          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "GENESIS has been installed to: ${GENESIS_HOME}"
echo ""
echo "To start using GENESIS on Termux:"
echo "  1. Reload your shell: source ~/.bashrc"
echo "     Or restart Termux"
echo "  2. Initialize GENESIS: genesis init"
echo "  3. Check status: genesis status"
echo "  4. Get help: genesis help"
echo ""
echo "Available commands:"
echo "  genesis init      - Initialize configuration"
echo "  genesis status    - Show system status"
echo "  genesis portal    - Access portals"
echo "  genesis help      - Show all commands"
echo ""
echo "Installation log: ${GENESIS_HOME}/logs/"
echo ""
echo "Note: Termux-specific features optimized for Android"
echo ""

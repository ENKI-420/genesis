# GENESIS Sovereign Platform - Installation Guide

This guide provides instructions for installing the GENESIS Sovereign Platform on your local system.

## Quick Installation

### Linux/macOS/PC

One-liner installation (when repository is publicly accessible):
```bash
curl -fsSL https://raw.githubusercontent.com/ENKI-420/genesis/main/install.sh | sh
```

**Local Installation** (if the remote URL is not available or you cloned the repository):
```bash
cd /path/to/genesis
chmod +x install.sh
./install.sh
```

### Android/Termux

One-liner installation (when repository is publicly accessible):
```bash
curl -fsSL https://raw.githubusercontent.com/ENKI-420/genesis/main/scripts/install-termux.sh | sh
```

**Local Installation** (if the remote URL is not available):
```bash
cd /path/to/genesis
chmod +x scripts/install-termux.sh
./scripts/install-termux.sh
```

## What Gets Installed

The installer creates a local GENESIS installation at `~/.genesis` with the following structure:

```
~/.genesis/
├── bin/
│   └── genesis              # GENESIS CLI executable
├── lib/                     # Libraries (for future use)
├── config/                  # Configuration files
├── archive/                 # Archive storage
├── logs/                    # System logs
├── portals/                 # Portal-specific data
│   ├── enterprise/
│   ├── defense/
│   ├── health/
│   ├── legal/
│   └── darpa/
└── classification/          # Classification-level storage
    ├── unclassified/
    ├── cui/
    ├── secret/
    ├── top-secret/
    ├── ts-sci/
    └── sap/
```

## Post-Installation

After running the installer:

1. **Reload your shell configuration:**
   ```bash
   source ~/.bashrc    # For bash
   # or
   source ~/.zshrc     # For zsh
   # or restart your terminal
   ```

2. **Initialize GENESIS:**
   ```bash
   genesis init
   ```

3. **Verify installation:**
   ```bash
   genesis status
   ```

4. **Get help:**
   ```bash
   genesis help
   ```

## Available Commands

After installation, the `genesis` command will be available in your PATH:

- `genesis init` - Initialize GENESIS configuration
- `genesis status` - Show system status
- `genesis portal [name]` - Access portals (enterprise, defense, health, legal, darpa)
- `genesis archive [target]` - Archive management
- `genesis ccce` - Continuous Compliance and Certification Engine
- `genesis omega` - Ωmega Protocol access
- `genesis prove <statement>` - Generate zero-knowledge proof
- `genesis help` - Show help message

## Requirements

### Linux/macOS
- Python 3.6 or higher
- Standard POSIX shell (sh, bash, zsh)
- Basic Unix utilities (mkdir, chmod, grep)

### Android/Termux
- Termux app installed
- Python package: `pkg install python`
- Git (optional): `pkg install git`

## Troubleshooting

### 404 Error on Remote Installation

If you encounter a 404 error when trying to use the one-liner installation command:

```
curl: (22) The requested URL returned error: 404
```

**Causes:**
- The repository may not be publicly accessible yet
- The branch containing the installer may not be merged to main
- GitHub raw content URL may be temporarily unavailable

**Solutions:**

1. **Clone and install locally:**
   ```bash
   git clone https://github.com/ENKI-420/genesis.git
   cd genesis
   chmod +x install.sh
   ./install.sh
   ```

2. **Check branch availability:**
   - Ensure the installer has been merged to the `main` branch
   - Check if the file exists at: https://github.com/ENKI-420/genesis/blob/main/install.sh

3. **Manual installation:**
   - Download the repository as a ZIP
   - Extract and navigate to the directory
   - Run the installer: `./install.sh`

### Permission Denied

If you get "Permission denied" when running the installer:

```bash
chmod +x install.sh
./install.sh
```

### Command Not Found After Installation

If `genesis` command is not found after installation:

1. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

2. **Manually add to PATH:**
   ```bash
   echo 'export PATH="${HOME}/.genesis/bin:${PATH}"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Verify installation:**
   ```bash
   ls -la ~/.genesis/bin/genesis
   # Should show an executable file
   ```

### Python Not Found (Termux)

If Python is not installed on Termux:

```bash
pkg update
pkg install python
```

### Directory Already Exists

The installer is idempotent - running it multiple times is safe. It will:
- Skip creating directories that already exist
- Overwrite the CLI script with the latest version
- Not duplicate PATH entries in shell configuration

## Uninstallation

To remove GENESIS from your system:

```bash
# Remove GENESIS directory
rm -rf ~/.genesis

# Remove PATH entry from shell configuration
# Edit ~/.bashrc or ~/.zshrc and remove the line:
# export PATH="${HOME}/.genesis/bin:${PATH}"
```

## Next Steps

After successful installation:

1. **Initialize the system:**
   ```bash
   genesis init
   ```

2. **Explore portals:**
   ```bash
   genesis portal          # List available portals
   genesis portal defense  # Access defense portal
   ```

3. **Check system status regularly:**
   ```bash
   genesis status
   ```

4. **Review logs:**
   ```bash
   ls ~/.genesis/logs/
   ```

## Support

For issues, questions, or contributions:
- Create an issue in the [GitHub repository](https://github.com/ENKI-420/genesis/issues)
- Review existing documentation in the `docs/` directory
- Check the main [README.md](../README.md) for project overview

## Security Note

The GENESIS Sovereign Platform includes classification-level directories (unclassified, cui, secret, etc.). These are for organizational purposes in the local installation. Actual security classification and handling of classified information must follow your organization's security policies and government regulations.

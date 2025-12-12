#!/bin/bash
# Test script for GENESIS installer
# Validates installer behavior in a sandboxed environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           GENESIS Installer Test Suite                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail_test() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

warn_test() {
    echo -e "${YELLOW}⚠ WARN${NC}: $1"
}

# Create temporary test directory
TEST_DIR=$(mktemp -d)
echo "Test directory: ${TEST_DIR}"
echo ""

# Set up test environment with fake HOME
export TEST_HOME="${TEST_DIR}/home"
mkdir -p "${TEST_HOME}"

# Find the repository root (go up from tests/ directory)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_SCRIPT="${REPO_ROOT}/install.sh"

echo "Repository root: ${REPO_ROOT}"
echo "Install script: ${INSTALL_SCRIPT}"
echo ""

# Test 1: Check if install script exists
echo "Test 1: Verify install.sh exists"
if [ -f "${INSTALL_SCRIPT}" ]; then
    pass_test "install.sh found at ${INSTALL_SCRIPT}"
else
    fail_test "install.sh not found at ${INSTALL_SCRIPT}"
    echo "Cannot continue without installer script"
    exit 1
fi

# Test 2: Check if script is executable
echo ""
echo "Test 2: Verify install.sh is executable"
if [ -x "${INSTALL_SCRIPT}" ]; then
    pass_test "install.sh is executable"
else
    warn_test "install.sh is not executable, attempting to fix..."
    chmod +x "${INSTALL_SCRIPT}"
    if [ -x "${INSTALL_SCRIPT}" ]; then
        pass_test "install.sh made executable"
    else
        fail_test "Could not make install.sh executable"
    fi
fi

# Test 3: Run installer in test environment
echo ""
echo "Test 3: Run installer in sandboxed environment"
cd "${TEST_DIR}"

# Create a minimal shell RC file for testing
touch "${TEST_HOME}/.bashrc"

# Run installer with custom HOME
if HOME="${TEST_HOME}" "${INSTALL_SCRIPT}" > "${TEST_DIR}/install_output.log" 2>&1; then
    pass_test "Installer executed successfully"
else
    fail_test "Installer failed with exit code $?"
    echo "Installer output:"
    cat "${TEST_DIR}/install_output.log"
fi

# Test 4: Verify directory structure
echo ""
echo "Test 4: Verify ~/.genesis directory structure"

GENESIS_HOME="${TEST_HOME}/.genesis"

required_dirs=(
    "bin"
    "lib"
    "config"
    "archive"
    "logs"
    "portals/enterprise"
    "portals/defense"
    "portals/health"
    "portals/legal"
    "portals/darpa"
    "classification/unclassified"
    "classification/cui"
    "classification/secret"
    "classification/top-secret"
    "classification/ts-sci"
    "classification/sap"
)

all_dirs_ok=true
for dir in "${required_dirs[@]}"; do
    if [ -d "${GENESIS_HOME}/${dir}" ]; then
        pass_test "Directory exists: ${dir}"
    else
        fail_test "Directory missing: ${dir}"
        all_dirs_ok=false
    fi
done

# Test 5: Verify genesis CLI exists and is executable
echo ""
echo "Test 5: Verify genesis CLI installation"

GENESIS_CLI="${GENESIS_HOME}/bin/genesis"

if [ -f "${GENESIS_CLI}" ]; then
    pass_test "genesis CLI file exists"
else
    fail_test "genesis CLI file not found at ${GENESIS_CLI}"
fi

if [ -x "${GENESIS_CLI}" ]; then
    pass_test "genesis CLI is executable"
else
    fail_test "genesis CLI is not executable"
fi

# Test 6: Verify CLI file content
echo ""
echo "Test 6: Verify genesis CLI content"

if [ -f "${GENESIS_CLI}" ]; then
    # Check for Python shebang
    if head -n 1 "${GENESIS_CLI}" | grep -q "python"; then
        pass_test "CLI has Python shebang"
    else
        fail_test "CLI missing Python shebang"
    fi
    
    # Check for key functions
    if grep -q "def show_banner" "${GENESIS_CLI}"; then
        pass_test "CLI contains show_banner function"
    else
        fail_test "CLI missing show_banner function"
    fi
    
    if grep -q "def init_command" "${GENESIS_CLI}"; then
        pass_test "CLI contains init_command function"
    else
        fail_test "CLI missing init_command function"
    fi
    
    if grep -q "def status_command" "${GENESIS_CLI}"; then
        pass_test "CLI contains status_command function"
    else
        fail_test "CLI missing status_command function"
    fi
    
    # Check for all required commands
    required_commands=("portal" "archive" "ccce" "omega" "prove")
    for cmd in "${required_commands[@]}"; do
        if grep -q "def ${cmd}_command" "${GENESIS_CLI}"; then
            pass_test "CLI contains ${cmd}_command function"
        else
            fail_test "CLI missing ${cmd}_command function"
        fi
    done
fi

# Test 7: Verify PATH configuration
echo ""
echo "Test 7: Verify PATH configuration in shell RC"

if [ -f "${TEST_HOME}/.bashrc" ]; then
    if grep -q ".genesis/bin" "${TEST_HOME}/.bashrc"; then
        pass_test "PATH entry added to .bashrc"
    else
        fail_test "PATH entry not found in .bashrc"
    fi
    
    # Check for idempotency marker
    if grep -q "GENESIS Sovereign Platform" "${TEST_HOME}/.bashrc"; then
        pass_test "Installation marker found in .bashrc"
    else
        warn_test "Installation marker not found in .bashrc"
    fi
fi

# Test 8: Test idempotency - run installer again
echo ""
echo "Test 8: Test installer idempotency"

BASHRC_BEFORE=$(cat "${TEST_HOME}/.bashrc")
if HOME="${TEST_HOME}" "${INSTALL_SCRIPT}" > "${TEST_DIR}/install_output2.log" 2>&1; then
    pass_test "Second installer run succeeded"
    
    BASHRC_AFTER=$(cat "${TEST_HOME}/.bashrc")
    
    # Count PATH entries
    PATH_COUNT=$(grep -c ".genesis/bin" "${TEST_HOME}/.bashrc" || true)
    if [ "${PATH_COUNT}" -eq 1 ]; then
        pass_test "No duplicate PATH entries after re-run"
    else
        fail_test "Found ${PATH_COUNT} PATH entries (expected 1)"
    fi
else
    fail_test "Second installer run failed"
fi

# Test 9: Verify CLI can be executed (syntax check)
echo ""
echo "Test 9: Verify CLI Python syntax"

if command -v python3 >/dev/null 2>&1; then
    if python3 -m py_compile "${GENESIS_CLI}" 2>/dev/null; then
        pass_test "CLI Python syntax is valid"
    else
        fail_test "CLI has Python syntax errors"
    fi
else
    warn_test "Python3 not available, skipping syntax check"
fi

# Test 10: Test CLI help command
echo ""
echo "Test 10: Test CLI help command execution"

if command -v python3 >/dev/null 2>&1; then
    if python3 "${GENESIS_CLI}" help > "${TEST_DIR}/cli_help_output.log" 2>&1; then
        pass_test "CLI help command executed successfully"
        
        # Verify help output contains key information
        if grep -q "GENESIS" "${TEST_DIR}/cli_help_output.log"; then
            pass_test "Help output contains GENESIS banner"
        else
            fail_test "Help output missing GENESIS banner"
        fi
        
        if grep -q "Commands:" "${TEST_DIR}/cli_help_output.log"; then
            pass_test "Help output lists commands"
        else
            fail_test "Help output missing commands list"
        fi
    else
        fail_test "CLI help command failed"
        cat "${TEST_DIR}/cli_help_output.log"
    fi
else
    warn_test "Python3 not available, skipping CLI execution test"
fi

# Cleanup
echo ""
echo "Cleaning up test environment..."
rm -rf "${TEST_DIR}"
echo "✓ Test directory removed"

# Print summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    Test Summary                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${TESTS_FAILED} -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi

#!/usr/bin/env bash
# ==============================================================================
# MUIOGO VERIFICATION GATEWAY
# ==============================================================================
# This script is the primary safety gate for upstream pulls from OSeMOSYS/MUIO.
# It ensures that MUIOGO's portability, security, and stability are preserved.
#
# MAINTAINER NOTES (Always Review these files during a v5.x pull):
# 1. API/app.py - Core Flask config and blueprint registration.
# 2. API/Classes/Case/OsemosysClass.py - Model execution logic.
# 3. API/Routes/Case/CaseRoute.py - Backend API for case management.
# 4. WebAPP/Classes/Osemosys.Class.js - Frontend solver coordination.
#
# REJECTED PATTERNS:
# - Hardcoded paths (e.g. C:\)
# - Insecure session/path handling
# - Breaking Python 3.10-3.12 support
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

BOLD="\033[1m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

# Disable colours when not in a real terminal
if [ ! -t 1 ]; then
    BOLD="" GREEN="" YELLOW="" RED="" RESET=""
fi

_print_header() {
    echo -e "\n${BOLD}=== $1 ===${RESET}"
}

_print_status() {
    if [ "$1" -eq 0 ]; then
        echo -e "  ${GREEN}[PASS]${RESET} $2"
    else
        echo -e "  ${RED}[FAIL]${RESET} $2"
        [ -n "${3:-}" ] && echo -e "\n${3}"
        exit 1
    fi
}

# 1. Environment & Solvers check
_print_header "Step 1: Environment & Solvers"
# Run setup check quietly, only show output on failure
if OUTPUT=$("$SCRIPT_DIR/setup.sh" --check --no-demo-data 2>&1); then
    _print_status 0 "Python venv and solvers (GLPK/CBC) are ready."
else
    _print_status 1 "Environment check failed. Run ./scripts/setup.sh first." "$OUTPUT"
fi

# 2. Syntax Check (py_compile)
_print_header "Step 2: Python Syntax Check"
if python3 -m py_compile "$PROJECT_ROOT/API/app.py" 2>/dev/null; then
    _print_status 0 "app.py is syntactically valid."
else
    _print_status 1 "Syntax error detected in app.py."
fi

# 3. Smoke Test Harness
_print_header "Step 3: API & Route Smoke Tests"
if OUTPUT=$(python3 "$PROJECT_ROOT/tests/smoke_test.py" 2>&1); then
    _print_status 0 "Smoke tests passed (API boot and core routes)."
else
    _print_status 1 "Smoke tests failed." "$OUTPUT"
fi

# 4. Unresolved Merge state
_print_header "Step 4: Git Merge Integrity"
if [ -d "$PROJECT_ROOT/.git" ]; then
    if [ -f "$PROJECT_ROOT/.git/MERGE_HEAD" ] || [ -f "$PROJECT_ROOT/.git/REBASE_HEAD" ] || [ -f "$PROJECT_ROOT/.git/CHERRY_PICK_HEAD" ]; then
        _print_status 1 "Unresolved git merge/rebase detected (.git/MERGE_HEAD exists)."
    else
        _print_status 0 "No unresolved git merge/rebase state found."
    fi
else
    echo -e "  ${YELLOW}[SKIP]${RESET} Not a git repository."
fi

# 5. Conflict Markers scan
_print_header "Step 5: Conflict Marker Scan"
# Use ^ to match markers at the beginning of the line to avoid decorative comments
if grep -rnE "^<<<<<<<|^=======|^>>>>>>>" "$PROJECT_ROOT/API" "$PROJECT_ROOT/WebAPP/App" --exclude-dir=__pycache__ > /dev/null 2>&1; then
    _print_status 1 "Conflict markers found in the codebase!"
    grep -rnE "^<<<<<<<|^=======|^>>>>>>>" "$PROJECT_ROOT/API" "$PROJECT_ROOT/WebAPP/App" --exclude-dir=__pycache__
else
    _print_status 0 "No conflict markers found in key backend/frontend folders."
fi

echo -e "\n${BOLD}${GREEN}Verification Complete: MUIOGO is healthy and ready for upstream pull.${RESET}\n"

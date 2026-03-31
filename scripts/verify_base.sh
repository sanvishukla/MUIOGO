#!/usr/bin/env bash
# verification_checklist.sh - High-level sanity check for MUIOGO base.
# Fail if any command fails.
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

_print_pass() { echo -e "  ${GREEN}[PASS]${RESET} $1"; }
_print_fail() { echo -e "  ${RED}[FAIL]${RESET} $1"; }
_print_warn() { echo -e "  ${YELLOW}[WARN]${RESET} $1"; }

# 1. Environment & Solvers check
_print_header "Step 1: setup.sh --check"
# We skip demo-data in the smoke check as it's not strictly required for API/Backend sanity.
if "$SCRIPT_DIR/setup.sh" --check --no-demo-data; then
    _print_pass "Environment and solvers are ready."
else
    _print_fail "Environment check failed. Run ./scripts/setup.sh first."
    exit 1
fi

# 2. Syntax Check (py_compile)
_print_header "Step 2: Python syntax check"
python3 -m py_compile "$PROJECT_ROOT/API/app.py"
_print_pass "app.py is syntactically valid."

# 3. Smoke Test Harness
_print_header "Step 3: smoke_test.py (unittest)"
if python3 "$PROJECT_ROOT/tests/smoke_test.py"; then
    _print_pass "Smoke tests passed."
else
    _print_fail "Smoke tests failed."
    exit 1
fi

# 4. Unresolved Merge state
_print_header "Step 4: Check for unresolved git merge/rebase"
if [ -d "$PROJECT_ROOT/.git" ]; then
    if [ -f "$PROJECT_ROOT/.git/MERGE_HEAD" ] || [ -f "$PROJECT_ROOT/.git/REBASE_HEAD" ] || [ -f "$PROJECT_ROOT/.git/CHERRY_PICK_HEAD" ]; then
        _print_fail "Unresolved git merge/rebase detected (.git/MERGE_HEAD or similar exists)."
        exit 1
    else
        _print_pass "No unresolved git merge/rebase found."
    fi
else
    _print_warn ".git directory not found (skipping git state check)."
fi

# 5. Check for conflict markers
_print_header "Step 5: Check for conflict markers"
# Use ^ to match markers at the beginning of the line to avoid decorative comments
if grep -rnE "^<<<<<<<|^=======|^>>>>>>>" "$PROJECT_ROOT/API" "$PROJECT_ROOT/WebAPP/App" --exclude-dir=__pycache__ > /dev/null 2>&1; then
    _print_fail "Conflict markers (<<<<<<<, =======, >>>>>>>) found in the codebase!"
    grep -rnE "^<<<<<<<|^=======|^>>>>>>>" "$PROJECT_ROOT/API" "$PROJECT_ROOT/WebAPP/App" --exclude-dir=__pycache__
    exit 1
else
    _print_pass "No conflict markers found in key backend/frontend folders."
fi

_print_header "Verification Complete"
_print_pass "Codebase is healthy and ready for upstream pull."
echo ""

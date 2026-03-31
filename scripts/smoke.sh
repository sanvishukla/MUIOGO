#!/usr/bin/env bash
# smoke.sh - Wrapper for the minimal stdlib unittest smoke harness.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Running MUIOGO Smoke Tests..."
python3 "$PROJECT_ROOT/tests/smoke_test.py"

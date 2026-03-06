#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# MUIOGO macOS Test Reset
#
# Removes the local MUIOGO venv, repo .env, demo data installed by setup,
# and Homebrew solver packages so setup can be tested from a clean state.
#
# Usage:
#   ./scripts/reset_macos_test.sh
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="${MUIOGO_VENV_DIR:-$HOME/.venvs/muiogo}"
ENV_FILE="$PROJECT_ROOT/.env"
DEMO_MARKER="$PROJECT_ROOT/WebAPP/DataStorage/.demo_data_installed.json"
DEMO_DIR="$PROJECT_ROOT/WebAPP/DataStorage/CLEWs Demo"

if [ "$(uname -s)" != "Darwin" ]; then
    echo "ERROR: This reset script is for macOS only."
    exit 1
fi

echo "This will remove MUIOGO test state from this Mac:"
echo "  - $VENV_DIR"
echo "  - $ENV_FILE"
echo "  - $DEMO_MARKER"
echo "  - $DEMO_DIR"
if command -v brew >/dev/null 2>&1; then
    echo "  - Homebrew packages glpk and cbc (if installed)"
else
    echo "  - Homebrew solver uninstall will be skipped (brew not found)"
fi
echo
read -r -p "Continue? [y/N]: " reply
case "$reply" in
    [Yy]|[Yy][Ee][Ss]) ;;
    *)
        echo "Cancelled."
        exit 1
        ;;
esac

remove_path() {
    local target="$1"
    if [ -e "$target" ]; then
        rm -rf "$target"
        echo "Removed $target"
    else
        echo "Not present: $target"
    fi
}

remove_path "$VENV_DIR"
remove_path "$ENV_FILE"
remove_path "$DEMO_MARKER"
remove_path "$DEMO_DIR"

if command -v brew >/dev/null 2>&1; then
    if brew list --formula glpk >/dev/null 2>&1; then
        if brew uninstall glpk; then
            echo "Uninstalled Homebrew formula: glpk"
        else
            echo "WARNING: Could not uninstall Homebrew formula: glpk"
        fi
    else
        echo "Homebrew formula not installed: glpk"
    fi

    if brew list --formula cbc >/dev/null 2>&1; then
        if brew uninstall cbc; then
            echo "Uninstalled Homebrew formula: cbc"
        else
            echo "WARNING: Could not uninstall Homebrew formula: cbc"
        fi
    else
        echo "Homebrew formula not installed: cbc"
    fi
fi

echo
if [ -n "${SOLVER_GLPK_PATH:-}" ] || [ -n "${SOLVER_CBC_PATH:-}" ]; then
    echo "NOTE: SOLVER_GLPK_PATH or SOLVER_CBC_PATH is set in the current shell."
fi
echo "Open a NEW terminal before running ./scripts/setup.sh again."

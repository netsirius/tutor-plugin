#!/bin/bash
# MCP Server launcher - uses standard Python venv

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Find Python 3
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: Python 3 not found" >&2
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..." >&2
    "$PYTHON" -m venv "$VENV_DIR"
fi

# Activate and install dependencies if needed
VENV_PYTHON="$VENV_DIR/bin/python"
if [ ! -f "$VENV_DIR/.installed" ]; then
    echo "Installing dependencies..." >&2
    "$VENV_PYTHON" -m pip install --quiet --upgrade pip
    "$VENV_PYTHON" -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
    touch "$VENV_DIR/.installed"
fi

exec "$VENV_PYTHON" "$SCRIPT_DIR/tutor_mcp.py"

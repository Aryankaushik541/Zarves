#!/bin/bash

echo "========================================"
echo "   ZARVES AI AGENT - Auto Installer"
echo "========================================"
echo ""

echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python3 first"
    exit 1
fi
python3 --version
echo "Python found!"
echo ""

echo "[2/4] Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

echo "[3/4] Installing dependencies..."
pip3 install -r requirements.txt
echo ""

echo "[4/4] Installing additional packages..."
pip3 install selenium webdriver-manager
echo ""

echo "========================================"
echo "   Installation Complete!"
echo "========================================"
echo ""
echo "To run Zarves, type:"
echo "    python3 zarves_advanced.py"
echo ""
echo "For help, read QUICK_START.md"
echo ""

# Make script executable
chmod +x install.sh

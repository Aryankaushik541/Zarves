#!/bin/bash

echo "========================================"
echo "   ZARVES AI AGENT - Auto Installer"
echo "========================================"
echo ""

echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python3 first:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi
python3 --version
echo "Python found!"
echo ""

echo "[2/5] Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

echo "[3/5] Installing core dependencies..."
pip3 install pyttsx3 SpeechRecognition selenium webdriver-manager psutil pyautogui requests beautifulsoup4 lxml python-dotenv
echo ""

echo "[4/5] Installing platform-specific packages..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS - Installing macOS packages..."
    pip3 install pyobjc-core pyobjc-framework-Cocoa
    
    # Install PortAudio for PyAudio
    if command -v brew &> /dev/null; then
        echo "Installing PortAudio via Homebrew..."
        brew install portaudio
    fi
else
    # Linux
    echo "Detected Linux - Installing Linux packages..."
    echo "You may need to install system packages:"
    echo "  sudo apt-get install python3-pyaudio portaudio19-dev"
fi
echo ""

echo "[5/5] Installing optional packages..."
echo "Installing PyAudio (may fail - that's okay)..."
pip3 install pyaudio 2>/dev/null || {
    echo ""
    echo "WARNING: PyAudio installation failed."
    echo "Voice recognition will still work but may be less accurate."
    echo ""
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "For better voice support on Linux, run:"
        echo "  sudo apt-get install python3-pyaudio portaudio19-dev"
        echo "  pip3 install pyaudio"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "For better voice support on macOS, run:"
        echo "  brew install portaudio"
        echo "  pip3 install pyaudio"
    fi
    echo ""
}

echo ""
echo "========================================"
echo "   Installation Complete!"
echo "========================================"
echo ""
echo "To run Zarves, type one of these:"
echo "    python3 main.py"
echo "    python3 zarves_pro.py"
echo "    python3 zarves_advanced.py"
echo ""
echo "For help, read README.md"
echo ""
echo "NOTE: Make sure you have a working microphone!"
echo ""

# Make script executable
chmod +x install.sh

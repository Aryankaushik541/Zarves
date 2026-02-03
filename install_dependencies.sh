#!/bin/bash

# JARVIS Dependency Auto-Installer
# Automatically installs all required dependencies

echo "🤖 JARVIS Dependency Installer"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "🔍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
    echo -e "${GREEN}✅ Python3 found${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PIP_CMD=pip
    echo -e "${GREEN}✅ Python found${NC}"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Show Python version
PYTHON_VERSION=$($PYTHON_CMD --version)
echo "   Version: $PYTHON_VERSION"
echo ""

# Check pip
echo "🔍 Checking pip..."
if command -v $PIP_CMD &> /dev/null; then
    echo -e "${GREEN}✅ pip found${NC}"
else
    echo -e "${RED}❌ pip not found. Installing...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade
fi
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
$PIP_CMD install --upgrade pip
echo ""

# Install requirements
echo "📦 Installing Python dependencies..."
echo "   This may take a few minutes..."
echo ""

if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ All dependencies installed successfully!${NC}"
    else
        echo -e "${RED}❌ Some dependencies failed to install${NC}"
        echo -e "${YELLOW}💡 Try manual installation:${NC}"
        echo "   $PIP_CMD install selenium beautifulsoup4 requests webdriver-manager pywhatkit"
    fi
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    echo -e "${YELLOW}💡 Installing core dependencies manually...${NC}"
    $PIP_CMD install ollama selenium beautifulsoup4 requests webdriver-manager pywhatkit
fi
echo ""

# Check Ollama
echo "🔍 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama found${NC}"
    
    # Check if model is pulled
    echo "🔍 Checking for llama3.2 model..."
    if ollama list | grep -q "llama3.2"; then
        echo -e "${GREEN}✅ llama3.2 model found${NC}"
    else
        echo -e "${YELLOW}⚠️  llama3.2 model not found${NC}"
        echo "📥 Pulling llama3.2 model (this may take a few minutes)..."
        ollama pull llama3.2
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo ""
    echo "📥 Installing Ollama..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo -e "${YELLOW}💡 Please install Ollama manually:${NC}"
        echo "   Windows: https://ollama.com/download/windows"
        echo "   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh"
    fi
fi
echo ""

# Check VLC (optional)
echo "🔍 Checking VLC Player (optional for movie playback)..."
if command -v vlc &> /dev/null; then
    echo -e "${GREEN}✅ VLC found${NC}"
else
    echo -e "${YELLOW}⚠️  VLC not found (optional)${NC}"
    echo "💡 Install VLC for movie playback:"
    echo "   Linux: sudo apt install vlc"
    echo "   macOS: brew install --cask vlc"
    echo "   Windows: https://www.videolan.org/vlc/"
fi
echo ""

# Summary
echo "================================"
echo "📊 Installation Summary"
echo "================================"
echo ""

# Test imports
echo "🧪 Testing Python packages..."
$PYTHON_CMD << 'PYEOF'
import sys

packages = {
    'ollama': 'Ollama (LLM)',
    'selenium': 'Selenium (Web Automation)',
    'bs4': 'BeautifulSoup4 (Web Scraping)',
    'requests': 'Requests (HTTP)',
    'pywhatkit': 'PyWhatKit (YouTube)',
}

success = 0
failed = 0

for package, name in packages.items():
    try:
        __import__(package)
        print(f"✅ {name}")
        success += 1
    except ImportError:
        print(f"❌ {name}")
        failed += 1

print(f"\n📊 Results: {success} installed, {failed} missing")

if failed == 0:
    print("\n🎉 All core packages installed successfully!")
    sys.exit(0)
else:
    print(f"\n⚠️  {failed} package(s) missing. Run:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
PYEOF

INSTALL_STATUS=$?

echo ""
echo "================================"

if [ $INSTALL_STATUS -eq 0 ]; then
    echo -e "${GREEN}🎉 Installation Complete!${NC}"
    echo ""
    echo "🚀 Start JARVIS:"
    echo "   $PYTHON_CMD main.py"
    echo ""
    echo "📚 Read guides:"
    echo "   - README.md - Overview"
    echo "   - INSTALLATION.md - Detailed setup"
    echo "   - MOVIE_DOWNLOADER_GUIDE.md - Movie features"
    echo "   - YOUTUBE_AUTO_MUSIC_GUIDE.md - Music features"
else
    echo -e "${YELLOW}⚠️  Installation completed with warnings${NC}"
    echo ""
    echo "💡 Try manual installation:"
    echo "   $PIP_CMD install -r requirements.txt"
    echo ""
    echo "🆘 Need help? Check INSTALLATION.md"
fi

echo "================================"

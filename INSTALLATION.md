# 🚀 JARVIS Installation Guide

Complete step-by-step installation guide for JARVIS AI Assistant.

---

## 📋 Prerequisites

### 1. Python 3.8+
```bash
# Check Python version
python --version
# or
python3 --version

# Should show: Python 3.8.x or higher
```

### 2. Git
```bash
# Check Git
git --version
```

### 3. VLC Player (for movie playback)
- **Windows**: https://www.videolan.org/vlc/download-windows.html
- **macOS**: https://www.videolan.org/vlc/download-macosx.html
- **Linux**: `sudo apt install vlc`

---

## 🔧 Installation Steps

### Step 1: Clone Repository
```bash
# Clone the repo
git clone https://github.com/Aryankaushik541/Zarves.git

# Navigate to directory
cd Zarves
```

### Step 2: Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# OR if you have pip3
pip3 install -r requirements.txt
```

**Common packages installed:**
- `ollama` - Local LLM
- `selenium` - Web automation (movie downloader)
- `beautifulsoup4` - Web scraping
- `pywhatkit` - YouTube automation
- `requests` - HTTP requests
- `PyQt5` - GUI (optional)
- And more...

### Step 3: Install Ollama (Local LLM)
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from: https://ollama.com/download/windows
```

### Step 4: Pull LLM Model
```bash
# Start Ollama service
ollama serve

# In another terminal, pull model
ollama pull llama3.2

# OR pull a larger model for better performance
ollama pull llama3.1
```

### Step 5: Setup Environment (Optional)
```bash
# Copy template
cp .env.template .env

# Edit .env file
nano .env

# Add your configurations:
# OLLAMA_HOST=http://localhost:11434
# OLLAMA_MODEL=llama3.2
```

### Step 6: Run JARVIS!
```bash
# Start JARVIS
python main.py

# OR
python3 main.py
```

---

## 🎯 Quick Install (One Command)

### Linux/macOS
```bash
git clone https://github.com/Aryankaushik541/Zarves.git && \
cd Zarves && \
pip install -r requirements.txt && \
curl -fsSL https://ollama.com/install.sh | sh && \
ollama pull llama3.2 && \
python main.py
```

### Windows (PowerShell)
```powershell
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
pip install -r requirements.txt
# Download Ollama from: https://ollama.com/download/windows
# Then run: ollama pull llama3.2
python main.py
```

---

## 🛠️ Troubleshooting

### Issue 1: "No module named 'selenium'"
```bash
pip install selenium webdriver-manager
```

### Issue 2: "No module named 'pywhatkit'"
```bash
pip install pywhatkit
```

### Issue 3: "Ollama connection refused"
```bash
# Start Ollama service
ollama serve

# In another terminal
python main.py
```

### Issue 4: "Model not found"
```bash
# Pull the model
ollama pull llama3.2

# Check available models
ollama list
```

### Issue 5: "VLC player not found"
**Windows:**
1. Download: https://www.videolan.org/vlc/
2. Install to default location
3. Restart JARVIS

**Linux:**
```bash
sudo apt install vlc
```

**macOS:**
```bash
brew install --cask vlc
```

### Issue 6: "ChromeDriver not found"
```bash
# Auto-installs via webdriver-manager
pip install webdriver-manager

# Or manual install
# Download from: https://chromedriver.chromium.org/
```

### Issue 7: "PyAudio installation failed"
**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

---

## 📦 Optional Dependencies

### For Voice Recognition
```bash
pip install SpeechRecognition pyaudio
```

### For Text-to-Speech
```bash
pip install pyttsx3
```

### For GUI
```bash
pip install PyQt5
```

### For Advanced Features
```bash
# Computer vision
pip install opencv-python

# Screen automation
pip install pyautogui

# System monitoring
pip install psutil
```

---

## 🔍 Verify Installation

### Check All Dependencies
```bash
# Create a test script
cat > test_install.py << 'EOF'
import sys

packages = [
    'ollama',
    'selenium',
    'beautifulsoup4',
    'pywhatkit',
    'requests',
]

print("🔍 Checking dependencies...\n")

for package in packages:
    try:
        __import__(package)
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - NOT INSTALLED")

print("\n✅ All checks complete!")
EOF

# Run test
python test_install.py
```

### Test JARVIS
```bash
# Start JARVIS
python main.py

# Try commands:
# - "hello jarvis"
# - "youtube kholo"
# - "google search python"
```

---

## 🚀 Performance Optimization

### Use Faster Model
```bash
# Smaller, faster model
ollama pull llama3.2:1b

# Update .env
OLLAMA_MODEL=llama3.2:1b
```

### GPU Acceleration (NVIDIA)
```bash
# Ollama automatically uses GPU if available
# Check GPU usage:
nvidia-smi
```

### Reduce Memory Usage
Edit `core/engine.py`:
```python
# Line ~75
self.max_iterations = 3  # Reduce from 5
```

---

## 📱 Platform-Specific Notes

### Windows
- Install Visual C++ Redistributable if needed
- Run as Administrator for system control features
- Windows Defender may flag some automation features

### macOS
- Grant accessibility permissions for automation
- Install Xcode Command Line Tools: `xcode-select --install`
- Allow Terminal in System Preferences > Security

### Linux
- Install `xdotool` for window management: `sudo apt install xdotool`
- Grant permissions: `chmod +x main.py`
- Some features may need `sudo`

---

## 🔄 Update JARVIS

```bash
# Navigate to directory
cd Zarves

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart JARVIS
python main.py
```

---

## 📚 Next Steps

After installation:

1. **Read Guides:**
   - `README.md` - Overview
   - `MOVIE_DOWNLOADER_GUIDE.md` - Movie features
   - `YOUTUBE_AUTO_MUSIC_GUIDE.md` - Music features
   - `OLLAMA_SETUP.md` - LLM setup

2. **Try Features:**
   - YouTube automation
   - Movie downloader
   - Google search
   - System control

3. **Customize:**
   - Edit `.env` for settings
   - Modify `skill/` for new features
   - Update `core/engine.py` for behavior

---

## 🆘 Getting Help

### Check Logs
```bash
# JARVIS shows detailed logs in terminal
# Look for error messages and warnings
```

### Common Solutions
1. **Restart Ollama**: `ollama serve`
2. **Reinstall Dependencies**: `pip install -r requirements.txt --force-reinstall`
3. **Clear Cache**: Delete `__pycache__` folders
4. **Update Python**: Use Python 3.8+

### Report Issues
- GitHub Issues: https://github.com/Aryankaushik541/Zarves/issues
- Include error logs and system info

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Ollama installed and running
- [ ] Model pulled (`ollama pull llama3.2`)
- [ ] VLC player installed (for movies)
- [ ] JARVIS runs successfully (`python main.py`)
- [ ] Basic commands work

---

**Made with ❤️ by JARVIS AI**

Need help? Check the guides or open an issue!

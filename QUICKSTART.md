# 🚀 JARVIS Quick Start Guide

Apne PC par JARVIS ko 5 minutes mein setup karo!

---

## 📋 Prerequisites

### Required:
- ✅ Python 3.8+ installed
- ✅ Microphone (for voice commands)
- ✅ Internet connection
- ✅ Windows/Mac/Linux

### Optional (for better performance):
- 🎮 NVIDIA GPU (for faster AI)
- 💾 8GB+ RAM
- 🎤 Good quality microphone

---

## ⚡ 5-Minute Setup

### Step 1: Download JARVIS
```bash
# Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Switch to fixed version
git checkout fix-wake-word-detection
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# For GPU support (NVIDIA only)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Step 4: Setup API Key
```bash
# Copy template
cp .env.template .env

# Edit .env file and add your GROQ API key
# Get free key from: https://console.groq.com/keys
```

Edit `.env`:
```
GROQ_API_KEY=your_api_key_here
```

### Step 5: Test Installation
```bash
# Run test script
python test_fixes.py
```

Expected output:
```
✅ All imports successful
✅ All wake word tests passed!
✅ Hardware detection successful
✅ GROQ_API_KEY found
```

### Step 6: Run JARVIS
```bash
python main.py
```

---

## 🎤 First Commands

### Test Wake Word:
Say: **"Jarvis, hello"**

Expected response:
```
Listening...
Recognizing...
Hindi: जार्विस हैलो
✅ Command detected: hello
JARVIS: Hello! How can I help you?
```

### Open YouTube:
Say: **"Jarvis, YouTube kholo"**

Expected: YouTube opens in browser

### Play Music:
Say: **"Jarvis, gaana bajao"**

Expected: Music player opens

### Check Time:
Say: **"Jarvis, time kya hua?"**

Expected: JARVIS tells current time

---

## 🐛 Common Issues & Fixes

### Issue 1: "No wake word detected"
**Problem:** JARVIS ignores your commands

**Solution:**
```bash
# Test microphone
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

# Make sure to say "Jarvis" first
# Correct: "Jarvis, YouTube kholo"
# Wrong: "YouTube kholo"
```

### Issue 2: "Microphone not found"
**Problem:** PyAudio installation failed

**Solution (Windows):**
```bash
# Download PyAudio wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# Install wheel (replace with your Python version)
pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl
```

**Solution (Mac):**
```bash
brew install portaudio
pip install pyaudio
```

**Solution (Linux):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Issue 3: "GROQ_API_KEY not found"
**Problem:** API key missing

**Solution:**
```bash
# 1. Get free API key from: https://console.groq.com/keys
# 2. Create .env file
cp .env.template .env

# 3. Edit .env and add:
GROQ_API_KEY=gsk_your_actual_key_here
```

### Issue 4: "CUDA not available" (GPU users)
**Problem:** GPU not detected

**Solution:**
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Issue 5: Hindi not recognized
**Problem:** Voice recognition fails for Hindi

**Solution (Windows):**
```
1. Open Settings
2. Go to Time & Language → Language
3. Add Hindi language pack
4. Restart JARVIS
```

---

## 📝 Command Examples

### Basic Commands:
```
✅ "Jarvis, YouTube kholo"
✅ "Jarvis, Chrome chalu karo"
✅ "Jarvis, Notepad band karo"
✅ "Jarvis, Calculator dikha do"
```

### Music & Video:
```
✅ "Jarvis, gaana bajao"
✅ "Jarvis, video chala do"
✅ "Jarvis, music roko"
```

### Search:
```
✅ "Jarvis, Google pe dhundho AI news"
✅ "Jarvis, YouTube pe search karo Python tutorial"
```

### System:
```
✅ "Jarvis, volume badha do"
✅ "Jarvis, screenshot le lo"
✅ "Jarvis, time batao"
✅ "Jarvis, weather kaisa hai?"
```

### Shutdown:
```
✅ "Jarvis, band karo"
✅ "Jarvis, quit"
✅ "Jarvis, bye"
```

---

## 🎯 Tips for Best Experience

### 1. Clear Pronunciation
- Speak clearly and at normal pace
- Say "Jarvis" first, then pause briefly
- Example: "Jarvis, [pause] YouTube kholo"

### 2. Quiet Environment
- Reduce background noise
- Use good quality microphone
- Adjust microphone sensitivity in Windows settings

### 3. Natural Language
- Use Hinglish freely
- Mix Hindi and English
- JARVIS understands both!

### 4. Command Structure
```
✅ Good: "Jarvis, YouTube kholo"
✅ Good: "Jarvis, open YouTube"
✅ Good: "जार्विस, यूट्यूब खोलो"

❌ Bad: "YouTube kholo" (no wake word)
❌ Bad: "Open YouTube Jarvis" (wake word at end)
```

---

## 🔧 Advanced Setup

### Enable GPU Acceleration (NVIDIA):
```bash
# Install CUDA toolkit from: https://developer.nvidia.com/cuda-downloads
# Then install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Enable Intel NPU (Core Ultra):
```bash
pip install intel-extension-for-pytorch
```

### Enable AMD GPU (ROCm):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6
```

---

## 📊 Verify Installation

Run comprehensive test:
```bash
python test_fixes.py
```

Expected output:
```
✅ Imports
✅ Wake Word Detection
✅ Hardware Detection
✅ Indian Language
✅ PyTorch
✅ Speech Recognition
✅ Text-to-Speech
✅ Environment
```

---

## 🎉 Success!

You should see:
```
🔍 Detecting hardware...
✅ Detected: NVIDIA GeForce RTX 3060
   CUDA Version: 11.8

============================================================
🤖 JARVIS - Autonomous AI Assistant
⚡ NPU-Accelerated for Omen PC
🇮🇳 Natural Indian Language Support
============================================================

JARVIS: Jarvis Online. Ready for command.
🎤 Voice mode active. Say 'Jarvis' followed by your command.
💡 Natural Indian language supported!
   Examples: 'Jarvis, YouTube kholo', 'Jarvis, gaana bajao'

Listening...
```

---

## 📚 Next Steps

1. **Read Full Documentation:**
   - `README.md` - Complete features
   - `FIXES.md` - Troubleshooting guide
   - `INDIAN_LANGUAGE_GUIDE.md` - Language support

2. **Explore Skills:**
   ```bash
   ls skill/
   ```

3. **Add Custom Skills:**
   - See `skill/` directory for examples
   - Create your own skills

4. **Join Community:**
   - Star the repo ⭐
   - Report issues
   - Contribute improvements

---

## 🆘 Need Help?

### Quick Diagnostics:
```bash
# Test wake word
python -c "from core.voice import detect_wake_word; print(detect_wake_word('Jarvis hello'))"

# Test hardware
python -c "from core.npu_accelerator import npu_accelerator; npu_accelerator.print_status()"

# Test microphone
python -c "import speech_recognition as sr; r = sr.Recognizer(); m = sr.Microphone(); print('Say something...'); audio = r.listen(m.__enter__()); print(r.recognize_google(audio, language='hi-IN'))"
```

### Still Having Issues?
1. Check `FIXES.md` for detailed troubleshooting
2. Run `python test_fixes.py` for diagnostics
3. Create GitHub issue with error logs
4. Include output of test script

---

## ✅ Checklist

Before asking for help, verify:
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] GROQ_API_KEY set in `.env`
- [ ] Microphone working
- [ ] Test script passes (`python test_fixes.py`)
- [ ] Wake word "Jarvis" spoken clearly

---

**Happy Jarvis-ing! 🚀**

Agar koi problem ho, toh `FIXES.md` dekho ya GitHub issue create karo.

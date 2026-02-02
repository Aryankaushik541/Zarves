# 🔧 JARVIS Fixes - Wake Word & Hardware Detection

## 🎯 Problems Fixed

### 1. ✅ Wake Word Detection Issue
**Problem:** JARVIS samajh nahi raha tha jab aap "Jarvis" bolte the
- Voice recognition "जार्विस" (Hindi) return kar raha tha
- Code "jarvis" (English) dhundh raha tha
- Match nahi ho raha tha

**Solution:** 
- Ab dono Hindi aur English "Jarvis" detect hota hai
- Devanagari script support added
- Case-insensitive matching

### 2. ✅ Hardware Auto-Detection
**Problem:** NPU/GPU properly detect nahi ho raha tha
- Manual configuration required tha
- Errors aa rahe the

**Solution:**
- Automatic detection with PyTorch
- Priority order: NVIDIA GPU → AMD GPU → Intel NPU → Apple Silicon → CPU
- Graceful fallback to CPU

### 3. ✅ Indian Language Support
**Problem:** Hinglish commands properly samajh nahi aa rahe the

**Solution:**
- Comprehensive Hinglish dictionary
- Natural language processing
- Common variations support

---

## 🚀 Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Basic dependencies
pip install -r requirements.txt

# For GPU support (NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For Intel NPU support
pip install intel-extension-for-pytorch

# For AMD GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6
```

### Step 4: Setup API Key
```bash
# Copy template
cp .env.template .env

# Edit .env and add your GROQ API key
# Get free key from: https://console.groq.com/keys
```

### Step 5: Test Microphone
```bash
# Test if microphone works
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('Microphone test...'); print(sr.Microphone.list_microphone_names())"
```

### Step 6: Run JARVIS
```bash
python main.py
```

---

## 🎤 Wake Word Usage

### ✅ Working Examples:

**English:**
- "Jarvis, open YouTube"
- "Jarvis, play music"
- "Jarvis, what's the time?"

**Hindi:**
- "जार्विस, YouTube खोलो"
- "जार्विस, गाना बजाओ"
- "जार्विस, समय क्या हुआ?"

**Hinglish:**
- "Jarvis, YouTube kholo"
- "Jarvis, gaana bajao"
- "Jarvis, time kya hua?"

### ❌ Common Mistakes:

**Wrong:**
- "YouTube kholo" (no wake word)
- "Open YouTube Jarvis" (wake word at end)

**Correct:**
- "Jarvis, YouTube kholo" ✅
- "Jarvis open YouTube" ✅

---

## 🖥️ Hardware Detection

### Automatic Detection Order:
1. **NVIDIA GPU (CUDA)** - Best for AI tasks
2. **AMD GPU (ROCm)** - Good for AI tasks
3. **Intel NPU** - Efficient for laptops
4. **Apple Silicon (MPS)** - For Mac M1/M2/M3
5. **CPU** - Fallback (works everywhere)

### Check Your Hardware:
```python
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

### Expected Output:
```
🔍 Detecting hardware...
✅ Detected: NVIDIA GeForce RTX 3060
   CUDA Version: 11.8

🔧 NPU Accelerator Status
============================================================
Device: CUDA
NPU Type: GPU (NVIDIA CUDA)
Acceleration: ✅ Enabled
CPU Cores: 16
Total RAM: 15.29 GB
GPU Memory: 6.0 GB
```

---

## 🐛 Troubleshooting

### Problem: "No wake word detected"
**Solution:**
```bash
# Check if voice recognition works
python -c "import speech_recognition as sr; r = sr.Recognizer(); m = sr.Microphone(); print('Say something...'); audio = r.listen(m.__enter__()); print(r.recognize_google(audio, language='hi-IN'))"
```

### Problem: "Microphone not found"
**Solution:**
```bash
# Install PyAudio
pip install pyaudio

# If error on Windows, download wheel:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl
```

### Problem: "CUDA not available"
**Solution:**
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

### Problem: "Hindi not recognized"
**Solution:**
```bash
# Windows: Install Hindi language pack
# Settings → Time & Language → Language → Add Hindi

# Test Hindi recognition
python -c "import speech_recognition as sr; r = sr.Recognizer(); m = sr.Microphone(); audio = r.listen(m.__enter__()); print(r.recognize_google(audio, language='hi-IN'))"
```

---

## 📝 Testing Commands

### Test Wake Word Detection:
```bash
# Say: "Jarvis, YouTube kholo"
# Expected: ✅ Command detected: youtube kholo
```

### Test Hardware Detection:
```bash
python -c "from core.npu_accelerator import npu_accelerator; npu_accelerator.print_status()"
```

### Test Indian Language:
```bash
python core/indian_language.py
```

---

## 🎯 Quick Commands Reference

### Apps:
- "Jarvis, YouTube kholo"
- "Jarvis, Chrome chalu karo"
- "Jarvis, Notepad band karo"
- "Jarvis, Calculator dikha do"

### Music/Video:
- "Jarvis, gaana bajao"
- "Jarvis, video chala do"
- "Jarvis, music roko"

### Search:
- "Jarvis, Google pe dhundho"
- "Jarvis, YouTube pe search karo"

### System:
- "Jarvis, volume badha do"
- "Jarvis, screenshot le lo"
- "Jarvis, time batao"

### Shutdown:
- "Jarvis, band karo"
- "Jarvis, quit"
- "Jarvis, bye"

---

## 🔄 Update to Latest Fixes

```bash
# Pull latest changes
git fetch origin
git checkout fix-wake-word-detection
git pull origin fix-wake-word-detection

# Reinstall dependencies
pip install -r requirements.txt

# Run JARVIS
python main.py
```

---

## 📞 Support

### Issues?
1. Check this guide first
2. Run diagnostics: `python -c "from core.self_healing import self_healing; self_healing.run_diagnostics()"`
3. Create GitHub issue with error logs

### Working?
- Star the repo ⭐
- Share with friends
- Contribute improvements

---

## 🎉 Success Indicators

You'll know it's working when you see:

```
✅ Detected: NVIDIA GeForce RTX 3060
✅ Using GPU acceleration
🎤 Voice mode active. Say 'Jarvis' followed by your command.
💡 Natural Indian language supported!

Listening...
Recognizing...
Hindi: जार्विस यूट्यूब खोलो
✅ Command detected: youtube kholo
JARVIS: Opening YouTube...
```

---

**Happy Coding! 🚀**

Agar koi problem ho, toh GitHub issue create karo ya documentation check karo.

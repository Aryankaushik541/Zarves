# 🔧 JARVIS Fixes - Complete Guide

## Problem: JARVIS Engine Not Initialized

Your JARVIS is running in **demo mode** because the core engine isn't initializing properly.

---

## ✅ Quick Fix (5 Minutes)

### **Step 1: Install Ollama (Required)**

JARVIS uses Ollama for local AI. Install it:

**Windows:**
```bash
# Download and install from:
https://ollama.com/download/windows

# After installation, open PowerShell and run:
ollama serve
```

**Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

### **Step 2: Pull AI Model**

Open a **new terminal** (keep `ollama serve` running) and run:

```bash
ollama pull llama3.2
```

This downloads the AI model (~2GB). Wait for it to complete.

### **Step 3: Install Python Dependencies**

```bash
cd Zarves
pip install -r requirements.txt
```

### **Step 4: Run JARVIS**

```bash
python main.py
```

**Expected Output:**
```
✅ Connected to Ollama at http://localhost:11434
✅ Using model: llama3.2
🚀 Launching JARVIS GUI...
```

---

## 🔍 Troubleshooting

### **Issue 1: "Ollama connection issue"**

**Solution:**
```bash
# Make sure Ollama is running:
ollama serve

# In another terminal:
ollama list  # Should show llama3.2
```

### **Issue 2: "Module not found"**

**Solution:**
```bash
# Reinstall dependencies:
pip install --upgrade -r requirements.txt

# If PyQt5 fails on Mac:
pip install PyQt5 --no-cache-dir
```

### **Issue 3: "JARVIS core not available"**

**Solution:**
```bash
# Check if core folder exists:
ls core/

# Should show:
# engine.py, registry.py, voice.py, etc.

# If missing, re-clone the repo:
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

### **Issue 4: Still in Demo Mode**

**Solution:**
```bash
# Check Ollama status:
curl http://localhost:11434/api/tags

# Should return JSON with models
# If not, restart Ollama:
pkill ollama
ollama serve
```

---

## 🚀 Advanced: Use Cloud AI (No Ollama Needed)

If you can't install Ollama, switch to cloud AI:

### **Option 1: Use Groq (Free & Fast)**

1. Get API key from: https://console.groq.com/keys

2. Create `.env` file:
```bash
GROQ_API_KEY=your_key_here
USE_GROQ=true
```

3. Install groq:
```bash
pip install groq
```

### **Option 2: Use OpenAI**

1. Get API key from: https://platform.openai.com/api-keys

2. Create `.env` file:
```bash
OPENAI_API_KEY=your_key_here
USE_OPENAI=true
```

3. Install openai:
```bash
pip install openai
```

---

## 📝 Configuration File

Create `.env` in project root:

```bash
# AI Model (choose one)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OR use cloud AI
# GROQ_API_KEY=your_key
# USE_GROQ=true

# Voice Settings
VOICE_ENABLED=true
VOICE_RATE=150
VOICE_VOLUME=0.9

# Auto-Login (Optional)
GOOGLE_EMAIL=your_email@gmail.com
GOOGLE_PASSWORD=your_password

# Movie Search Paths (Optional)
MOVIE_PATHS=C:\Users\YourName\Videos,D:\Movies
```

---

## ✅ Verification

After fixes, you should see:

```
[08:58:46] ⚙️ SYSTEM: ✅ JARVIS core initialized
[08:58:47] 🤖 JARVIS: ✅ Engine ready
[08:58:48] 🤖 JARVIS: 📦 Loaded 15 skills
[08:58:49] 🤖 JARVIS: 🎯 45 tools available
[08:58:50] 🤖 JARVIS: ✅ Ready to assist!
```

---

## 🆘 Still Not Working?

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Check logs:**
   ```bash
   # Look for error details in terminal
   python main.py 2>&1 | tee jarvis.log
   ```

3. **Reset everything:**
   ```bash
   # Remove config
   rm ~/.jarvis_config.json
   
   # Reinstall
   pip uninstall -y -r requirements.txt
   pip install -r requirements.txt
   
   # Restart Ollama
   pkill ollama
   ollama serve
   ollama pull llama3.2
   ```

4. **Create GitHub issue:**
   - Go to: https://github.com/Aryankaushik541/Zarves/issues
   - Include: Error message, OS, Python version
   - Attach: `jarvis.log` file

---

## 🎯 Quick Test

After fixes, test with:

```python
# In Python console:
from core.registry import SkillRegistry
from core.engine import JarvisEngine

registry = SkillRegistry()
engine = JarvisEngine(registry)

# Should print:
# ✅ Connected to Ollama
# ✅ Using model: llama3.2
```

If this works, JARVIS is ready! 🎉

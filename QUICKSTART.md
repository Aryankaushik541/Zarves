# ⚡ JARVIS Quick Start - 2 Minutes!

Get JARVIS running in just 2 minutes with ONE command!

---

## 🎯 The Fastest Way - Just 2 Commands!

```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Run (everything auto-installs!)
python main.py
```

**That's literally it!** 🎉

---

## 📺 What Happens

```
🤖 JARVIS - Personal AI Assistant
======================================================================

📦 Checking Python dependencies...
   ✅ All dependencies installed!

🤖 Setting up AI Engine (Ollama)...
```

### **If Ollama Not Installed:**

```
   ⚠️  Ollama not found!

   Install Ollama now? (y/n): 
```

**Just type `y` and press Enter!**

- **Mac/Linux:** Installs automatically
- **Windows:** Opens download link, you install, press Enter

### **If Model Not Downloaded:**

```
   ⚠️  AI model (llama3.2) not found

   Download model now? (y/n): 
```

**Just type `y` and press Enter!**

Downloads ~2GB model (takes 2-5 minutes).

### **Then:**

```
✅ AI Engine ready!

🚀 Launching JARVIS GUI...

💡 Full Mode Enabled:
   ✅ Local AI processing
   ✅ Natural conversations
   ✅ Smart task execution

🎵 Features:
   ✅ YouTube Auto-Play
   ✅ Browser Auto-Login
   ✅ PC Movie Search
   ✅ VLC Auto-Play
   ✅ Voice & Text Control
```

**Beautiful GUI opens!** 🎨

---

## 🔍 Troubleshooting

### **Error: "Ollama installation failed"**

**Windows:**
1. Download: https://ollama.com/download/windows
2. Install it
3. Run `python main.py` again

**Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
python main.py
```

### **Error: "Model download failed"**

```bash
# Terminal 1:
ollama serve

# Terminal 2:
ollama pull llama3.2

# Terminal 3:
cd Zarves
python main.py
```

### **Error: "Module not found"**

```bash
pip install -r requirements.txt
python main.py
```

---

## ✅ Verify It's Working

You should see:
```
✅ AI Engine ready!
🚀 Launching JARVIS GUI...
```

Then a beautiful GUI window opens!

---

## 🎮 Try These Commands

Once JARVIS is running, try:

1. **"Hello JARVIS"** - Test conversation
2. **"youtube kholo"** - Opens YouTube
3. **"gmail kholo"** - Opens Gmail
4. **"volume badhao"** - Increases volume
5. **"calculator kholo"** - Opens calculator
6. **"Avengers movie search karo"** - Searches PC for movies

---

## 💡 Pro Tips

### **Skip Ollama (Limited Mode):**

If you don't want to install Ollama:
```
Install Ollama now? (y/n): n
```

JARVIS will run in limited mode (basic commands only).

### **Install Later:**

You can always install Ollama later:
```bash
# Install Ollama
# Windows: https://ollama.com/download/windows
# Mac/Linux: curl -fsSL https://ollama.com/install.sh | sh

# Start server
ollama serve

# Download model
ollama pull llama3.2

# Restart JARVIS
python main.py
```

---

## 🆘 Still Not Working?

See detailed troubleshooting: [FIXES.md](FIXES.md)

Or create an issue: https://github.com/Aryankaushik541/Zarves/issues

---

## 📚 Next Steps

Once JARVIS is running:

1. **Configure Auto-Login:**
   - Click "⚙️ Settings"
   - Add your Google credentials
   - Save

2. **Add Movie Folders:**
   - Click "⚙️ Settings"
   - Add your movie directories
   - Save

3. **Explore Commands:**
   - See full list: [README.md](README.md#-commands)

---

**That's it! Enjoy JARVIS! 🤖**

**Remember: Just run `python main.py` - everything else is automatic!**

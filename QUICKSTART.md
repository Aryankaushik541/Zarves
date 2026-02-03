# ⚡ JARVIS Quick Start - 5 Minutes

Get JARVIS running in 5 minutes!

---

## 🎯 The Fastest Way

### **Windows:**
```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Run (automatically installs everything)
start_jarvis.bat
```

### **Mac/Linux:**
```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Make executable and run
chmod +x start_jarvis.sh
./start_jarvis.sh
```

**Done!** JARVIS GUI will open automatically! 🎉

---

## 🔍 What If It Doesn't Work?

### **Error: "Ollama not found"**

**Fix:**
1. Install Ollama: https://ollama.com/download
2. Restart the script

### **Error: "JARVIS engine not initialized"**

**Fix:**
```bash
# Open terminal 1:
ollama serve

# Open terminal 2:
ollama pull llama3.2

# Open terminal 3:
cd Zarves
python main.py
```

### **Error: "Module not found"**

**Fix:**
```bash
pip install -r requirements.txt
python main.py
```

---

## ✅ Verify It's Working

You should see:
```
✅ Connected to Ollama at http://localhost:11434
✅ Using model: llama3.2
🚀 Launching JARVIS GUI...
```

Then a beautiful GUI window opens!

---

## 🎮 Try These Commands

Once JARVIS is running, try:

1. **"Hello JARVIS"** - Test basic conversation
2. **"youtube kholo"** - Opens YouTube
3. **"gmail kholo"** - Opens Gmail
4. **"volume badhao"** - Increases volume
5. **"calculator kholo"** - Opens calculator

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

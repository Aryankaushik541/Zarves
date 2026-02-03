# ⚡ JARVIS Quick Start Guide

## 🚀 Super Easy Setup (3 Steps!)

JARVIS ab **automatically** sab kuch install kar dega! Bas 3 steps:

---

## Step 1: Install Ollama

### Windows
```
Download from: https://ollama.com/download/windows
```

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## Step 2: Clone Repository
```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

---

## Step 3: Run JARVIS!
```bash
python main.py
```

**That's it!** 🎉

JARVIS automatically:
- ✅ Checks all dependencies
- ✅ Installs missing packages (selenium, pywhatkit, etc.)
- ✅ Downloads Ollama model (llama3.2)
- ✅ Creates .env file
- ✅ Starts running!

---

## 🎯 What Happens on First Run

```
🤖 JARVIS Startup Checks
======================================================================

🔍 Checking required packages...
   ❌ selenium - MISSING
   ❌ pywhatkit - MISSING
   ❌ beautifulsoup4 - MISSING

📦 Found 3 missing required package(s)
🔧 Auto-installing missing packages...

📋 Installing from requirements.txt...
   This may take a few minutes on first run...
✅ All dependencies installed successfully!

🔍 Checking Ollama...
   ✅ Ollama installed
   ⚠️  llama3.2 model not found

📥 Pulling llama3.2 model...
   This may take a few minutes (one-time download)...
   ✅ Model downloaded successfully!

✅ Startup checks complete!

🤖 JARVIS - Your Autonomous AI Assistant
======================================================================
🎤 JARVIS is listening...
```

---

## 💬 Try These Commands

After JARVIS starts:

### YouTube & Music
```
👤 You: youtube kholo
🤖 JARVIS: 🎵 Playing trending song: Tauba Tauba Bad Newz

👤 You: gaana bajao
🤖 JARVIS: 🎵 Auto-selected: Kesariya Brahmastra

👤 You: play Kesariya on youtube
🤖 JARVIS: 🎵 Playing: Kesariya
```

### Movie Download
```
👤 You: vegamovies se Inception download karo
🤖 JARVIS: 
🎬 Movie Downloader & Player
============================================================
Movie: Inception
Website: https://vegamovies.attorney/
Quality: 720p
============================================================
🔍 Searching for 'Inception'...
✅ Found: Inception (2010)
⬇️  Downloading...
✅ Download complete!
🎥 Opening in VLC player...
```

### Web Search
```
👤 You: google search python
🤖 JARVIS: ✅ Opened Google search for: python

👤 You: open youtube.com
🤖 JARVIS: ✅ Opened: https://youtube.com
```

### General Chat
```
👤 You: hello jarvis
🤖 JARVIS: Hello! How can I help you today?

👤 You: what can you do?
🤖 JARVIS: I can:
- Play music on YouTube (trending or specific songs)
- Download movies from websites
- Search Google
- Open websites
- And much more!
```

---

## 🛠️ Troubleshooting

### Issue: "Ollama connection refused"
```bash
# Start Ollama in separate terminal
ollama serve

# Then run JARVIS in another terminal
python main.py
```

### Issue: "Dependencies still missing after auto-install"
```bash
# Restart JARVIS
python main.py

# OR manually install
pip install -r requirements.txt
```

### Issue: "Model not found"
```bash
# Pull model manually
ollama pull llama3.2

# Then restart JARVIS
python main.py
```

---

## 📋 What Gets Auto-Installed

When you run `python main.py`, JARVIS automatically installs:

### Required Packages
- ✅ `ollama` - Local LLM
- ✅ `selenium` - Web automation (movie downloader)
- ✅ `beautifulsoup4` - Web scraping
- ✅ `requests` - HTTP requests
- ✅ `pywhatkit` - YouTube automation
- ✅ `webdriver-manager` - ChromeDriver auto-install
- ✅ `SpeechRecognition` - Voice input
- ✅ `pyttsx3` - Text-to-speech
- ✅ `python-dotenv` - Environment variables

### Optional Packages
- ⚠️ `PyQt5` - GUI (optional)
- ⚠️ `opencv-python` - Computer vision (optional)
- ⚠️ `pyautogui` - Screen automation (optional)

---

## 🎉 Success Indicators

You'll know JARVIS is ready when you see:

```
✅ All required packages are installed!

🔍 Checking Ollama...
   ✅ Ollama installed
   ✅ llama3.2 model found

✅ Startup checks complete!

🤖 JARVIS - Your Autonomous AI Assistant
======================================================================
✅ Loaded 8 skills
✅ JARVIS ready!

🎤 JARVIS is listening...
======================================================================

👤 You: _
```

---

## 🔄 Update JARVIS

To get latest features:

```bash
cd Zarves
git pull origin main
python main.py  # Auto-installs any new dependencies
```

---

## 📚 Learn More

- **README.md** - Full overview
- **INSTALLATION.md** - Detailed setup
- **MOVIE_DOWNLOADER_GUIDE.md** - Movie features
- **YOUTUBE_AUTO_MUSIC_GUIDE.md** - Music features
- **OLLAMA_SETUP.md** - LLM configuration

---

## 💡 Pro Tips

1. **First Run**: Takes 2-5 minutes (downloads model + installs packages)
2. **Subsequent Runs**: Starts in seconds
3. **Ollama Server**: Keep `ollama serve` running in background
4. **Updates**: Just `git pull` and run - auto-installs new dependencies

---

## ✅ Quick Checklist

- [ ] Ollama installed
- [ ] Repository cloned
- [ ] Run `python main.py`
- [ ] Wait for auto-install (first time only)
- [ ] Start using JARVIS!

---

**That's it! JARVIS handles everything else automatically!** 🚀

No manual pip installs, no configuration files, no complex setup.

Just run and go! 🎉

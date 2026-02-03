# 🤖 JARVIS - Autonomous AI That Fixes & Installs Itself

> **"I don't just assist. I auto-install dependencies, fix my own code, play trending songs, and evolve myself."**

JARVIS is an **advanced autonomous AI** that can:
- ✅ **AUTO-INSTALLS EVERYTHING** - Just run `python main.py` and it handles the rest!
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **Internet-Powered Self-Healing** - Searches web + uses AI to fix its own errors
- ✅ **Trending Music** - Plays latest viral songs from YouTube automatically
- ✅ **Movie Downloader** - Download and play movies with VLC
- ✅ **Real-time Web Search** - Fetches live data from internet
- ✅ **Auto-heal errors** using Ollama AI + StackOverflow solutions
- ✅ **Control your entire system** with natural language (Windows/Mac/Linux)
- ✅ **Understand Hinglish** - speak naturally in Hindi or English

---

## ⚡ Super Quick Start (3 Steps!)

### **Step 1: Install Ollama**

```bash
# Windows
https://ollama.com/download/windows

# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### **Step 2: Clone Repository**

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

### **Step 3: Run JARVIS!**

```bash
python main.py
```

**That's it!** 🎉

JARVIS automatically:
- ✅ Checks all dependencies (selenium, pywhatkit, beautifulsoup4, etc.)
- ✅ Installs missing packages from requirements.txt
- ✅ Downloads Ollama model (llama3.2) if needed
- ✅ Creates .env configuration file
- ✅ Starts running!

**First run takes 2-5 minutes** (downloads model + installs packages)  
**Subsequent runs start in seconds!**

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
✅ Loaded 8 skills
✅ JARVIS ready!

🎤 JARVIS is listening...
```

---

## 🌟 Key Features

### 🔧 **Auto-Install Everything**
- **Zero Manual Setup** - No pip install commands needed!
- **Dependency Detection** - Automatically finds missing packages
- **Smart Installation** - Installs from requirements.txt
- **Model Management** - Downloads Ollama models automatically

### 🎵 **Smart Music Player**
- **Auto-Trending** - "YouTube kholo" plays latest viral song
- **Multi-language** - Hindi, English, Punjabi, Tamil, etc.
- **Smart Defaults** - "gaana bajao" → plays trending song
- **Specific Songs** - "Kesariya bajao" → plays exact song

### 🎬 **Movie Downloader**
- **Web Automation** - Downloads from vegamovies, etc.
- **Auto-Play** - Opens in VLC player automatically
- **Quality Selection** - 480p, 720p, 1080p
- **Progress Tracking** - Shows download progress

### 🌐 **Internet Integration**
- **Real-time Search** - DuckDuckGo API for instant answers
- **Web Scraping** - Extracts content from any webpage
- **YouTube Search** - Finds videos and trending content
- **Live Data** - Weather, news, prices, anything current

### 🔧 **Autonomous Self-Healing**
- **Ollama AI** analyzes errors and generates fixes
- **Internet Search** finds solutions from StackOverflow
- **Automatic Code Repair** - fixes itself without intervention
- **Backup System** - creates backups before applying fixes

### 🗣️ **Natural Language**
- **Hinglish Support** - "Jarvis, gaana bajao", "YouTube kholo"
- **Context Aware** - Understands follow-up commands
- **Multi-language** - Hindi, English, mixed

---

## 💬 Usage Examples

### **YouTube & Music (Auto-Trending!)**
```
👤 You: youtube kholo
🤖 JARVIS: 🎵 Playing trending song: Tauba Tauba Bad Newz

👤 You: gaana bajao
🤖 JARVIS: 🎵 Auto-selected: Kesariya Brahmastra

👤 You: play Kesariya on youtube
🤖 JARVIS: 🎵 Playing: Kesariya

👤 You: latest song bajao
🤖 JARVIS: 🎵 Playing: Satranga Animal
```

### **Movie Download**
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
⬇️  Progress: 45.2%
...
✅ Download complete!
🎥 Opening in VLC player...

👤 You: Avatar 1080p quality mein download karo
🤖 JARVIS: [Downloads Avatar in 1080p]
```

### **Web Search**
```
👤 You: google search python
🤖 JARVIS: ✅ Opened Google search for: python

👤 You: open youtube.com
🤖 JARVIS: ✅ Opened: https://youtube.com
```

### **General Chat**
```
👤 You: hello jarvis
🤖 JARVIS: Hello! How can I help you today?

👤 You: what can you do?
🤖 JARVIS: I can:
- Play music on YouTube (trending or specific songs)
- Download movies from websites
- Search Google and open websites
- And much more!
```

---

## 📦 Auto-Installed Packages

When you run `python main.py`, JARVIS automatically installs:

### Required Packages
- ✅ `ollama` - Local LLM
- ✅ `selenium` - Web automation (movie downloader)
- ✅ `beautifulsoup4` - Web scraping
- ✅ `requests` - HTTP requests
- ✅ `pywhatkit` - YouTube automation
- ✅ `webdriver-manager` - ChromeDriver auto-install
- ✅ `SpeechRecognition` - Voice input (optional)
- ✅ `pyttsx3` - Text-to-speech (optional)
- ✅ `python-dotenv` - Environment variables

### Optional Packages
- ⚠️ `PyQt5` - GUI (optional)
- ⚠️ `opencv-python` - Computer vision (optional)
- ⚠️ `pyautogui` - Screen automation (optional)

---

## 🛠️ Troubleshooting

### Issue: "Ollama connection refused"
```bash
# Start Ollama in separate terminal
ollama serve

# Then run JARVIS in another terminal
python main.py
```

### Issue: "Dependencies still missing"
```bash
# Restart JARVIS (it will auto-install again)
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

### Issue: "VLC player not found" (for movies)
```bash
# Windows
Download from: https://www.videolan.org/vlc/

# Linux
sudo apt install vlc

# macOS
brew install --cask vlc
```

---

## 🏗️ Architecture

```
JARVIS/
├── core/
│   ├── engine.py              # Ollama LLM integration
│   ├── self_healing.py        # Autonomous error fixing
│   ├── voice.py               # Speech recognition
│   └── registry.py            # Skill management
├── skill/
│   ├── web_ops.py             # YouTube auto-music
│   ├── movie_downloader.py    # Movie download & play
│   ├── music_ops.py           # Trending music player
│   ├── system_ops.py          # System control
│   └── [15+ other skills]
├── main.py                    # Auto-install + Entry point
└── requirements.txt           # All dependencies
```

---

## 🔥 Advanced Features

### **1. Auto-Install System**

```python
# On startup, JARVIS automatically:
1. Checks all required packages
2. Detects missing dependencies
3. Installs from requirements.txt
4. Downloads Ollama model if needed
5. Creates .env configuration
6. Starts running!
```

### **2. YouTube Auto-Music**

```python
# When you say "YouTube kholo":
1. Fetches trending songs from YouTube
2. Filters music videos
3. Selects random trending song
4. Auto-plays on YouTube
```

### **3. Movie Downloader**

```python
# When you say "download movie X":
1. Searches movie on website (vegamovies, etc.)
2. Extracts download link using Selenium
3. Downloads with progress tracking
4. Auto-plays in VLC player
```

### **4. Internet-Powered Error Fixing**

```python
# When an error occurs:
1. Searches DuckDuckGo for solutions
2. Scrapes StackOverflow for fixes
3. Feeds solutions to Ollama AI
4. Generates comprehensive fix
5. Validates and applies fix
6. Creates backup before changes
```

---

## 📚 Documentation

- **QUICK_START.md** - 3-step setup guide
- **INSTALLATION.md** - Detailed installation
- **MOVIE_DOWNLOADER_GUIDE.md** - Movie features
- **YOUTUBE_AUTO_MUSIC_GUIDE.md** - Music features
- **OLLAMA_SETUP.md** - LLM configuration

---

## 🔄 Update JARVIS

```bash
cd Zarves
git pull origin main
python main.py  # Auto-installs any new dependencies
```

---

## 📊 System Requirements

### **Minimum**
- Python 3.8+
- 4GB RAM
- 5GB disk space (for Ollama model)
- Internet connection

### **Recommended**
- Python 3.10+
- 8GB RAM
- 10GB disk space
- Good internet (for trending music & downloads)

### **Supported Platforms**
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

---

## 💡 Pro Tips

1. **First Run**: Takes 2-5 minutes (downloads model + installs packages)
2. **Subsequent Runs**: Starts in seconds
3. **Ollama Server**: Keep `ollama serve` running in background
4. **Updates**: Just `git pull` and run - auto-installs new dependencies
5. **VLC**: Install for movie playback feature

---

## ✅ Quick Checklist

- [ ] Ollama installed
- [ ] Repository cloned
- [ ] Run `python main.py`
- [ ] Wait for auto-install (first time only)
- [ ] Start using JARVIS!

---

## 🎉 Success Indicators

You'll know JARVIS is ready when you see:

```
✅ All required packages are installed!
✅ Ollama installed
✅ llama3.2 model found
✅ Startup checks complete!

🤖 JARVIS - Your Autonomous AI Assistant
======================================================================
✅ Loaded 8 skills
✅ JARVIS ready!

🎤 JARVIS is listening...
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new skills
- Improve auto-install system
- Enhance error handling
- Add more features

---

## 📄 License

MIT License - Free to use and modify!

---

## 🙏 Credits

- **Ollama** - Local LLM
- **Selenium** - Web automation
- **PyWhatKit** - YouTube integration
- **BeautifulSoup** - Web scraping

---

**Made with ❤️ by the JARVIS community**

**No manual setup. No pip installs. Just run and go!** 🚀

# 🤖 JARVIS - Your Personal AI Assistant (Bilkul Human Jaisa!)

> **"Main sirf assist nahi karta. Main samajhta hoon, yaad rakhta hoon, aur bilkul insaan ki tarah baat karta hoon."**

JARVIS is an **intelligent personal AI assistant** that behaves like a real human:
- ✅ **🎤 VOICE MODE** - Talk naturally, no typing needed! Just say "Jarvis" and speak!
- ✅ **NATURAL CONVERSATIONS** - Talks like a real person, not a robot!
- ✅ **EMOTION DETECTION** - Understands if you're happy, frustrated, or excited
- ✅ **CONTEXT MEMORY** - Remembers previous conversations and tasks
- ✅ **OPENS ANY WINDOWS APP** - This PC, Control Panel, VLC, Word, Excel, and 50+ apps! 🖥️
- ✅ **AUTO-PLAY MUSIC** - "YouTube kholo" automatically plays trending songs! 🎵
- ✅ **AUTO-INSTALLS EVERYTHING** - Just run `python main.py` and it handles the rest!
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **MOVIE DOWNLOADER** - Download and play movies with VLC
- ✅ **SELF-HEALING** - Fixes its own errors using AI + internet
- ✅ **HINGLISH SUPPORT** - Speak naturally in Hindi, English, or mixed!

---

## 💬 Natural Conversation Examples

### **Example 1: Voice Mode - Just Talk! 🎤**

```
🎤 You: "Jarvis, gaana bajao"

🔊 JARVIS: "Playing trending song for you! Opening YouTube with auto-play..."
          [YouTube opens and music starts playing automatically]
          "Done! What else can I do for you?"

🎤 You: "volume badhao"

🔊 JARVIS: "Done! Anything else?"

🎤 You: "thanks!"

🔊 JARVIS: "You're welcome! Happy to help!"
```

**No typing needed! Just talk naturally like you're talking to a friend!** 🗣️

### **Example 2: Opens ANY Windows Application**

```
🎤 You: "Jarvis, this pc kholo"

🔊 JARVIS: "Opening This PC. Done!"

🎤 You: "control panel kholo"

🔊 JARVIS: "Opening Control Panel. Done!"

🎤 You: "vlc kholo"

🔊 JARVIS: "Opening VLC Media Player. Done!"

🎤 You: "word kholo"

🔊 JARVIS: "Opening Microsoft Word. Done!"
```

### **Example 3: Text Mode (Alternative)**

If you prefer typing:

```
👤 You: hello jarvis

🤖 JARVIS: Hello! I'm JARVIS, your personal assistant. How can I help you today?

👤 You: gaana bajao

🤖 JARVIS: 🎵 Playing trending song for you!
          
          🎬 Opening YouTube with auto-play...
          ✅ YouTube opened and playing!
          
          😊 Glad I could help! Anything else?

👤 You: volume badhao

🤖 JARVIS: ✅ Done! What else can I do for you?
```

### **Example 4: Understands Your Emotions**

```
🎤 You: "Jarvis, this is not working properly"

🔊 JARVIS: "I understand your frustration. Let me try to fix this."
          [Attempts fix]
          "I hope this helps! Let me know if you need anything else."

🎤 You: "perfect! that worked"

🔊 JARVIS: "I'm glad I could help!"
```

### **Example 5: Remembers Context**

```
🎤 You: "Jarvis, youtube kholo"

🔊 JARVIS: "Playing trending song: Kesariya. Opening YouTube with auto-play..."
          [YouTube opens and plays]
          "Done! What else can I do for you?"

🎤 You: "uska volume kam karo"

🔊 JARVIS: "Done! Anything else?"
          [Knows "uska" = YouTube video]
```

**[See more examples in CONVERSATION_EXAMPLES.md](CONVERSATION_EXAMPLES.md)**

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
- ✅ Asks if you want Voice Mode or Text Mode
- ✅ Starts running!

**First run takes 2-5 minutes** (downloads model + installs packages)  
**Subsequent runs start in seconds!**

---

## 🎯 What Makes JARVIS Special?

### **1. 🎤 Voice Mode - Talk Naturally!**

**No typing needed!** Just talk to JARVIS like you're talking to a friend:

```
🎙️  Choose Mode:
1. 🎤 Voice Mode (Recommended) - Talk naturally
2. ⌨️  Text Mode - Type commands

Enter choice (1 or 2, default=1): 1

🎤 Voice Mode Activated

💬 How to use:
   1. Say 'Jarvis' to activate
   2. Then give your command
   3. JARVIS will respond with voice

💡 Examples:
   • 'Jarvis, gaana bajao'
   • 'Jarvis, youtube kholo'
   • 'Jarvis, volume badhao'
```

**Features:**
- ✅ **Wake Word Detection** - Say "Jarvis" to activate
- ✅ **Continuous Mode** - After wake word, no need to repeat "Jarvis" for 30 seconds
- ✅ **Hindi + English Support** - Speak in Hindi, English, or Hinglish
- ✅ **Natural Voice Response** - JARVIS speaks back to you
- ✅ **Emotion Detection** - Understands your tone and mood

**How it works:**
1. Say **"Jarvis"** (wake word)
2. JARVIS activates and says "I'm listening"
3. Give your command (no need to say "Jarvis" again for 30 seconds)
4. JARVIS responds with voice
5. Continue conversation naturally!

### **2. 🗣️ Natural Conversations (Like a Real Person!)**

JARVIS doesn't talk like a robot. It understands context, emotions, and speaks naturally:

**Robot Response:**
```
❌ "Task completed successfully. Awaiting further instructions."
```

**JARVIS Response:**
```
✅ "Done! Anything else I can help with? 😊"
```

### **3. 🖥️ Opens ANY Windows Application (50+ Apps!)**

Just say the app name and JARVIS opens it instantly! No need to search or click:

#### **System Tools & Settings**
```
🎤 You: "Jarvis, this pc kholo"          → Opens This PC (My Computer)
🎤 You: "Jarvis, control panel kholo"    → Opens Control Panel
🎤 You: "Jarvis, settings kholo"         → Opens Windows Settings
🎤 You: "Jarvis, task manager kholo"     → Opens Task Manager
🎤 You: "Jarvis, device manager kholo"   → Opens Device Manager
🎤 You: "Jarvis, disk management kholo"  → Opens Disk Management
🎤 You: "Jarvis, registry editor kholo"  → Opens Registry Editor
🎤 You: "Jarvis, services kholo"         → Opens Services
🎤 You: "Jarvis, event viewer kholo"     → Opens Event Viewer
```

#### **Office Applications**
```
🎤 You: "Jarvis, word kholo"             → Opens Microsoft Word
🎤 You: "Jarvis, excel kholo"            → Opens Microsoft Excel
🎤 You: "Jarvis, powerpoint kholo"       → Opens PowerPoint
🎤 You: "Jarvis, outlook kholo"          → Opens Outlook
```

#### **Media & Entertainment**
```
🎤 You: "Jarvis, vlc kholo"              → Opens VLC Media Player
🎤 You: "Jarvis, spotify kholo"          → Opens Spotify
🎤 You: "Jarvis, steam kholo"            → Opens Steam
```

#### **Browsers & Communication**
```
🎤 You: "Jarvis, chrome kholo"           → Opens Google Chrome
🎤 You: "Jarvis, firefox kholo"          → Opens Firefox
🎤 You: "Jarvis, edge kholo"             → Opens Microsoft Edge
🎤 You: "Jarvis, discord kholo"          → Opens Discord
```

#### **Development Tools**
```
🎤 You: "Jarvis, vscode kholo"           → Opens Visual Studio Code
🎤 You: "Jarvis, cmd kholo"              → Opens Command Prompt
🎤 You: "Jarvis, powershell kholo"       → Opens PowerShell
```

#### **Utilities**
```
🎤 You: "Jarvis, notepad kholo"          → Opens Notepad
🎤 You: "Jarvis, calculator kholo"       → Opens Calculator
🎤 You: "Jarvis, paint kholo"            → Opens Paint
🎤 You: "Jarvis, snipping tool kholo"    → Opens Snipping Tool
```

**And many more!** JARVIS can open:
- ✅ **50+ Windows applications**
- ✅ **System tools and settings**
- ✅ **Office applications**
- ✅ **Media players**
- ✅ **Browsers**
- ✅ **Development tools**
- ✅ **Any installed application**

**How it works:**
1. 🔍 Searches Windows Registry for app paths
2. 🔍 Checks common installation directories
3. 🔍 Uses Windows shell commands for system tools
4. ✅ Opens the app automatically!

### **4. 🎵 AUTO-PLAY Music (No Manual Clicking!)**

Just say "YouTube kholo" or "gaana bajao" and JARVIS:
1. ✅ Fetches trending songs from YouTube
2. ✅ Opens browser automatically
3. ✅ **Clicks the first video to play** (using Selenium)
4. ✅ Music starts playing instantly!

**No more manual clicking!** JARVIS does everything automatically! 🚀

```
🎤 You: "Jarvis, youtube kholo"

🔊 JARVIS: "Playing trending song: Tauba Tauba Bad Newz. Opening YouTube with auto-play..."
          [YouTube opens and music starts playing]
          "Done! What else can I do for you?"
```

### **5. 😊 Emotion Detection**

JARVIS detects your mood and responds appropriately:

- **Happy** → "I'm glad I could help! 😊"
- **Frustrated** → "I understand your frustration. Let me fix this."
- **Excited** → "That's awesome! 🎉"
- **Neutral** → "Sure, I'm on it."

### **6. 🧠 Context Memory**

Remembers previous tasks and conversations:

```
🎤 You: "Jarvis, play Kesariya on youtube"
🔊 JARVIS: [Plays Kesariya]

🎤 You: "uska volume badhao"
🔊 JARVIS: [Increases volume - knows "uska" = YouTube]

🎤 You: "screenshot lo"
🔊 JARVIS: [Takes screenshot]

🎤 You: "woh movie download karo"
🔊 JARVIS: [Remembers which movie you mentioned earlier]
```

### **7. 🎬 Smart Movie Downloader**

Download and play movies with one command:

```
🎤 You: "Jarvis, vegamovies se Inception download karo"

🔊 JARVIS: "Downloading Inception. I'll let you know when it's ready!"
          [Downloads and opens in VLC automatically]
```

### **8. 🌐 Multi-language (Hinglish!)**

Speak naturally in Hindi, English, or mixed:

```
🎤 You: "Jarvis, bhai youtube pe latest song bajao"

🔊 JARVIS: "Playing latest song for you! Opening YouTube with auto-play..."
          [YouTube opens and plays]
          "Done! Aur kya chahiye?"
```

---

## 🌟 Key Features

### **🎤 Voice Mode (Primary Feature)**
- **Wake Word Detection** - Say "Jarvis" to activate
- **Continuous Listening** - No need to repeat wake word for 30 seconds
- **Hindi + English Support** - Speak in any language
- **Natural Voice Response** - JARVIS speaks back to you
- **Emotion Detection** - Understands your tone
- **Context Awareness** - Remembers conversation
- **No Typing Needed** - Just talk naturally!

### **🔧 Auto-Install Everything**
- **Zero Manual Setup** - No pip install commands needed!
- **Dependency Detection** - Automatically finds missing packages
- **Smart Installation** - Installs from requirements.txt
- **Model Management** - Downloads Ollama models automatically

### **💬 Personal Assistant Intelligence**
- **Natural Language** - Talks like a human, not a robot
- **Emotion Detection** - Understands happy, sad, frustrated, excited
- **Context Awareness** - Remembers previous conversations
- **Proactive Suggestions** - Offers help based on time and context
- **Multi-language** - Hindi, English, Hinglish

### **🖥️ Universal Windows App Opener**
- **50+ Applications** - Opens any Windows app, system tool, or setting
- **Smart Search** - Finds apps in Registry, Program Files, AppData
- **System Tools** - This PC, Control Panel, Settings, Task Manager, etc.
- **Office Suite** - Word, Excel, PowerPoint, Outlook
- **Media Players** - VLC, Spotify, Windows Media Player
- **Browsers** - Chrome, Firefox, Edge
- **Development** - VS Code, CMD, PowerShell
- **Utilities** - Notepad, Calculator, Paint, Snipping Tool
- **Auto-Detection** - Automatically finds installed apps

### **🎵 Smart Music Player with AUTO-PLAY**
- **Auto-Trending** - "YouTube kholo" plays latest viral song
- **Automatic Playback** - Uses Selenium to click and play video
- **Multi-language** - Hindi, English, Punjabi, Tamil, etc.
- **Smart Defaults** - "gaana bajao" → plays trending song
- **Specific Songs** - "Kesariya bajao" → plays exact song
- **No Manual Clicking** - Everything happens automatically!

### **🎬 Movie Downloader**
- **Web Automation** - Downloads from vegamovies, etc.
- **Auto-Play** - Opens in VLC player automatically
- **Quality Selection** - 480p, 720p, 1080p
- **Progress Tracking** - Shows download progress

### **🌐 Internet Integration**
- **Real-time Search** - DuckDuckGo API for instant answers
- **Web Scraping** - Extracts content from any webpage
- **YouTube Search** - Finds videos and trending content
- **Live Data** - Weather, news, prices, anything current

### **🔧 Autonomous Self-Healing**
- **Ollama AI** analyzes errors and generates fixes
- **Internet Search** finds solutions from StackOverflow
- **Automatic Code Repair** - fixes itself without intervention
- **Backup System** - creates backups before applying fixes

---

## 💬 Usage Examples

### **Voice Mode (Recommended) 🎤**
```
🎤 You: "Jarvis, hello"
🔊 JARVIS: "Hello! How can I help you today?"

🎤 You: "gaana bajao"
🔊 JARVIS: "Playing trending song for you!"
          [Auto-plays music on YouTube]

🎤 You: "this pc kholo"
🔊 JARVIS: "Opening This PC. Done!"

🎤 You: "vlc kholo"
🔊 JARVIS: "Opening VLC Media Player. Done!"

🎤 You: "volume badhao"
🔊 JARVIS: "Done! Anything else?"

🎤 You: "thanks"
🔊 JARVIS: "You're welcome! Happy to help!"
```

### **Text Mode (Alternative) ⌨️**
```
👤 You: hello jarvis
🤖 JARVIS: Hello! How can I help you today?

👤 You: what can you do?
🤖 JARVIS: I can:
          - Open ANY Windows app (This PC, VLC, Word, Excel, etc.)
          - Play music on YouTube (auto-plays trending songs!)
          - Download movies from websites
          - Search Google and open websites
          - Control system (volume, brightness)
          - And much more! Just ask naturally!

👤 You: gaana bajao
🤖 JARVIS: 🎵 Playing trending song for you!
          [Auto-plays music on YouTube]
```

### **Opening Windows Applications**
```
🎤 You: "Jarvis, this pc kholo"
🔊 JARVIS: "Opening This PC. Done!"

🎤 You: "control panel kholo"
🔊 JARVIS: "Opening Control Panel. Done!"

🎤 You: "vlc kholo"
🔊 JARVIS: "Opening VLC Media Player. Done!"

🎤 You: "word kholo"
🔊 JARVIS: "Opening Microsoft Word. Done!"

🎤 You: "task manager kholo"
🔊 JARVIS: "Opening Task Manager. Done!"

🎤 You: "settings kholo"
🔊 JARVIS: "Opening Windows Settings. Done!"
```

### **YouTube & Music (AUTO-PLAY!)**
```
🎤 You: "Jarvis, youtube kholo"
🔊 JARVIS: "Playing trending song: Tauba Tauba Bad Newz. Opening YouTube with auto-play..."
          [YouTube opens and plays]

🎤 You: "play Kesariya"
🔊 JARVIS: "Playing Kesariya. Opening YouTube with auto-play..."
          [YouTube opens and plays]

🎤 You: "latest song bajao"
🔊 JARVIS: "Playing Satranga Animal..."
          [Auto-plays automatically!]
```

### **Movie Download**
```
🎤 You: "Jarvis, vegamovies se Inception download karo"
🔊 JARVIS: "Downloading Inception. I'll let you know when it's ready!"
          [Downloads and plays in VLC]

🎤 You: "Avatar 1080p quality mein download karo"
🔊 JARVIS: [Downloads Avatar in 1080p]
```

### **Follow-up Commands**
```
🎤 You: "Jarvis, youtube kholo"
🔊 JARVIS: [Opens YouTube with trending song auto-playing]

🎤 You: "uska volume badhao"
🔊 JARVIS: "Done!"

🎤 You: "screenshot lo"
🔊 JARVIS: "Screenshot saved!"
```

---

## 📦 Auto-Installed Packages

When you run `python main.py`, JARVIS automatically installs:

### Required Packages
- ✅ `ollama` - Local LLM
- ✅ `selenium` - Web automation (for auto-play feature!)
- ✅ `webdriver-manager` - ChromeDriver auto-install
- ✅ `beautifulsoup4` - Web scraping
- ✅ `requests` - HTTP requests
- ✅ `pywhatkit` - YouTube automation
- ✅ `python-dotenv` - Environment variables
- ✅ `SpeechRecognition` - Voice input (for Voice Mode!)
- ✅ `pyttsx3` - Text-to-speech (for Voice Mode!)

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

### Issue: "Auto-play not working"
```bash
# Make sure Selenium is installed
pip install selenium webdriver-manager

# Chrome browser must be installed
# JARVIS will auto-download ChromeDriver
```

### Issue: "Voice mode not working"
```bash
# Make sure microphone is connected
# Check microphone permissions in Windows Settings

# Install voice packages manually if needed
pip install SpeechRecognition pyttsx3

# Test microphone
python -c "import speech_recognition as sr; print('Mic test:', sr.Microphone.list_microphone_names())"
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

### Issue: "App not opening"
```bash
# Make sure the application is installed
# Try using full app name (e.g., "Google Chrome" instead of "Chrome")
# JARVIS will search Registry and common locations automatically
```

---

## 🏗️ Architecture

```
JARVIS/
├── core/
│   ├── engine.py              # Ollama LLM + Personal Assistant
│   ├── personal_assistant.py  # Natural conversation & emotion detection
│   ├── voice.py               # Voice input/output (Speech Recognition + TTS)
│   ├── self_healing.py        # Autonomous error fixing
│   └── registry.py            # Skill management
├── skill/
│   ├── system_ops.py          # Windows app opener (50+ apps!)
│   ├── web_ops.py             # YouTube auto-play with Selenium
│   ├── movie_downloader.py    # Movie download & play
│   ├── music_ops.py           # Trending music player with auto-play
│   ├── system_ops.py          # System control
│   └── [18+ other skills]
├── main.py                    # Auto-install + Voice/Text Mode + Entry point
└── requirements.txt           # All dependencies
```

---

## 📚 Documentation

- **CONVERSATION_EXAMPLES.md** - Natural conversation examples
- **QUICK_START.md** - 3-step setup guide
- **README.md** - This file

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
- Chrome browser (for auto-play feature)
- Microphone (for Voice Mode)
- Internet connection

### **Recommended**
- Python 3.10+
- 8GB RAM
- 10GB disk space
- Good internet (for trending music & downloads)
- Quality microphone (for better voice recognition)

### **Supported Platforms**
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

---

## 💡 Pro Tips

1. **Use Voice Mode** - Much more natural than typing! Just say "Jarvis" and talk
2. **Continuous Mode** - After saying "Jarvis" once, no need to repeat for 30 seconds
3. **Talk Naturally** - JARVIS understands natural language, no need for commands
4. **Use Follow-ups** - "usko volume badhao" works after "youtube kholo"
5. **Express Emotions** - JARVIS responds empathetically
6. **Mix Languages** - Hindi, English, Hinglish - sab chalega!
7. **First Run** - Takes 2-5 minutes (downloads model + packages)
8. **Subsequent Runs** - Starts in seconds
9. **Auto-Play** - Just say "YouTube kholo" and music starts automatically!
10. **Open Any App** - Just say the app name: "VLC kholo", "Word kholo", "This PC kholo"

---

## ✅ Quick Checklist

- [ ] Ollama installed
- [ ] Chrome browser installed (for auto-play)
- [ ] Microphone connected (for Voice Mode)
- [ ] Repository cloned
- [ ] Run `python main.py`
- [ ] Choose Voice Mode (option 1)
- [ ] Wait for auto-install (first time only)
- [ ] Say "Jarvis" and start talking!

---

## 🎉 Success Indicators

You'll know JARVIS is ready when you see:

```
✅ All required packages are installed!
✅ Ollama installed
✅ llama3.2 model found
✅ Startup checks complete!

🤖 JARVIS - Your Personal AI Assistant
======================================================================
✅ Loaded 19 skills
✅ JARVIS ready!

🎙️  Choose Mode:
1. 🎤 Voice Mode (Recommended) - Talk naturally
2. ⌨️  Text Mode - Type commands

Enter choice (1 or 2, default=1): 1

🎤 Voice Mode Activated
Say 'Jarvis' to activate...
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new skills
- Improve conversation intelligence
- Enhance emotion detection
- Add more features
- Improve voice recognition

---

## 📄 License

MIT License - Free to use and modify!

---

## 🙏 Credits

- **Ollama** - Local LLM
- **Selenium** - Web automation & auto-play
- **PyWhatKit** - YouTube integration
- **BeautifulSoup** - Web scraping
- **SpeechRecognition** - Voice input
- **pyttsx3** - Text-to-speech

---

**Made with ❤️ by the JARVIS community**

**Bas "Jarvis" bolo aur baat karo! Koi bhi Windows app khol sakta hai aur music bhi automatically play kar dega! Ab typing ki zarurat nahi!** 🚀🎵🖥️🎤

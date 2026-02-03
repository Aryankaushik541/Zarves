# 🤖 JARVIS - Your Personal AI Assistant (Bilkul Human Jaisa!)

> **"Main sirf assist nahi karta. Main samajhta hoon, yaad rakhta hoon, aur bilkul insaan ki tarah baat karta hoon."**

JARVIS is an **intelligent personal AI assistant** that behaves like a real human:
- ✅ **NATURAL CONVERSATIONS** - Talks like a real person, not a robot!
- ✅ **EMOTION DETECTION** - Understands if you're happy, frustrated, or excited
- ✅ **CONTEXT MEMORY** - Remembers previous conversations and tasks
- ✅ **AUTO-INSTALLS EVERYTHING** - Just run `python main.py` and it handles the rest!
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **TRENDING MUSIC** - "YouTube kholo" automatically plays viral songs
- ✅ **MOVIE DOWNLOADER** - Download and play movies with VLC
- ✅ **SELF-HEALING** - Fixes its own errors using AI + internet
- ✅ **HINGLISH SUPPORT** - Speak naturally in Hindi, English, or mixed!

---

## 💬 Natural Conversation Examples

### **Example 1: Just Like Talking to a Friend**

```
👤 You: hello jarvis

🤖 JARVIS: Hello! I'm JARVIS, your personal assistant. How can I help you today?

👤 You: gaana bajao

🤖 JARVIS: 🎵 Playing trending song for you!
          [Plays: Tauba Tauba Bad Newz]
          😊 Glad I could help! Anything else?

👤 You: volume badhao

🤖 JARVIS: ✅ Done! What else can I do for you?

👤 You: thanks!

🤖 JARVIS: You're welcome! Happy to help! 😊
```

### **Example 2: Understands Your Emotions**

```
👤 You: this is not working properly

🤖 JARVIS: I understand your frustration. Let me try to fix this.
          [Attempts fix]
          I hope this helps! Let me know if you need anything else.

👤 You: perfect! that worked

🤖 JARVIS: I'm glad I could help! 😊
```

### **Example 3: Remembers Context**

```
👤 You: youtube kholo

🤖 JARVIS: 🎵 Playing trending song: Kesariya
          Done! What else can I do for you?

👤 You: uska volume kam karo

🤖 JARVIS: ✅ Done! Anything else?
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
- ✅ Starts running!

**First run takes 2-5 minutes** (downloads model + installs packages)  
**Subsequent runs start in seconds!**

---

## 🎯 What Makes JARVIS Special?

### **1. 🗣️ Natural Conversations (Like a Real Person!)**

JARVIS doesn't talk like a robot. It understands context, emotions, and speaks naturally:

**Robot Response:**
```
❌ "Task completed successfully. Awaiting further instructions."
```

**JARVIS Response:**
```
✅ "Done! Anything else I can help with? 😊"
```

### **2. 😊 Emotion Detection**

JARVIS detects your mood and responds appropriately:

- **Happy** → "I'm glad I could help! 😊"
- **Frustrated** → "I understand your frustration. Let me fix this."
- **Excited** → "That's awesome! 🎉"
- **Neutral** → "Sure, I'm on it."

### **3. 🧠 Context Memory**

Remembers previous tasks and conversations:

```
👤 You: play Kesariya on youtube
🤖 JARVIS: [Plays Kesariya]

👤 You: uska volume badhao
🤖 JARVIS: [Increases volume - knows "uska" = YouTube]

👤 You: screenshot lo
🤖 JARVIS: [Takes screenshot]

👤 You: woh movie download karo
🤖 JARVIS: [Remembers which movie you mentioned earlier]
```

### **4. 🎵 Auto-Trending Music**

Just say "YouTube kholo" and JARVIS automatically plays the latest viral song:

```
👤 You: youtube kholo

🤖 JARVIS: 🎵 Playing trending song: Tauba Tauba Bad Newz
          ✅ YouTube opened and playing!
```

### **5. 🎬 Smart Movie Downloader**

Download and play movies with one command:

```
👤 You: vegamovies se Inception download karo

🤖 JARVIS: 🎬 Downloading Inception. I'll let you know when it's ready!
          [Downloads and opens in VLC automatically]
```

### **6. 🌐 Multi-language (Hinglish!)**

Speak naturally in Hindi, English, or mixed:

```
👤 You: bhai youtube pe latest song bajao

🤖 JARVIS: 🎵 Playing latest song for you!
          Done! Aur kya chahiye?
```

---

## 🌟 Key Features

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

### **🎵 Smart Music Player**
- **Auto-Trending** - "YouTube kholo" plays latest viral song
- **Multi-language** - Hindi, English, Punjabi, Tamil, etc.
- **Smart Defaults** - "gaana bajao" → plays trending song
- **Specific Songs** - "Kesariya bajao" → plays exact song

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

### **Natural Conversation**
```
👤 You: hello jarvis
🤖 JARVIS: Hello! How can I help you today?

👤 You: what can you do?
🤖 JARVIS: I can:
          - Play music on YouTube (trending or specific songs)
          - Download movies from websites
          - Search Google and open websites
          - Control system (volume, brightness)
          - And much more! Just ask naturally!

👤 You: gaana bajao
🤖 JARVIS: 🎵 Playing trending song for you!
```

### **YouTube & Music**
```
👤 You: youtube kholo
🤖 JARVIS: 🎵 Playing trending song: Tauba Tauba Bad Newz

👤 You: play Kesariya
🤖 JARVIS: 🎵 Playing: Kesariya

👤 You: latest song bajao
🤖 JARVIS: 🎵 Playing: Satranga Animal
```

### **Movie Download**
```
👤 You: vegamovies se Inception download karo
🤖 JARVIS: 🎬 Downloading Inception. I'll let you know when it's ready!
          [Downloads and plays in VLC]

👤 You: Avatar 1080p quality mein download karo
🤖 JARVIS: [Downloads Avatar in 1080p]
```

### **Follow-up Commands**
```
👤 You: youtube kholo
🤖 JARVIS: [Opens YouTube with trending song]

👤 You: uska volume badhao
🤖 JARVIS: ✅ Done!

👤 You: screenshot lo
🤖 JARVIS: 📸 Screenshot saved!
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
- ✅ `python-dotenv` - Environment variables

### Optional Packages
- ⚠️ `SpeechRecognition` - Voice input (optional)
- ⚠️ `pyttsx3` - Text-to-speech (optional)
- ⚠️ `PyQt5` - GUI (optional)

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
│   ├── engine.py              # Ollama LLM + Personal Assistant
│   ├── personal_assistant.py  # Natural conversation & emotion detection
│   ├── self_healing.py        # Autonomous error fixing
│   ├── voice.py               # Speech recognition
│   └── registry.py            # Skill management
├── skill/
│   ├── web_ops.py             # YouTube auto-music
│   ├── movie_downloader.py    # Movie download & play
│   ├── music_ops.py           # Trending music player
│   ├── system_ops.py          # System control
│   └── [18+ other skills]
├── main.py                    # Auto-install + Entry point
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

1. **Talk Naturally** - JARVIS understands natural language, no need for commands
2. **Use Follow-ups** - "usko volume badhao" works after "youtube kholo"
3. **Express Emotions** - JARVIS responds empathetically
4. **Mix Languages** - Hindi, English, Hinglish - sab chalega!
5. **First Run** - Takes 2-5 minutes (downloads model + packages)
6. **Subsequent Runs** - Starts in seconds

---

## ✅ Quick Checklist

- [ ] Ollama installed
- [ ] Repository cloned
- [ ] Run `python main.py`
- [ ] Wait for auto-install (first time only)
- [ ] Start talking naturally!

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
- Improve conversation intelligence
- Enhance emotion detection
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

**Bilkul insaan ki tarah baat karo, JARVIS samajh jayega!** 🚀

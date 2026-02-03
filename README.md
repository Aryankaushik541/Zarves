# 🤖 JARVIS - Autonomous AI That Fixes Itself Using Internet + AI

> **"I don't just assist. I search the web, fix my own code, play trending songs, and evolve myself."**

JARVIS is an **advanced autonomous AI** that can:
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **Internet-Powered Self-Healing** - Searches web + uses AI to fix its own errors
- ✅ **Real-time Web Search** - Fetches live data from internet
- ✅ **Trending Music** - Plays latest viral songs from YouTube
- ✅ **Continuous listening mode** - say "Jarvis" once, then give commands naturally
- ✅ **Create new skills** on demand with AI-generated code
- ✅ **Auto-heal errors** using Ollama AI + StackOverflow solutions
- ✅ **Control your entire system** with natural language (Windows/Mac/Linux)
- ✅ **Understand Hinglish** - speak naturally in Hindi or English

---

## 🌟 Key Features

### 🔧 **Autonomous Self-Healing**
- **Ollama AI** analyzes errors and generates fixes
- **Internet Search** finds solutions from StackOverflow, documentation
- **Automatic Code Repair** - fixes itself without human intervention
- **Backup System** - creates backups before applying fixes

### 🌐 **Internet Integration**
- **Real-time Search** - DuckDuckGo API for instant answers
- **Web Scraping** - Extracts content from any webpage
- **YouTube Search** - Finds videos and trending content
- **Live Data** - Weather, news, prices, anything current

### 🎵 **Smart Music Player**
- **Trending Songs** - Automatically plays latest viral hits
- **Multi-language** - Hindi, English, Punjabi, Tamil, etc.
- **Smart Defaults** - "play music" → plays trending song
- **Playlist Support** - Romantic, party, workout playlists

### 🗣️ **Natural Language**
- **Hinglish Support** - "Jarvis, gaana bajao", "YouTube kholo"
- **Continuous Mode** - Say "Jarvis" once, then talk naturally for 30 seconds
- **Context Aware** - Understands follow-up commands

---

## ⚡ Quick Start

### **Step 1: Install Ollama (Free Local LLM)**

```bash
# Windows
https://ollama.com/download/windows

# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### **Step 2: Start Ollama & Pull Model**

```bash
# Start Ollama server
ollama serve

# In another terminal, pull model (one-time, ~2GB download)
ollama pull llama3.2
```

### **Step 3: Setup JARVIS**

```bash
# 1. Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Setup environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run JARVIS
python main.py
```

---

## 🎯 Usage Examples

### **Internet Search**
```
"Jarvis, Bitcoin ki price kya hai?"
"Jarvis, aaj ka weather kaisa hai?"
"Jarvis, latest AI news batao"
"Jarvis, Python tutorial dhundo"
```

### **Music (Trending Songs)**
```
"Jarvis, gaana bajao"              → Plays trending Hindi song
"Jarvis, new song play karo"       → Latest viral hit
"Jarvis, Kesariya bajao"           → Specific song
"Jarvis, English song sunao"       → Trending English song
"Jarvis, romantic playlist"        → Romantic songs mix
```

### **System Control**
```
"Jarvis, volume badao"
"Jarvis, screenshot lo"
"Jarvis, calculator kholo"
"Jarvis, brightness kam karo"
```

### **Web Operations**
```
"Jarvis, YouTube kholo"
"Jarvis, Google pe AI search karo"
"Jarvis, is website ka content batao: example.com"
```

### **Self-Healing (Automatic)**
When JARVIS encounters an error:
1. 🌐 Searches internet for solutions (StackOverflow, docs)
2. 🤖 Uses Ollama AI to analyze error + web solutions
3. 🔧 Generates and validates fix
4. 💾 Creates backup and applies fix
5. ✅ Continues working without interruption

---

## 🏗️ Architecture

```
JARVIS/
├── core/
│   ├── engine.py              # Ollama LLM integration
│   ├── advanced_self_coder.py # AI code generation + Internet search
│   ├── self_healing.py        # Autonomous error fixing
│   ├── voice.py               # Speech recognition
│   └── registry.py            # Skill management
├── skill/
│   ├── internet_search_skill.py  # Web search & scraping
│   ├── music_ops.py              # Trending music player
│   ├── web_ops.py                # Browser control
│   ├── system_ops.py             # System control
│   └── [18+ other skills]
├── gui/
│   └── app.py                 # PyQt5 interface
└── main.py                    # Entry point
```

---

## 🔥 Advanced Features

### **1. Internet-Powered Error Fixing**

When an error occurs:
```python
# JARVIS automatically:
1. Searches DuckDuckGo for error solutions
2. Scrapes StackOverflow for fixes
3. Feeds solutions to Ollama AI
4. Generates comprehensive fix
5. Validates and applies fix
6. Creates backup before changes
```

### **2. Trending Music Detection**

```python
# Automatically fetches trending songs:
1. Scrapes YouTube trending page
2. Filters music videos
3. Selects random trending song
4. Auto-plays on YouTube
```

### **3. Real-time Web Search**

```python
# Live internet data:
- DuckDuckGo Instant Answers
- Google search scraping
- Webpage content extraction
- YouTube video search
```

### **4. Continuous Listening Mode**

```
User: "Jarvis, YouTube kholo"
JARVIS: ✅ Opens YouTube
        💡 Continuous mode active (30 sec)

User: "gaana bajao"  # No need to say "Jarvis" again!
JARVIS: 🎵 Plays trending song
```

---

## 🛠️ Configuration

### **Environment Variables** (`.env`)

```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Voice Settings
VOICE_ENABLED=true
WAKE_WORD=jarvis

# Features
AUTO_FIX=true
INTERNET_SEARCH=true
TRENDING_MUSIC=true
```

---

## 📊 System Requirements

### **Minimum**
- Python 3.8+
- 4GB RAM
- 5GB disk space (for Ollama model)
- Internet connection (for web search & trending music)

### **Recommended**
- Python 3.10+
- 8GB RAM
- NVIDIA GPU (for faster Ollama inference)
- 10GB disk space

### **Supported Platforms**
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

---

## 🎓 How It Works

### **Self-Healing Process**

```mermaid
Error Occurs
    ↓
Search Internet (DuckDuckGo + StackOverflow)
    ↓
Feed Solutions to Ollama AI
    ↓
Generate Fix Code
    ↓
Validate Syntax
    ↓
Create Backup
    ↓
Apply Fix
    ↓
Continue Working ✅
```

### **Music Intelligence**

```mermaid
User: "gaana bajao"
    ↓
Detect Intent (trending/specific)
    ↓
Scrape YouTube Trending
    ↓
Filter Music Videos
    ↓
Select Random Song
    ↓
Auto-play on YouTube 🎵
```

---

## 🚀 Skills Available

| Skill | Description | Internet Required |
|-------|-------------|-------------------|
| **Internet Search** | Real-time web search, scraping | ✅ Yes |
| **Trending Music** | Latest viral songs | ✅ Yes |
| **Web Control** | Open websites, search | ❌ No |
| **System Control** | Volume, brightness, apps | ❌ No |
| **File Operations** | Create, read, delete files | ❌ No |
| **Screenshot** | Capture screen | ❌ No |
| **DateTime** | Time, date, alarms | ❌ No |
| **Weather** | Current weather | ✅ Yes |
| **Email** | Send emails | ✅ Yes |
| **Code Generator** | Write code | ❌ No |
| **Self-Improvement** | Fix own code | ✅ Yes (optional) |

---

## 🐛 Troubleshooting

### **Ollama Connection Failed**
```bash
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### **Internet Search Not Working**
```bash
# Install dependencies
pip install requests beautifulsoup4 lxml

# Check internet connection
ping google.com
```

### **Music Not Playing**
```bash
# Install pywhatkit
pip install pywhatkit

# Or use browser fallback (automatic)
```

### **Voice Recognition Issues**
```bash
# Install PyAudio
pip install pyaudio

# Windows: Download wheel from
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **Ollama** - Free local LLM runtime
- **DuckDuckGo** - Privacy-focused search API
- **YouTube** - Music and video platform
- **StackOverflow** - Developer community
- **PyQt5** - GUI framework
- **SpeechRecognition** - Voice input

---

## 📧 Contact

- **GitHub**: [@Aryankaushik541](https://github.com/Aryankaushik541)
- **Project**: [Zarves](https://github.com/Aryankaushik541/Zarves)

---

## 🌟 Star History

If you find JARVIS useful, please ⭐ star the repository!

---

**Made with ❤️ by developers who believe AI should be free, local, and autonomous.**

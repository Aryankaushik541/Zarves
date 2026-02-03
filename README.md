# 🤖 JARVIS - Your Personal AI Assistant

> **"Enhanced AI Agent with Modern GUI - Smart, Fast, Beautiful"**

Complete AI assistant with **two powerful interfaces** - Classic all-in-one GUI and Modern Enhanced GUI with smart intent detection, threaded processing, and conversation memory!

---

## 🚀 Quick Start - Choose Your Interface!

### 🎨 **Option 1: Modern GUI (Recommended)**
```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Run Modern GUI
python launch_modern.py
```

**✨ Modern GUI Features:**
- 🧵 **Threaded Processing** - No freezing!
- 🧠 **Smart Intent Detection** - Understands Hindi + English
- 💬 **Conversation Memory** - Context-aware responses
- 📊 **Live Statistics** - Real-time monitoring
- ⚡ **Quick Actions** - One-click shortcuts
- 🎨 **Beautiful Dark Theme** - Professional interface

### 📺 **Option 2: Classic GUI**
```bash
# Run Classic GUI (Everything in main.py)
python main.py
```

**Classic Features:**
- ✅ Auto-installs dependencies
- ✅ Auto-installs Ollama
- ✅ Auto-starts Ollama server
- ✅ Auto-downloads AI model
- ✅ Opens GUI window
- ✅ All-in-one file

---

## 🎨 Modern GUI Preview

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 JARVIS                                    ● Ready        │
│  Enhanced AI Assistant                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  💬 Conversation                    📊 Statistics           │
│  ┌──────────────────────┐          ┌──────────────────┐    │
│  │ [09:19:04] 🤖 JARVIS:│          │ 🎯 Skills: 21    │    │
│  │ How can I help?      │          │ 🔧 Tools: 69     │    │
│  │                      │          │ 💬 Queries: 15   │    │
│  │ [09:20:15] 👤 You:   │          │ ✅ Success: 98%  │    │
│  │ youtube kholo        │          └──────────────────┘    │
│  │                      │                                   │
│  │ [09:20:16] 🤖 JARVIS:│          ⚡ Quick Actions        │
│  │ Opening YouTube! 🎵  │          ┌──────────────────┐    │
│  │                      │          │ 🎵 YouTube       │    │
│  └──────────────────────┘          │ 🌐 Browser       │    │
│                                    │ 🎬 Movies        │    │
│                                    │ 🔍 Search        │    │
│                                    │ ⚙️ Settings      │    │
│                                    └──────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Type your command...              [Send] [🎤]              │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ What's New in Modern GUI?

### 🧠 **Enhanced AI Agent**

**Smart Intent Detection** - Automatically understands commands:

| Intent | Hindi Examples | English Examples |
|--------|---------------|------------------|
| YouTube | "youtube खोल", "गाना चला" | "open youtube", "play song" |
| Browser | "browser खोल" | "open browser" |
| Movies | "movie चला" | "play movie" |
| Search | "google खोज", "क्या है" | "search", "what is" |
| System | "volume बढ़ा" | "volume up" |

**Context Awareness** - Remembers conversation:
```
You: "youtube kholo"
JARVIS: "Opening YouTube! 🎵"

You: "wahan pe gaana search kar"  # Refers to YouTube
JARVIS: "Searching for song on YouTube..."
```

### 🎯 **Key Improvements**

1. **🧵 Non-Blocking UI**
   - GUI never freezes
   - Background processing
   - Smooth animations

2. **💬 Conversation Memory**
   - Maintains context
   - Better follow-ups
   - Natural conversations

3. **📊 Live Statistics**
   - Skills loaded
   - Tools available
   - Queries processed
   - Success rate

4. **⚡ Quick Actions**
   - YouTube shortcut
   - Browser shortcut
   - Movies shortcut
   - Search shortcut
   - Settings access

5. **🎨 Modern Design**
   - Dark theme
   - Color-coded messages
   - Professional look
   - Better readability

---

## 📦 Features

### 🎵 **Entertainment**
- ✅ YouTube Auto-Play
- ✅ PC Movie Search
- ✅ VLC Auto-Play
- ✅ Music Control

### 🌐 **Web & Browser**
- ✅ Browser Auto-Login
- ✅ Web Search
- ✅ Internet Operations

### 💻 **System Control**
- ✅ Volume Control
- ✅ Shutdown/Restart
- ✅ File Operations
- ✅ Screenshot

### 🤖 **AI Capabilities**
- ✅ Local AI (Ollama)
- ✅ Natural Conversations
- ✅ Smart Task Execution
- ✅ Multi-language (Hindi + English)

### 🎤 **Voice Control**
- ✅ Voice Commands
- ✅ Text-to-Speech
- ✅ Wake Word Detection
- ✅ Hindi Recognition

---

## 📚 Documentation

- **[Modern GUI Guide](MODERN_GUI.md)** - Complete guide for enhanced interface
- **[Quick Start](QUICKSTART.md)** - Get started in 5 minutes
- **[Skills Documentation](docs/SKILLS.md)** - All available skills

---

## 🎯 Usage Examples

### **Voice Commands**

```bash
# YouTube
"youtube kholo"
"gaana sunao"
"play despacito"

# Browser
"browser kholo"
"chrome open karo"

# Movies
"movie chalao"
"inception play karo"

# Search
"google par search karo"
"what is AI"
"python kya hai"

# System
"volume badhao"
"screenshot lo"
```

### **Text Commands**

Simply type in the input field:
- `open youtube`
- `play song`
- `search python`
- `what time is it`
- `take screenshot`

---

## 🛠️ Installation

### **Prerequisites**
- Python 3.8+
- Ollama (auto-installed)
- Internet connection (first run)

### **Quick Install**

```bash
# Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Install dependencies (optional - auto-installed)
pip install -r requirements.txt

# Run Modern GUI
python launch_modern.py

# OR Run Classic GUI
python main.py
```

### **Manual Ollama Setup** (if needed)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# Pull model
ollama pull llama3.2
```

---

## 📊 Project Structure

```
Zarves/
├── main.py                 # Classic all-in-one launcher
├── launch_modern.py        # Modern GUI launcher
├── requirements.txt        # Dependencies
├── README.md              # This file
├── MODERN_GUI.md          # Modern GUI documentation
├── QUICKSTART.md          # Quick start guide
│
├── core/                  # Core components
│   ├── engine.py          # JARVIS engine
│   ├── registry.py        # Skill registry
│   ├── voice.py           # Voice assistant
│   ├── enhanced_agent.py  # Enhanced AI agent (NEW!)
│   └── ...
│
├── gui/                   # GUI interfaces
│   ├── app.py            # Classic GUI
│   └── modern_app.py     # Modern GUI (NEW!)
│
└── skill/                 # Skills (21 skills, 69 tools)
    ├── youtube_player.py
    ├── music_ops.py
    ├── web_ops.py
    ├── system_ops.py
    └── ...
```

---

## 🎓 Skills & Tools

**21 Skills with 69 Tools:**

### **Entertainment**
- 🎵 YouTube Player
- 🎬 Movie Downloader
- 🎵 Music Operations

### **Web & Internet**
- 🌐 Web Operations
- 🔍 Internet Search
- 📧 Email Operations

### **System Control**
- 💻 System Operations
- 🎮 Master PC Control
- 📁 File Operations
- 📸 Screenshot

### **AI & Development**
- 🤖 Self-Coding AI
- 🏗️ AI Architect
- 💻 Code Generator
- 🎮 AI Game Player

### **Utilities**
- 🕐 DateTime Operations
- 🌤️ Weather Operations
- 💾 Memory Operations
- 📝 Text Operations
- 🖥️ Terminal Operations

---

## 🔧 Configuration

### **Settings** (Modern GUI)

Access via: Quick Actions → Settings

- ✅ Voice responses
- 🎨 Theme (coming soon)
- 🌐 Language preference
- 🔊 Voice settings

### **Config File**

Location: `~/.jarvis_config.json`

```json
{
  "theme": "dark",
  "voice_enabled": true,
  "auto_execute": false,
  "language": "hi-IN"
}
```

---

## 🐛 Troubleshooting

### **GUI doesn't open**
```bash
# Check tkinter
python -c "import tkinter"

# Linux: Install tkinter
sudo apt-get install python3-tk
```

### **Voice not working**
```bash
# Install dependencies
pip install SpeechRecognition pyaudio pyttsx3

# Linux: Install portaudio
sudo apt-get install portaudio19-dev
```

### **Ollama connection error**
```bash
# Start Ollama
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

---

## 🚀 Performance

### **Modern GUI**
- ⚡ Non-blocking UI
- 🚀 < 1s response time
- 💾 Memory efficient
- 🔄 Concurrent processing

### **Classic GUI**
- ✅ All-in-one file
- 🚀 Quick startup
- 💾 Lightweight
- 🔄 Simple architecture

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🙏 Credits

- **Ollama** - Local AI processing
- **Python Community** - Amazing libraries
- **Contributors** - Thank you!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Aryankaushik541/Zarves/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aryankaushik541/Zarves/discussions)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!

---

## 📈 Roadmap

### **Coming Soon**
- [ ] Custom theme support
- [ ] Plugin system
- [ ] Mobile app
- [ ] Cloud sync
- [ ] Multi-user support
- [ ] Advanced AI models
- [ ] Voice customization
- [ ] Automation workflows

---

**Made with ❤️ for the AI community**

**Choose your interface and start building with JARVIS today!** 🚀

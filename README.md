# 🤖 ZARVES - Advanced AI Agent

**Zarves** ek powerful voice-controlled AI assistant hai jo **bina kisi external API** ke kaam karta hai. Yeh **offline AI** use karta hai aur **voice commands** se browser control, system operations, aur bahut kuch kar sakta hai!

---

## ✨ Key Features

### 🎤 Voice Control (Hindi + English)
- Natural voice commands samajhta hai
- Hindi aur English dono support karta hai
- Real-time speech recognition

### 🧠 Built-in Offline AI
- **Koi API key nahi chahiye**
- Pattern matching aur learning
- Self-improving capabilities
- Conversation history maintain karta hai

### 🌐 Smart Browser Automation
- Chrome/Firefox control
- Automatic website opening
- Google/YouTube search
- Click, scroll, navigate - sab kuch automatic

### 💻 System Control
- Shutdown/Restart/Sleep
- Application control
- System information
- Screenshot capture

### 🚀 Self-Learning
- User commands se seekhta hai
- Patterns recognize karta hai
- Better responses over time

---

## 🎯 Quick Start

### 1️⃣ Installation

```bash
# Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Run Zarves Advanced

```bash
python zarves_advanced.py
```

### 3️⃣ Start Talking!

Bas bol do:
- **"Zarves open Google"** → Chrome me Google khol dega
- **"Search for Python tutorials"** → Google pe search karega
- **"Open YouTube"** → YouTube khol dega
- **"What's the time?"** → Time batayega
- **"Close browser"** → Browser band kar dega
- **"Exit"** → Zarves band ho jayega

---

## 🎮 Voice Commands Examples

### 🌐 Browser Commands
```
"Open Google"
"Open YouTube"
"Open Facebook"
"Open Instagram"
"Open Gmail"
"Open WhatsApp"
"Close browser"
```

### 🔍 Search Commands
```
"Search for Python programming"
"YouTube search funny videos"
"Find best restaurants near me"
```

### 💻 System Commands
```
"What's the time?"
"What's the date?"
"Shutdown computer"
"Restart system"
"Sleep mode"
```

### 💬 Conversation
```
"Hello Zarves"
"How are you?"
"Thank you"
"Bye"
```

---

## 📁 Project Structure

```
Zarves/
├── zarves_advanced.py          # 🆕 Main advanced AI agent
├── main.py                     # Original entry point
├── requirements.txt            # Dependencies
├── core/                       # Core AI modules
│   ├── engine.py              # AI engine
│   ├── voice.py               # Voice processing
│   ├── autonomous_coder.py    # Self-coding AI
│   └── ...
├── skill/                      # Skills/Capabilities
│   ├── smart_browser_control.py  # 🆕 Advanced browser automation
│   ├── web_ops.py             # Web operations
│   ├── system_ops.py          # System control
│   └── ...
└── gui/                        # GUI components
```

---

## 🔧 Advanced Features

### 1. Smart Browser Control

```python
from skill.smart_browser_control import SmartBrowserControl

browser = SmartBrowserControl()

# Natural language commands
browser.execute_command("open google.com")
browser.execute_command("search for AI tutorials")
browser.execute_command("click first result")
browser.execute_command("scroll down")
browser.execute_command("go back")
browser.execute_command("close browser")
```

### 2. Offline AI Brain

```python
from zarves_advanced import OfflineAI

ai = OfflineAI()

# Understand commands
action = ai.understand("open google")
# Returns: {"action": "open_browser", "url": "https://www.google.com"}

# Learn from interactions
ai._learn("new command pattern")
```

### 3. Voice Engine

```python
from zarves_advanced import VoiceEngine

voice = VoiceEngine()

# Speak
voice.speak("Hello! Main Zarves hoon")

# Listen
command = voice.listen()
print(f"User said: {command}")
```

---

## 🎯 How It Works

### 1. Voice Input
```
User speaks → Microphone captures → Speech Recognition
```

### 2. AI Processing
```
Text → Pattern Matching → Action Decision → Learning
```

### 3. Action Execution
```
Browser Control / System Command / Response Generation
```

### 4. Voice Output
```
Text Response → Text-to-Speech → Speaker
```

---

## 🆚 Zarves vs Other AI Assistants

| Feature | Zarves | Others |
|---------|--------|--------|
| **Offline AI** | ✅ Built-in | ❌ Need API |
| **Voice Control** | ✅ Hindi + English | ⚠️ Limited |
| **Browser Automation** | ✅ Full control | ❌ Basic |
| **Self-Learning** | ✅ Yes | ❌ No |
| **No API Keys** | ✅ Free | ❌ Paid |
| **Open Source** | ✅ Yes | ⚠️ Limited |

---

## 🛠️ Dependencies

### Core Requirements
```
pyttsx3              # Text-to-speech
SpeechRecognition    # Voice recognition
selenium             # Browser automation
webdriver-manager    # Auto driver management
psutil               # System control
pyautogui            # GUI automation
```

### Optional (for advanced features)
```
ollama               # Local LLM (optional)
opencv-python        # Computer vision
pyaudio              # Audio processing
```

---

## 🎓 Usage Examples

### Example 1: Open Website
```python
# Voice: "Zarves open Google"
# Action: Opens google.com in Chrome
```

### Example 2: Search
```python
# Voice: "Search for best Python courses"
# Action: Opens Google and searches
```

### Example 3: System Control
```python
# Voice: "What's the time?"
# Response: "Abhi time hai 03:30 PM"
```

---

## 🔐 Privacy & Security

- ✅ **Fully Offline** - Koi data internet pe nahi jata
- ✅ **No API Keys** - Koi external service nahi
- ✅ **Local Processing** - Sab kuch aapke computer pe
- ✅ **Open Source** - Code dekh sakte ho

---

## 🐛 Troubleshooting

### Microphone not working?
```bash
# Check microphone permissions
# Windows: Settings → Privacy → Microphone
# Linux: Check ALSA/PulseAudio settings
```

### Browser not opening?
```bash
# Install Chrome/Chromium
# Or install Firefox and modify code
pip install selenium webdriver-manager
```

### Voice not clear?
```python
# Adjust voice settings in code
engine.setProperty('rate', 150)  # Slower
engine.setProperty('volume', 1.0)  # Louder
```

---

## 🚀 Future Enhancements

- [ ] WhatsApp automation
- [ ] Email sending
- [ ] Calendar management
- [ ] Smart home control
- [ ] Multi-language support
- [ ] GUI interface
- [ ] Mobile app
- [ ] Cloud sync (optional)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📄 License

MIT License - Free to use and modify

---

## 👨‍💻 Original Projects

### Aadhar ATM Automation
Original ATM automation features still available:
```bash
python launch_aadhar_atm.py
```

### Autonomous Coder
Self-coding AI capabilities:
```bash
python autonomous_coder_cli.py
```

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Aryankaushik541/Zarves/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aryankaushik541/Zarves/discussions)

---

## 🌟 Star History

Agar project pasand aaya to ⭐ star zaroor dena!

---

**Made with ❤️ by Aryan Kaushik**

**Powered by Offline AI - No API Keys Required!**

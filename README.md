# 🤖 JARVIS - Your Personal AI Assistant (Bilkul Human Jaisa!)

> **"Main sirf assist nahi karta. Main samajhta hoon, yaad rakhta hoon, aur bilkul insaan ki tarah baat karta hoon."**

JARVIS is an **intelligent personal AI assistant** that behaves like a real human:
- ✅ **🎤 VOICE MODE** - Talk naturally, no typing needed! Just say "Jarvis" and speak!
- ✅ **NATURAL CONVERSATIONS** - Talks like a real person, not a robot!
- ✅ **EMOTION DETECTION** - Understands if you're happy, frustrated, or excited
- ✅ **CONTEXT MEMORY** - Remembers previous conversations and tasks
- ✅ **CROSS-PLATFORM APP INSTALLER** - Windows (MS Store) + Mac (App Store) + Linux (apt/snap) 📦
- ✅ **OPENS ANY APP** - This PC, Control Panel, VLC, Word, Excel, and 50+ apps! 🖥️
- ✅ **AUTO-PLAY MUSIC** - "YouTube kholo" automatically plays trending songs! 🎵
- ✅ **AUTO-INSTALLS EVERYTHING** - Just run `python main.py` and it handles the rest!
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **MOVIE DOWNLOADER** - Download and play movies with VLC
- ✅ **SELF-HEALING** - Fixes its own errors using AI + internet
- ✅ **HINGLISH SUPPORT** - Speak naturally in Hindi, English, or mixed!

---

## 💬 Natural Conversation Examples

### **Example 1: Install Apps (Cross-Platform) 📦**

**Windows:**
```
🎤 You: "Jarvis, WhatsApp install karo"

🔊 JARVIS: "Installing WhatsApp from Microsoft Store..."
          [Microsoft Store opens to WhatsApp page]
          "Click 'Get' or 'Install' to download WhatsApp."
```

**Mac:**
```
🎤 You: "Jarvis, Spotify install karo"

🔊 JARVIS: "Installing Spotify from Mac App Store..."
          [Mac App Store opens to Spotify page]
          "Click 'Get' or 'Install' to download Spotify."
```

**Linux:**
```
🎤 You: "Jarvis, VLC install karo"

🔊 JARVIS: "Installing VLC via snap..."
          [Installs automatically]
          "VLC installed successfully!"
```

**Supported Apps (50+):**
- 📱 **Social**: WhatsApp, Telegram, Discord, Zoom, Teams, Skype, Slack
- 🎵 **Entertainment**: Spotify, Netflix, Prime Video, VLC
- 💼 **Productivity**: Notion, Evernote, OneNote, Pages, Numbers, Keynote
- 💻 **Development**: VS Code, Xcode, Windows Terminal, PowerShell, Git, Python
- 🎮 **Gaming**: Xbox, Steam
- 🌐 **Browsers**: Chrome, Firefox, Edge, Brave, Safari
- 📊 **Office**: Word, Excel, PowerPoint, Outlook
- 🛠️ **Utilities**: WinRAR, 7-Zip, Notepad++, Paint.NET, The Unarchiver, Magnet

### **Example 2: Voice Mode - Just Talk! 🎤**

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

### **Example 3: Opens ANY Application**

```
🎤 You: "Jarvis, this pc kholo"

🔊 JARVIS: "Opening This PC. Done!"

🎤 You: "control panel kholo"

🔊 JARVIS: "Opening Control Panel. Done!"

🎤 You: "vlc kholo"

🔊 JARVIS: "Opening VLC Media Player. Done!"
```

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
- ✅ Detects your platform (Windows/Mac/Linux)
- ✅ Installs missing packages
- ✅ Downloads Ollama model
- ✅ Starts running!

---

## 🌟 Key Features

### **📦 Cross-Platform App Installer (NEW!)**

Install apps with voice commands on **any platform**:

**Windows (Microsoft Store):**
```
🎤 "Jarvis, WhatsApp install karo"
🎤 "Jarvis, Spotify download karo"
🎤 "Jarvis, VS Code install karo"
```

**Mac (Mac App Store + Homebrew):**
```
🎤 "Jarvis, Telegram install karo"
🎤 "Jarvis, Notion download karo"
🎤 "Jarvis, Xcode install karo"
```

**Linux (apt/snap/flatpak):**
```
🎤 "Jarvis, VLC install karo"
🎤 "Jarvis, Firefox download karo"
```

**How it works:**
- **Windows**: Opens Microsoft Store → Click "Get/Install"
- **Mac**: Opens Mac App Store → Click "Get/Install"
- **Linux**: Auto-installs via snap/apt

**Fallback Methods:**
- Windows: winget (if MS Store fails)
- Mac: Homebrew (if App Store fails)
- Linux: apt → snap → flatpak

### **🎤 Voice Mode**
- Wake Word Detection - Say "Jarvis" to activate
- Continuous Listening - No need to repeat wake word
- Hindi + English Support
- Natural Voice Response
- Emotion Detection

### **🖥️ Opens ANY App (50+)**
- System Tools (This PC, Control Panel, Settings)
- Office Apps (Word, Excel, PowerPoint)
- Media Players (VLC, Spotify)
- Browsers (Chrome, Firefox, Edge)
- Development Tools (VS Code, CMD, PowerShell)

### **🎵 Auto-Play Music**
- "YouTube kholo" → Plays trending song automatically
- Uses Selenium to click and play video
- No manual clicking needed!

### **🎬 Movie Downloader**
- Download from vegamovies, etc.
- Auto-opens in VLC player

### **🔧 Self-Healing**
- Fixes its own errors using AI
- Searches internet for solutions
- Auto-repairs code

---

## 💬 Usage Examples

### **Installing Apps (Cross-Platform)**

**Windows:**
```
🎤 You: "Jarvis, WhatsApp install karo"
🔊 JARVIS: "Installing WhatsApp from Microsoft Store..."
          [Opens MS Store]

🎤 You: "Spotify download karo"
🔊 JARVIS: "Installing Spotify..."
          [Opens MS Store]
```

**Mac:**
```
🎤 You: "Jarvis, Telegram install karo"
🔊 JARVIS: "Installing Telegram from Mac App Store..."
          [Opens Mac App Store]

🎤 You: "Notion download karo"
🔊 JARVIS: "Installing Notion..."
          [Opens Mac App Store]
```

**Linux:**
```
🎤 You: "Jarvis, VLC install karo"
🔊 JARVIS: "Installing VLC via snap..."
          [Auto-installs]
          "VLC installed successfully!"
```

### **Opening Apps**
```
🎤 You: "Jarvis, this pc kholo"
🔊 JARVIS: "Opening This PC. Done!"

🎤 You: "vlc kholo"
🔊 JARVIS: "Opening VLC. Done!"
```

### **Playing Music**
```
🎤 You: "Jarvis, youtube kholo"
🔊 JARVIS: "Playing trending song..."
          [Auto-plays music]
```

---

## 🛠️ Requirements

- **Python 3.8+**
- **Ollama** (for AI model)
- **Windows 10/11 / macOS / Linux**
- **Internet Connection**

**All dependencies auto-install!**

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Run JARVIS (auto-installs everything!)
python main.py
```

---

## 💡 Platform-Specific Features

### **Windows**
- Microsoft Store app installation
- Opens 50+ Windows apps
- System tools (This PC, Control Panel, etc.)
- Winget fallback

### **Mac**
- Mac App Store installation
- Homebrew fallback
- macOS-specific apps (Xcode, Pages, etc.)
- Safari, Finder, etc.

### **Linux**
- snap/apt/flatpak support
- Auto-detects best package manager
- Works on Ubuntu, Debian, Fedora, etc.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

**Made with ❤️ by Aryan Kaushik**

**⭐ Star this repo if you find it useful!**

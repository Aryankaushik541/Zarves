# 🤖 JARVIS - Your Personal AI Assistant (Bilkul Human Jaisa!)

> **"Main sirf assist nahi karta. Main samajhta hoon, yaad rakhta hoon, aur bilkul insaan ki tarah baat karta hoon."**

JARVIS is an **intelligent personal AI assistant** that behaves like a real human:
- ✅ **🎤 VOICE MODE** - Talk naturally, no typing needed! Just say "Jarvis" and speak!
- ✅ **NATURAL CONVERSATIONS** - Talks like a real person, not a robot!
- ✅ **EMOTION DETECTION** - Understands if you're happy, frustrated, or excited
- ✅ **CONTEXT MEMORY** - Remembers previous conversations and tasks
- ✅ **INSTALLS APPS FROM MS STORE** - "WhatsApp install karo" → Downloads & installs automatically! 📦
- ✅ **OPENS ANY WINDOWS APP** - This PC, Control Panel, VLC, Word, Excel, and 50+ apps! 🖥️
- ✅ **AUTO-PLAY MUSIC** - "YouTube kholo" automatically plays trending songs! 🎵
- ✅ **AUTO-INSTALLS EVERYTHING** - Just run `python main.py` and it handles the rest!
- ✅ **100% FREE & LOCAL** - Uses Ollama (no API keys, no rate limits!)
- ✅ **MOVIE DOWNLOADER** - Download and play movies with VLC
- ✅ **SELF-HEALING** - Fixes its own errors using AI + internet
- ✅ **HINGLISH SUPPORT** - Speak naturally in Hindi, English, or mixed!

---

## 💬 Natural Conversation Examples

### **Example 1: Install Apps from Microsoft Store 📦**

```
🎤 You: "Jarvis, WhatsApp install karo"

🔊 JARVIS: "Installing WhatsApp from Microsoft Store..."
          [Microsoft Store opens to WhatsApp page]
          "Microsoft Store opened. Click 'Get' or 'Install' to download WhatsApp."

🎤 You: "Spotify install karo"

🔊 JARVIS: "Installing Spotify..."
          [Microsoft Store opens to Spotify page]
          "Done! Click 'Install' to get Spotify."
```

**Supported Apps (50+):**
- 📱 **Social**: WhatsApp, Telegram, Discord, Zoom, Teams, Skype
- 🎵 **Entertainment**: Spotify, Netflix, Prime Video, VLC
- 💼 **Productivity**: Notion, Evernote, OneNote
- 💻 **Development**: VS Code, Windows Terminal, PowerShell, Git, Python
- 🎮 **Gaming**: Xbox, Steam, Epic Games
- 🌐 **Browsers**: Chrome, Firefox, Edge, Brave
- 📊 **Office**: Word, Excel, PowerPoint, Outlook
- 🛠️ **Utilities**: WinRAR, 7-Zip, Notepad++, Paint.NET

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

**No typing needed! Just talk naturally like you're talking to a friend!** 🗣️

### **Example 3: Opens ANY Windows Application**

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
- ✅ Checks all dependencies
- ✅ Installs missing packages
- ✅ Downloads Ollama model
- ✅ Starts running!

---

## 🌟 Key Features

### **📦 Microsoft Store App Installer (NEW!)**

Install any app from Microsoft Store with just a voice command!

```
🎤 You: "Jarvis, WhatsApp install karo"
🔊 JARVIS: "Installing WhatsApp from Microsoft Store..."
          [Opens MS Store to WhatsApp page]

🎤 You: "Spotify download karo"
🔊 JARVIS: "Installing Spotify..."
          [Opens MS Store to Spotify page]
```

**How it works:**
1. 🔍 Searches for app in Microsoft Store database
2. 🏪 Opens Microsoft Store to app page
3. 💡 You click "Get" or "Install" button
4. ✅ App downloads and installs automatically!

**Supported Categories:**
- 📱 Social & Communication (WhatsApp, Telegram, Discord, Zoom, Teams)
- 🎵 Entertainment (Spotify, Netflix, Prime Video, VLC)
- 💼 Productivity (Notion, Evernote, OneNote)
- 💻 Development (VS Code, Windows Terminal, Git, Python)
- 🎮 Gaming (Xbox, Steam, Epic Games)
- 🌐 Browsers (Chrome, Firefox, Edge, Brave)
- 📊 Office (Word, Excel, PowerPoint, Outlook)
- 🛠️ Utilities (WinRAR, 7-Zip, Notepad++, Paint.NET)

**Commands:**
```
🎤 "Jarvis, WhatsApp install karo"
🎤 "Jarvis, Spotify download karo"
🎤 "Jarvis, VS Code install karo"
🎤 "Jarvis, Netflix install karo"
🎤 "Jarvis, Chrome download karo"
```

### **🎤 Voice Mode**
- Wake Word Detection - Say "Jarvis" to activate
- Continuous Listening - No need to repeat wake word
- Hindi + English Support
- Natural Voice Response
- Emotion Detection

### **🖥️ Opens ANY Windows App (50+)**
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

### **Installing Apps**
```
🎤 You: "Jarvis, WhatsApp install karo"
🔊 JARVIS: "Installing WhatsApp..."
          [Opens MS Store]

🎤 You: "Spotify download karo"
🔊 JARVIS: "Installing Spotify..."
          [Opens MS Store]
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

- Python 3.8+
- Ollama (for AI model)
- Windows 10/11
- Internet Connection

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

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

**Made with ❤️ by Aryan Kaushik**

**⭐ Star this repo if you find it useful!**

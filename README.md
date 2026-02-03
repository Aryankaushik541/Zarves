# 🤖 JARVIS - Your Personal AI Assistant

> **"Just Run main.py - Everything Auto-Installs!"**

Complete AI assistant with **automatic setup**, **browser auto-login**, **PC movie search**, **VLC auto-play**, and **local AI**!

---

## 🚀 Super Simple Setup - Just 2 Commands!

```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Run (everything auto-installs!)
python main.py
```

**That's it!** 🎉

The script automatically:
- ✅ Installs Python dependencies
- ✅ Installs Ollama (if needed)
- ✅ Starts Ollama server
- ✅ Downloads AI model (llama3.2)
- ✅ Launches beautiful GUI

**No manual setup needed!**

---

## 📺 What Happens When You Run

```
🤖 JARVIS - Personal AI Assistant
======================================================================

📦 Checking Python dependencies...
   ✅ All dependencies installed!

🤖 Setting up AI Engine (Ollama)...
   ✅ Ollama found!
   ✅ Ollama server running!
   ✅ AI model ready!

✅ AI Engine ready!

🚀 Launching JARVIS GUI...

💡 Full Mode Enabled:
   ✅ Local AI processing
   ✅ Natural conversations
   ✅ Smart task execution

🎵 Features:
   ✅ YouTube Auto-Play
   ✅ Browser Auto-Login
   ✅ PC Movie Search
   ✅ VLC Auto-Play
   ✅ Voice & Text Control

======================================================================
```

Then the beautiful GUI opens! 🎨

---

## ⚡ First Time Setup

### **If Ollama Not Installed:**

When you run `python main.py`, it will ask:

```
⚠️  Ollama not found!

Install Ollama now? (y/n): y
```

Type **y** and press Enter. It will:
1. Install Ollama automatically (Mac/Linux)
2. Or guide you to download (Windows)
3. Start Ollama server
4. Download AI model

**Windows Users:**
- Script will open download link
- Install Ollama
- Press Enter to continue
- Script will handle the rest!

### **If Model Not Downloaded:**

```
⚠️  AI model (llama3.2) not found

Download model now? (y/n): y
```

Type **y** and press Enter. It will download the model (~2GB).

---

## ✨ Features

### 🤖 **Automatic Setup**
```
✅ One command to rule them all
✅ Auto-installs everything
✅ No manual configuration
✅ Works on Windows, Mac, Linux
```

### 🧠 **Local AI Processing**
```
✅ Runs completely offline
✅ No API keys needed
✅ Fast and private
✅ Uses Ollama + llama3.2

Your data stays on your PC!
```

### 🔐 **Browser Auto-Login**
```
✅ Opens browser automatically
✅ Logs in with Google credentials
✅ No manual typing needed!

Supported:
- Gmail (Auto-login)
- YouTube (Auto-login)
- Facebook (Auto-login)
- Twitter (Auto-login)
```

### 🎬 **PC Movie Search**
```
✅ Searches entire PC storage
✅ Finds movies by name
✅ Supports all video formats
✅ Shows results instantly

Formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM
```

### 🎥 **VLC Auto-Play**
```
✅ Searches movie on PC
✅ Opens VLC automatically
✅ Starts playing movie
✅ Fully automatic!

Example:
Say: "Avengers movie play karo VLC me"
Result: Finds Avengers, opens VLC, plays automatically!
```

---

## 💬 Commands

### **🔐 Auto-Login:**
```
"gmail login karo" → Opens Gmail and logs in automatically
"youtube login karo" → Opens YouTube and logs in automatically
"facebook login karo" → Opens Facebook and logs in automatically
"twitter login karo" → Opens Twitter and logs in automatically
```

### **🎬 Movie Search:**
```
"Avengers movie search karo" → Searches PC for Avengers
"Interstellar movie dhundo" → Finds Interstellar on PC
"movie search karo" → Shows all movies
```

### **🎥 VLC Auto-Play:**
```
"Avengers movie play karo VLC me" → Finds & plays in VLC
"Interstellar chalao VLC me" → Finds & plays in VLC
"movie play karo" → Plays last searched movie
```

### **🎵 YouTube Auto-Play:**
```
"honey singh ka gaana bajao" → Auto-plays Honey Singh
"Kesariya bajao" → Auto-plays Kesariya
"arijit singh ka gaana bajao" → Auto-plays Arijit Singh
"youtube kholo" → Opens YouTube with trending music
```

### **🌐 Web (Quick Access):**
```
"gmail kholo" → Opens Gmail
"facebook kholo" → Opens Facebook
"youtube kholo" → Opens YouTube
"google search karo X" → Searches Google for X
```

### **📱 Applications:**
```
"chrome kholo" → Opens Chrome
"word kholo" → Opens Word
"vlc kholo" → Opens VLC
"calculator kholo" → Opens Calculator
```

### **🔊 System Control:**
```
"volume badhao" → Increases volume
"volume kam karo" → Decreases volume
"mute karo" → Mutes audio
```

### **⚡ Power:**
```
"lock karo" → Locks PC
"sleep karo" → Sleep mode
```

### **💬 Natural Conversation:**
```
"hello jarvis" → Greets you warmly
"what's the weather?" → Tells weather
"tell me a joke" → Tells a joke
"thanks" → Responds warmly
```

---

## ⚙️ Configuration (Optional)

### **1. Configure Auto-Login:**
```
1. Click "⚙️ Settings" button (top-right in GUI)
2. Enter Google Email
3. Enter Google Password
4. Click "Save Settings"

Now JARVIS can auto-login to Gmail, YouTube, Facebook!
```

### **2. Add Movie Folders:**
```
1. Click "⚙️ Settings" button
2. Scroll to "Movie Search Paths"
3. Click "Add Folder"
4. Select your movie folders
5. Click "Save Settings"

JARVIS will search these folders for movies!
```

**Default Paths (Auto-detected):**
- Windows: C:\Users\YourName\Videos, Downloads, Movies
- All Drives: D:\Movies, E:\Videos, etc.

---

## 🎨 GUI Interface

### **Beautiful Visual Interface:**
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 JARVIS | Auto-Login | Movie Search | VLC Play           │
│                                    [⚙️ Settings] [● Ready]  │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  Quick Actions   │         Chat with JARVIS                │
│                  │                                          │
│  🌐 Web          │  💬 Type or speak your commands         │
│    • Gmail ✅    │                                          │
│    • YouTube ✅  │  [08:58:46] 👤 YOU: hello jarvis        │
│    • Facebook ✅ │  [08:58:47] 🤖 JARVIS: Hello! How can   │
│                  │             I help you today? 😊         │
│  🎬 Movies       │                                          │
│    • Search ✅   │  [08:59:12] 👤 YOU: youtube kholo       │
│    • Play VLC ✅ │  [08:59:13] 🤖 JARVIS: Opening YouTube  │
│                  │             with trending music! 🎵      │
│  📱 Apps         │                                          │
│    • Chrome      │                                          │
│    • VLC ✅      │  ┌────────────────────────────────────┐ │
│    • Calculator  │  │ Type your message...               │ │
│                  │  │                        [🎤] [Send] │ │
│  🎵 Media        │  └────────────────────────────────────┘ │
│    • Play ✅     │                                          │
│    • Pause       │                                          │
│                  │                                          │
│  🔊 System       │                                          │
│    • Volume      │                                          │
│    • Mute        │                                          │
│                  │                                          │
│  ⚡ Power        │                                          │
│    • Lock        │                                          │
│    • Sleep       │                                          │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### **Problem: "Ollama installation failed"**

**Windows:**
1. Download manually: https://ollama.com/download/windows
2. Run installer
3. Run `python main.py` again

**Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
python main.py
```

### **Problem: "Model download failed"**

```bash
# Open terminal and run:
ollama serve

# In another terminal:
ollama pull llama3.2

# Then run JARVIS:
python main.py
```

### **Problem: "Module not found"**

```bash
pip install -r requirements.txt
python main.py
```

### **Problem: "JARVIS running in limited mode"**

This means Ollama is not available. JARVIS will still work but with basic commands only.

**To enable full mode:**
1. Install Ollama: https://ollama.com/download
2. Run: `ollama serve`
3. Run: `ollama pull llama3.2`
4. Restart JARVIS: `python main.py`

---

## 📊 System Requirements

### **Minimum:**
- Python 3.8+
- 4GB RAM
- 5GB free disk space (for AI model)
- Windows 10/11, macOS 10.15+, or Linux

### **Recommended:**
- Python 3.10+
- 8GB RAM
- 10GB free disk space
- SSD for faster AI processing

---

## 🔒 Privacy & Security

### **Your Data is Safe:**
```
✅ All AI processing happens locally
✅ No data sent to cloud
✅ Credentials stored locally only
✅ Open source - audit the code
✅ No telemetry or tracking
```

### **Credentials:**
- Stored in `~/.jarvis_config.json`
- Never shared or uploaded
- You can delete anytime

---

## 🎯 How It Works

### **1. Automatic Setup:**
```
You run: python main.py

JARVIS:
1. Checks Python dependencies → Installs if missing
2. Checks Ollama → Asks to install if missing
3. Checks Ollama server → Starts if not running
4. Checks AI model → Downloads if missing
5. Launches beautiful GUI

Result: Everything ready in 5 minutes!
```

### **2. Local AI Processing:**
```
You say: "What's the weather like?"

JARVIS:
1. Processes query with Ollama (local AI)
2. Understands intent
3. Executes appropriate skill
4. Responds naturally

Result: All processing happens on your PC!
        No data sent to cloud!
```

### **3. Smart Task Execution:**
```
You say: "Avengers movie play karo VLC me"

JARVIS:
1. Understands: Search movie + Play in VLC
2. Searches PC for "Avengers"
3. Finds movie file
4. Opens VLC with movie
5. Movie starts playing!

Result: Complex task done automatically!
```

---

## 🛠️ Development

### **Project Structure:**
```
Zarves/
├── main.py              # Entry point (auto-setup + launch)
├── core/                # Core engine
│   ├── engine.py        # AI engine
│   ├── registry.py      # Skill registry
│   ├── voice.py         # Voice assistant
│   └── ...
├── gui/                 # GUI interface
│   └── app.py           # Main GUI
├── skill/               # Skills (plugins)
│   ├── web_skills.py
│   ├── media_skills.py
│   └── ...
└── requirements.txt     # Dependencies
```

### **Add Custom Skills:**

Create a new file in `skill/` folder:

```python
# skill/my_custom_skill.py

def my_function(param1: str) -> dict:
    """
    Description of what this does
    
    Args:
        param1: Description of parameter
    
    Returns:
        dict: Result
    """
    # Your code here
    return {"status": "success", "message": "Done!"}
```

JARVIS automatically loads it!

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - See LICENSE file

---

## 🆘 Support

- **Issues:** https://github.com/Aryankaushik541/Zarves/issues
- **Detailed Fixes:** [FIXES.md](FIXES.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)

---

## 🎉 Credits

Built with:
- Ollama (Local AI)
- llama3.2 (AI Model)
- PyQt5 (GUI)
- Selenium (Browser automation)
- pyttsx3 (Voice)

---

## ⭐ Star This Repo!

If you find JARVIS helpful, please star this repo! ⭐

It helps others discover this project!

---

**Made with ❤️ by Aryan Kaushik**

**Just run `python main.py` and enjoy! 🚀**

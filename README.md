# 🤖 JARVIS - Your Personal AI Assistant

> **"Just Run `python main.py` - GUI Window Opens Automatically!"**

Complete AI assistant with **automatic setup**, **GUI window**, **browser auto-login**, **PC movie search**, **VLC auto-play**, and **local AI**!

---

## 🚀 Super Simple Setup - Just 2 Commands!

```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Run (GUI window opens automatically!)
python main.py
```

**That's it!** 🎉

The script automatically:
- ✅ Installs Python dependencies
- ✅ Installs Ollama (if needed)
- ✅ Starts Ollama server
- ✅ Downloads AI model (llama3.2)
- ✅ **Opens beautiful GUI window**

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

🚀 Launching JARVIS GUI...

✅ GUI window opened!
💡 If you don't see the window, check your taskbar
```

**Then a beautiful GUI window opens!** 🎨

---

## 🎨 GUI Interface

The GUI window shows:

```
┌─────────────────────────────────────────────────────────┐
│         🤖 JARVIS - Personal AI Assistant               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [09:19:04] ⚙️ SYSTEM: 📦 Loading skills...           │
│  [09:19:05] ⚙️ SYSTEM: 🧠 Initializing AI engine...   │
│  [09:19:07] ⚙️ SYSTEM: 🎤 Voice assistant ready!      │
│  [09:19:07] 🤖 JARVIS: ✅ JARVIS Ready!               │
│                                                         │
│             📊 Loaded 21 skills with 69 tools          │
│                                                         │
│             💬 How can I help you today?               │
│                                                         │
│  [09:20:15] 👤 You: youtube kholo                     │
│  [09:20:16] 🤖 JARVIS: Opening YouTube! 🎵            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Type your message...              [Send] [🎤 Voice]   │
├─────────────────────────────────────────────────────────┤
│  ● Ready                                                │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🎨 **Beautiful GUI Window**
- Modern dark theme interface
- Real-time chat display
- Text and voice input
- Status indicators
- Automatic window opening

### 🤖 **Automatic Setup**
- One command to rule them all
- Auto-installs everything
- No manual configuration
- Works on Windows, Mac, Linux

### 🧠 **Local AI Processing**
- Runs completely offline
- No API keys needed
- Fast and private
- Uses Ollama + llama3.2
- Your data stays on your PC!

### 🔐 **Browser Auto-Login**
- Opens browser automatically
- Logs in with Google credentials
- No manual typing needed!
- Supported: Gmail, YouTube, Facebook, Twitter

### 🎬 **PC Movie Search**
- Searches entire PC storage
- Finds movies by name
- Supports all video formats (MP4, MKV, AVI, MOV, WMV, FLV, WEBM)
- Shows results instantly

### 🎥 **VLC Auto-Play**
- Searches movie on PC
- Opens VLC automatically
- Starts playing movie
- Fully automatic!

### 🎵 **YouTube Auto-Play**
- Opens YouTube with Selenium
- Auto-plays songs/videos
- Trending music support
- Natural language commands

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

## 🔧 Troubleshooting

### **Problem: GUI window not opening**

**Solution 1 - Check taskbar:**
```
The window might be minimized or behind other windows.
Check your taskbar for "JARVIS" window.
```

**Solution 2 - Install tkinter:**
```bash
# Linux:
sudo apt-get install python3-tk

# Mac:
brew install python-tk

# Windows:
# Reinstall Python with tkinter support from python.org
```

**Solution 3 - Run directly:**
```bash
python jarvis_gui.py
```

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
# Open terminal 1:
ollama serve

# Open terminal 2:
ollama pull llama3.2

# Open terminal 3:
cd Zarves
python main.py
```

### **Problem: "Module not found"**

```bash
pip install -r requirements.txt
python main.py
```

---

## ⚙️ Configuration (Optional)

### **1. Configure Auto-Login:**

In the GUI window:
```
1. Type: "settings" or click Settings button (if available)
2. Or manually edit: ~/.jarvis_config.json
3. Add your Google credentials:
   {
     "google_email": "your@gmail.com",
     "google_password": "yourpassword"
   }
```

### **2. Add Movie Folders:**

Edit `~/.jarvis_config.json`:
```json
{
  "movie_paths": [
    "D:\\Movies",
    "E:\\Videos",
    "C:\\Users\\YourName\\Downloads"
  ]
}
```

**Default Paths (Auto-detected):**
- Windows: C:\Users\YourName\Videos, Downloads, Movies
- All Drives: D:\Movies, E:\Videos, etc.

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
- ✅ All AI processing happens locally
- ✅ No data sent to cloud
- ✅ Credentials stored locally only
- ✅ Open source - audit the code
- ✅ No telemetry or tracking

### **Credentials:**
- Stored in `~/.jarvis_config.json`
- Never shared or uploaded
- You can delete anytime

---

## 🛠️ Development

### **Project Structure:**
```
Zarves/
├── main.py              # Entry point (auto-setup + launch)
├── jarvis_gui.py        # Simple GUI (guaranteed to work)
├── core/                # Core engine
│   ├── engine.py        # AI engine
│   ├── registry.py      # Skill registry
│   ├── voice.py         # Voice assistant
│   └── ...
├── gui/                 # Advanced GUI (optional)
│   └── app.py           # Full-featured GUI
├── skill/               # Skills (plugins)
│   ├── web_skills.py
│   ├── media_skills.py
│   └── ...
└── requirements.txt     # Dependencies
```

### **Run Different GUIs:**

```bash
# Simple GUI (recommended):
python main.py

# Or directly:
python jarvis_gui.py

# Advanced GUI (if you prefer):
python gui/app.py
```

---

## 💡 Tips & Tricks

### **Faster Commands:**
```
Instead of: "open youtube and play honey singh song"
Just say: "honey singh ka gaana bajao"
```

### **Natural Language:**
```
✅ "youtube kholo" (works)
✅ "open youtube" (works)
✅ "youtube chalao" (works)
✅ "yt kholo" (works)

All variations work!
```

### **Voice vs Text:**
```
Voice: Click 🎤 Voice button
Text: Type in input box and press Enter

Use what's comfortable!
```

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
- **Ollama Docs:** https://ollama.com/docs

---

## 🎉 Credits

Built with:
- Ollama (Local AI)
- llama3.2 (AI Model)
- Tkinter (GUI)
- Selenium (Browser automation)
- pyttsx3 (Voice)

---

## ⭐ Star This Repo!

If you find JARVIS helpful, please star this repo! ⭐

It helps others discover this project!

---

**Made with ❤️ by Aryan Kaushik**

**Just run `python main.py` and the GUI window opens! 🚀**

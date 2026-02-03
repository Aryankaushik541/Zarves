# 🤖 JARVIS - Your Personal AI Assistant

> **"Auto-Login | PC Movie Search | VLC Auto-Play | Local AI"**

Complete AI assistant with **browser auto-login**, **PC movie search**, **VLC auto-play**, and **local AI** support!

---

## 🚀 Quick Start (Recommended)

### **One-Click Launch:**

**Windows:**
```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
start_jarvis.bat
```

**Mac/Linux:**
```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
chmod +x start_jarvis.sh
./start_jarvis.sh
```

**That's it!** The script automatically:
- ✅ Installs Ollama (if needed)
- ✅ Starts Ollama server
- ✅ Downloads AI model
- ✅ Installs dependencies
- ✅ Launches JARVIS GUI

---

## 📋 Manual Setup (If Needed)

### **Step 1: Install Ollama**

JARVIS uses Ollama for local AI processing.

**Windows:**
1. Download: https://ollama.com/download/windows
2. Run installer
3. Open PowerShell and run: `ollama serve`

**Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

### **Step 2: Download AI Model**

Open a **new terminal** (keep `ollama serve` running):
```bash
ollama pull llama3.2
```

This downloads the AI model (~2GB). Wait for completion.

### **Step 3: Install Dependencies**

```bash
cd Zarves
pip install -r requirements.txt
```

### **Step 4: Launch JARVIS**

```bash
python main.py
```

**Expected Output:**
```
✅ Connected to Ollama at http://localhost:11434
✅ Using model: llama3.2
🚀 Launching JARVIS GUI...
```

---

## ⚠️ Troubleshooting

### **Problem: "JARVIS engine not initialized"**

**Solution:**
```bash
# Make sure Ollama is running:
ollama serve

# In another terminal, check if model exists:
ollama list

# Should show llama3.2
# If not, pull it:
ollama pull llama3.2

# Restart JARVIS:
python main.py
```

### **Problem: "Ollama connection issue"**

**Solution:**
```bash
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# If error, start Ollama:
ollama serve

# Then restart JARVIS
```

### **Problem: "Module not found"**

**Solution:**
```bash
# Reinstall dependencies:
pip install --upgrade -r requirements.txt

# If PyQt5 fails on Mac:
pip install PyQt5 --no-cache-dir
```

### **Still Having Issues?**

See detailed fixes: [FIXES.md](FIXES.md)

---

## ✨ Features

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

### 🤖 **Local AI Processing**
```
✅ Runs completely offline
✅ No API keys needed
✅ Fast and private
✅ Uses Ollama + llama3.2

Your data stays on your PC!
```

---

## ⚙️ Configuration (Optional)

### **1. Configure Auto-Login:**
```
1. Click "⚙️ Settings" button (top-right)
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

### **3. Create .env File (Advanced):**

Create `.env` in project root:

```bash
# AI Model
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Voice Settings
VOICE_ENABLED=true
VOICE_RATE=150
VOICE_VOLUME=0.9

# Auto-Login (Optional)
GOOGLE_EMAIL=your_email@gmail.com
GOOGLE_PASSWORD=your_password

# Movie Search Paths (Optional)
MOVIE_PATHS=C:\Users\YourName\Videos,D:\Movies
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
```

### **🌐 Web (Quick Access):**
```
"gmail kholo" → Opens Gmail
"facebook kholo" → Opens Facebook
"youtube kholo" → Opens YouTube
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

---

## 🎯 How It Works

### **1. Browser Auto-Login:**
```
You say: "gmail login karo"

JARVIS:
1. Opens Chrome with Selenium
2. Goes to Gmail
3. Enters your email (from settings)
4. Enters your password (from settings)
5. Clicks login automatically
6. You're logged in!

Result: ✅ Logged into Gmail!
        🌐 Browser opened with auto-login
```

### **2. PC Movie Search:**
```
You say: "Avengers movie search karo"

JARVIS:
1. Searches all configured folders
2. Looks for "Avengers" in filename
3. Checks all video formats (MP4, MKV, etc.)
4. Shows all matches

Result: 🎬 Found 3 movie(s):
        1. Avengers Endgame.mp4
        2. Avengers Infinity War.mkv
        3. The Avengers.avi
```

### **3. VLC Auto-Play:**
```
You say: "Avengers movie play karo VLC me"

JARVIS:
1. Searches PC for "Avengers"
2. Finds movie file
3. Locates VLC player
4. Opens VLC with movie
5. Movie starts playing!

Result: 🎬 Playing in VLC:
        Avengers Endgame.mp4
        ✅ Movie started!
```

### **4. Local AI Processing:**
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

---

## 🎨 GUI Interface

### **Top Bar:**
```
🤖 JARVIS | Auto-Login | Movie Search | VLC Play
                                    [⚙️ Settings] [● Ready]
```

### **Left Panel - Quick Actions:**
```
🌐 Web (Auto-Login)
   • Gmail (Login) ✅
   • Facebook (Login) ✅
   • YouTube (Login) ✅
   • Twitter (Login) ✅

🎬 Movies
   • Search Movie ✅
   • Play in VLC ✅

📱 Apps
   • Chrome
   • Word
   • Excel
   • VLC ✅
   • Notepad
   • Calculator

🎵 Media
   • Play Music ✅
   • Pause
   • Next
   • Previous

🔊 System
   • Volume Up/Down
   • Mute

⚡ Power
   • Lock PC
   • Sleep
```

### **Right Panel - Chat:**
```
💬 Chat with JARVIS
   Type or speak your commands
   Real-time responses
   Natural conversation
```

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
- Encrypted (if you enable encryption)
- Never shared or uploaded
- You can delete anytime

---

## 🛠️ Development

### **Project Structure:**
```
Zarves/
├── main.py              # Entry point
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
- **Fixes Guide:** [FIXES.md](FIXES.md)
- **Ollama Docs:** https://ollama.com/docs

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

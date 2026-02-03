# 🤖 JARVIS - Your Personal AI Assistant

> **"Auto-Login | PC Movie Search | VLC Auto-Play"**

Complete AI assistant with **browser auto-login**, **PC movie search**, and **VLC auto-play** support!

---

## ✨ NEW Features

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

## 🚀 Quick Start

### **Super Simple - Just 2 Steps:**
```bash
# Step 1: Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Step 2: Run
python main.py
```

**That's it!** Beautiful GUI opens automatically! 🎉

---

## ⚙️ First Time Setup

### **1. Configure Auto-Login (Optional):**
```
1. Click "⚙️ Settings" button (top-right)
2. Enter Google Email
3. Enter Google Password
4. Click "Save Settings"

Now JARVIS can auto-login to Gmail, YouTube, Facebook!
```

### **2. Add Movie Folders (Optional):**
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
💬 Conversation
┌─────────────────────────────────┐
│ [12:30:45] 👤 You: gmail login │
│ [12:30:47] 🤖 JARVIS: ✅ Logged│
│            into Gmail!          │
│            🌐 Browser opened    │
└─────────────────────────────────┘

[Type message...] [Send] [🎤 Voice]
```

---

## 📦 What's Included

### **Files:**
```
Zarves/
├── main.py              ✅ Single entry point
├── gui/
│   ├── __init__.py
│   └── app.py           ✅ Complete GUI with all features
├── core/                ✅ Core modules
├── skill/               ✅ Skills folder
└── README.md            ✅ This file
```

### **Features:**
- ✅ **Browser Auto-Login** (Gmail, YouTube, Facebook)
- ✅ **PC Movie Search** (All drives, all formats)
- ✅ **VLC Auto-Play** (Finds & plays automatically)
- ✅ **YouTube Auto-Play** (Selenium)
- ✅ Beautiful dark theme GUI
- ✅ Quick action buttons
- ✅ Voice & text input
- ✅ Settings panel
- ✅ Full PC control
- ✅ Auto-install dependencies

---

## 🔧 Requirements

### **Auto-Installed:**
- Python 3.7+
- pyttsx3 (Text-to-speech)
- SpeechRecognition (Voice input)
- pyautogui (System control)
- psutil (Process management)
- selenium (Auto-login & YouTube)
- webdriver-manager (ChromeDriver)

**JARVIS installs everything automatically!**

---

## 💡 Tips

### **1. Auto-Login Setup:**
```
⚙️ Settings → Enter Google credentials → Save
Now: "gmail login karo" works automatically!
```

### **2. Movie Folders:**
```
⚙️ Settings → Add Folder → Select movie folders → Save
JARVIS will search these folders for movies!
```

### **3. Quick Movie Play:**
```
Say: "Avengers movie play karo VLC me"
JARVIS: Searches PC → Finds movie → Opens VLC → Plays!
```

### **4. Voice Commands:**
```
Click Voice button → Speak clearly
"gmail login karo" → Auto-login!
"Avengers movie play karo" → Auto-play!
```

---

## 🎉 Quick Examples

### **Example 1: Auto-Login Gmail**
```
Type: "gmail login karo"
Click: Send

JARVIS:
  ✅ Logged into Gmail!
  🌐 Browser opened with auto-login

[Chrome opens]
[Goes to Gmail]
[Enters email automatically]
[Enters password automatically]
[Clicks login]
[You're logged in!]
```

### **Example 2: Search Movie**
```
Type: "Avengers movie search karo"
Click: Send

JARVIS:
  🎬 Found 3 movie(s):
  
  1. Avengers Endgame.mp4
  2. Avengers Infinity War.mkv
  3. The Avengers.avi
```

### **Example 3: Play Movie in VLC**
```
Type: "Avengers movie play karo VLC me"
Click: Send

JARVIS:
  🎬 Playing in VLC:
  Avengers Endgame.mp4
  ✅ Movie started!

[VLC opens automatically]
[Movie starts playing]
```

### **Example 4: Voice Command**
```
Click: Voice button
Say: "Interstellar movie play karo VLC me"

JARVIS:
  🎬 Playing in VLC:
  Interstellar.mkv
  ✅ Movie started!

[Searches PC]
[Finds Interstellar]
[Opens VLC]
[Plays automatically!]
```

---

## 🎬 Movie Search Demo

```
User: "Avengers movie search karo"

JARVIS: 
  🎬 Found 3 movie(s):
  
  1. Avengers Endgame.mp4
  2. Avengers Infinity War.mkv
  3. The Avengers.avi

User: "play karo VLC me"

JARVIS:
  🎬 Playing in VLC:
  Avengers Endgame.mp4
  ✅ Movie started!

[VLC opens and plays first movie automatically!]
```

---

## 🔐 Auto-Login Demo

```
User: "gmail login karo"

JARVIS:
  ✅ Logged into Gmail!
  🌐 Browser opened with auto-login

[Chrome opens]
[Gmail page loads]
[Email field fills automatically]
[Password field fills automatically]
[Login button clicks automatically]
[Gmail inbox opens - logged in!]
```

---

## 🐛 Troubleshooting

### **Problem: Auto-login not working**
**Solution:**
```
1. Click ⚙️ Settings
2. Enter correct Google email & password
3. Click Save Settings
4. Try again: "gmail login karo"
```

### **Problem: Movie not found**
**Solution:**
```
1. Click ⚙️ Settings
2. Click "Add Folder"
3. Select folder containing movies
4. Click Save Settings
5. Try again: "movie search karo"
```

### **Problem: VLC not opening**
**Solution:**
```
1. Install VLC Media Player
2. Windows: Download from videolan.org
3. Try again: "movie play karo VLC me"
```

### **Problem: Selenium not working**
**Solution:**
```
# Auto-installs, but if fails:
pip install selenium webdriver-manager

# Then run:
python main.py
```

---

## 📊 Performance

- **Startup Time:** ~2 seconds
- **Auto-Login:** ~5-8 seconds
- **Movie Search:** ~2-5 seconds (depends on PC)
- **VLC Auto-Play:** ~3 seconds
- **YouTube Auto-Play:** ~3-5 seconds
- **Memory Usage:** ~100MB (with Selenium)
- **CPU Usage:** <5% idle

---

## 🎯 Supported Formats

### **Video Formats:**
```
✅ MP4 (MPEG-4)
✅ MKV (Matroska)
✅ AVI (Audio Video Interleave)
✅ MOV (QuickTime)
✅ WMV (Windows Media Video)
✅ FLV (Flash Video)
✅ WEBM (WebM)
```

### **Websites (Auto-Login):**
```
✅ Gmail
✅ YouTube
✅ Facebook
✅ Twitter
```

---

## 🚀 Get Started Now!

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
python main.py
```

**Beautiful GUI opens automatically!** 🎉

### **Then:**

**1. Setup (First Time):**
```
Click: ⚙️ Settings
Enter: Google email & password
Add: Movie folders
Click: Save Settings
```

**2. Use Commands:**
```
"gmail login karo" → Auto-login!
"Avengers movie search karo" → Search PC!
"movie play karo VLC me" → Auto-play!
```

**3. Enjoy!** 🎬

---

## 🔥 Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| **Browser Auto-Login** | ✅ Working | Opens & logs in automatically |
| **PC Movie Search** | ✅ Working | Searches entire PC storage |
| **VLC Auto-Play** | ✅ Working | Finds & plays in VLC |
| **YouTube Auto-Play** | ✅ Working | Opens & plays songs |
| **Settings Panel** | ✅ Working | Configure credentials & paths |
| **Voice Commands** | ✅ Working | Speak naturally |
| **Quick Actions** | ✅ Working | One-click buttons |
| **Beautiful GUI** | ✅ Working | Dark theme interface |
| **Auto-Install** | ✅ Working | Dependencies install automatically |

---

**Made with ❤️ in India**

**JARVIS - Auto-Login | Movie Search | VLC Play!**

---

## 💬 Example Conversations

### **Conversation 1: Auto-Login**
```
You: "gmail login karo"
JARVIS: ✅ Logged into Gmail! 🌐 Browser opened with auto-login

You: "youtube login karo"
JARVIS: ✅ Logged into YouTube! 🌐 Browser opened with auto-login
```

### **Conversation 2: Movie Search & Play**
```
You: "Avengers movie search karo"
JARVIS: 🎬 Found 3 movie(s):
        1. Avengers Endgame.mp4
        2. Avengers Infinity War.mkv
        3. The Avengers.avi

You: "play karo VLC me"
JARVIS: 🎬 Playing in VLC: Avengers Endgame.mp4
        ✅ Movie started!
```

### **Conversation 3: Direct Play**
```
You: "Interstellar movie play karo VLC me"
JARVIS: 🎬 Playing in VLC: Interstellar.mkv
        ✅ Movie started!
```

---

**Perfect! Ab browser auto-login, PC movie search, aur VLC auto-play - sab automatic!** 🎬

**Just one command - python main.py - that's it!** 🚀

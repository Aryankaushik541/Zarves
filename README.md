# 🤖 JARVIS - Your Personal AI Assistant

> **"YouTube Auto-Play - Opens & Plays Automatically!"**

Complete AI assistant with stunning visual interface, full PC control, and **YouTube auto-play** support.

---

## ✨ Features

### 🎨 **Beautiful GUI Interface**
```
🖥️  Modern dark theme
⚡ Quick action buttons
💬 Chat interface
🎤 Voice & text input
🟢 Real-time status
```

### 🎵 **YouTube Auto-Play (NEW!)**
```
✅ Opens YouTube automatically
✅ Searches for song
✅ Clicks first video
✅ Starts playing automatically!

Example:
Say: "honey singh ka gaana bajao"
Result: YouTube opens and plays Honey Singh song!
```

### 🌐 **Web Support**
```
✅ Gmail - Opens directly
✅ Facebook - One click
✅ YouTube - Instant access
✅ Twitter, Instagram, LinkedIn
✅ WhatsApp Web
✅ Any website!
```

### 💻 **Full PC Control**
```
✅ 50+ Apps (Chrome, Word, Excel, VLC, etc.)
✅ Volume & Brightness control
✅ Power management (Lock, Sleep, Shutdown)
✅ Media controls (Play, Pause, Next)
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

**That's it!** Beautiful GUI window opens automatically! 🎉

**Dependencies install automatically!** (Including Selenium for auto-play)

---

## 🎵 YouTube Auto-Play Examples

### **Example 1: Honey Singh**
```
Command: "honey singh ka gaana bajao"
Result: 
  1. YouTube opens
  2. Searches "honey singh"
  3. Clicks first video
  4. Starts playing automatically!
```

### **Example 2: Specific Song**
```
Command: "Kesariya bajao"
Result: 
  1. YouTube opens
  2. Searches "Kesariya"
  3. Clicks first video
  4. Plays automatically!
```

### **Example 3: Any Artist**
```
Command: "arijit singh ka gaana bajao"
Result: 
  1. YouTube opens
  2. Searches "arijit singh"
  3. Clicks first video
  4. Auto-plays!
```

### **Example 4: Just "Play Music"**
```
Command: "gaana bajao"
Result: 
  1. YouTube opens
  2. Plays trending song
  3. Automatic playback!
```

---

## 💬 Commands

### **YouTube Auto-Play:**
```
"honey singh ka gaana bajao" → Auto-plays Honey Singh
"Kesariya bajao" → Auto-plays Kesariya
"arijit singh ka gaana bajao" → Auto-plays Arijit Singh
"gaana bajao" → Auto-plays trending song
"diljit dosanjh ka song play karo" → Auto-plays Diljit
```

### **Web (Direct Access):**
```
"gmail kholo" → Opens Gmail
"facebook kholo" → Opens Facebook
"youtube kholo" → Opens YouTube
"twitter kholo" → Opens Twitter
"instagram kholo" → Opens Instagram
"whatsapp web kholo" → Opens WhatsApp Web
```

### **Applications:**
```
"chrome kholo" → Opens Chrome
"word kholo" → Opens Word
"excel kholo" → Opens Excel
"calculator kholo" → Opens Calculator
```

### **Media Controls:**
```
"pause karo" → Pauses media
"next" → Next track
"previous" → Previous track
```

### **System Control:**
```
"volume badhao" → Increases volume
"volume kam karo" → Decreases volume
"mute karo" → Mutes audio
"brightness badhao" → Increases brightness
```

### **Power Management:**
```
"lock karo" → Locks PC
"sleep karo" → Sleep mode
"restart karo" → Restarts PC
"shutdown karo" → Shuts down PC
```

### **Google Search:**
```
"google pe python search karo" → Searches Google
```

---

## 🎯 How YouTube Auto-Play Works

### **Technology:**
- **Selenium WebDriver** - Browser automation
- **ChromeDriver** - Chrome control
- **Auto-install** - Sets up automatically

### **Process:**
1. You say: "honey singh ka gaana bajao"
2. JARVIS extracts: "honey singh"
3. Opens Chrome with Selenium
4. Goes to YouTube
5. Searches for "honey singh"
6. Finds first video
7. Clicks it automatically
8. Video starts playing!

### **Fallback:**
- If Selenium fails, opens YouTube search
- You can click first video manually
- Still faster than manual search!

---

## 🎨 GUI Interface

### **Left Panel - Quick Actions:**
```
🌐 Web
   • Chrome
   • Gmail ✅
   • Facebook ✅
   • YouTube ✅
   • Twitter
   • Instagram
   • WhatsApp Web
   • LinkedIn

📱 Apps
   • Word
   • Excel
   • PowerPoint
   • Notepad
   • Calculator
   • Paint
   • VLC

🎵 Media
   • Play Music ✅ (Auto-play!)
   • Pause
   • Next
   • Previous

🔊 System
   • Volume Up/Down
   • Mute
   • Brightness Up/Down

⚡ Power
   • Lock PC
   • Sleep
   • Restart
   • Shutdown
```

---

## 📦 What's Included

### **Files:**
```
Zarves/
├── main.py              ✅ Single entry point (auto-installs Selenium)
├── gui/
│   ├── __init__.py
│   └── app.py           ✅ Complete GUI with YouTube auto-play
├── core/                ✅ Core modules
├── skill/               ✅ Skills folder
└── README.md            ✅ This file
```

### **Features:**
- ✅ Beautiful dark theme GUI
- ✅ Quick action buttons
- ✅ Voice & text input
- ✅ Web support (Gmail, Facebook, etc.)
- ✅ **YouTube Auto-Play (Selenium)**
- ✅ Full PC control
- ✅ Auto-install dependencies
- ✅ Real-time status
- ✅ Color-coded chat
- ✅ Single entry point (main.py)

---

## 🔧 Requirements

### **Auto-Installed:**
- Python 3.7+
- pyttsx3 (Text-to-speech)
- SpeechRecognition (Voice input)
- pyautogui (System control)
- psutil (Process management)
- **selenium (YouTube auto-play)**
- **webdriver-manager (ChromeDriver)**

**JARVIS installs everything automatically when you run main.py!**

---

## 💡 Tips

### **1. YouTube Auto-Play:**
- Say artist name: "honey singh ka gaana bajao"
- Say song name: "Kesariya bajao"
- Just say: "gaana bajao" for trending
- Works with any artist/song!

### **2. Quick Actions:**
- Use left panel buttons for instant access
- No typing needed!
- One click = instant action

### **3. Web Access:**
- Gmail, Facebook, YouTube - direct buttons
- No need to type URLs
- Instant access to favorite sites

### **4. Voice Commands:**
- Click Voice button
- Speak clearly
- JARVIS responds with voice

### **5. Natural Language:**
```
✅ "honey singh ka gaana bajao"
✅ "gmail kholo"
✅ "facebook kholo"
✅ "volume badhao"
```

---

## 🐛 Troubleshooting

### **Problem: YouTube doesn't auto-play**
**Solution:**
- Selenium installs automatically
- If fails, opens YouTube search
- Click first video manually
- Check Chrome is installed

### **Problem: GUI doesn't open**
**Solution:**
```bash
# Install tkinter (usually pre-installed)
# On Ubuntu/Debian:
sudo apt-get install python3-tk

# Then run:
python main.py
```

### **Problem: Voice not working**
**Solution:**
- Check microphone permissions
- Reduce background noise
- Click Voice button and speak clearly

### **Problem: Websites don't open**
**Solution:**
- Check internet connection
- Default browser will be used
- Try clicking button again

---

## 📊 Performance

- **Startup Time:** ~2 seconds
- **GUI Response:** Instant
- **YouTube Auto-Play:** ~3-5 seconds
- **Memory Usage:** ~80MB (with Selenium)
- **CPU Usage:** <5% idle

---

## 🎉 Quick Examples

### **Example 1: Auto-Play Honey Singh**
```
Type: "honey singh ka gaana bajao"
Click: Send
Result: 
  ✅ YouTube opens
  ✅ Searches "honey singh"
  ✅ Clicks first video
  ✅ Starts playing automatically!
```

### **Example 2: Open Gmail**
```
Click: Gmail button (left panel)
Result: Gmail opens in browser
```

### **Example 3: Control Volume**
```
Click: Volume Up button
Result: System volume increases
```

### **Example 4: Voice Command**
```
Click: Voice button
Say: "arijit singh ka gaana bajao"
Result: 
  ✅ YouTube opens
  ✅ Plays Arijit Singh song
  ✅ Automatic playback!
```

---

## 🎵 YouTube Auto-Play Demo

```
User: "honey singh ka gaana bajao"

JARVIS: 
  🎵 Playing: honey singh
  ✅ YouTube opened and playing!

[Chrome opens automatically]
[Searches "honey singh"]
[Clicks first video]
[Video starts playing!]
```

---

**Made with ❤️ in India**

**JARVIS - YouTube Auto-Play, Full Control!**

---

## 🚀 Get Started Now!

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
python main.py
```

**Beautiful GUI opens automatically!** 🎉

**Say: "honey singh ka gaana bajao"** 🎵

**YouTube opens and plays automatically!** ✨

**Just one command - python main.py - that's it!** 🚀

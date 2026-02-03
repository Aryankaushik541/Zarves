# 🤖 JARVIS - Your Personal AI Assistant

> **"Beautiful GUI - Just Run main.py!"**

Complete AI assistant with stunning visual interface, full PC control, and web support.

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

### 🎵 **YouTube Auto-Play**
```
Say: "gaana bajao"
Result: YouTube opens and plays!
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
   • Play Music
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

### **Right Panel - Chat & Controls:**
```
💬 Conversation Display
   • Color-coded messages
   • Timestamps
   • Scrollable history

⌨️  Input Area
   • Text input field
   • Send button
   • Voice button

🟢 Status Indicator
   • Ready (Green)
   • Listening (Blue)
   • Processing (Orange)
   • Error (Red)
```

---

## 💬 Commands

### **Web (Direct Access):**
```
"gmail kholo" → Opens Gmail
"facebook kholo" → Opens Facebook
"youtube kholo" → Opens YouTube
"twitter kholo" → Opens Twitter
"instagram kholo" → Opens Instagram
"whatsapp web kholo" → Opens WhatsApp Web
```

### **Music & YouTube:**
```
"gaana bajao" → Plays trending song
"Kesariya bajao" → Plays specific song
"pause karo" → Pauses media
"next" → Next track
```

### **Applications:**
```
"chrome kholo" → Opens Chrome
"word kholo" → Opens Word
"excel kholo" → Opens Excel
"calculator kholo" → Opens Calculator
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

## 🎯 How to Use

### **1. Click Quick Action Buttons:**
- Click any button in left panel
- Action executes immediately
- Response shows in chat

### **2. Type Commands:**
- Type in input field
- Press Enter or click Send
- JARVIS responds with voice

### **3. Use Voice Input:**
- Click "🎤 Voice" button
- Speak your command
- JARVIS executes and responds

---

## 📦 What's Included

### **Files:**
```
Zarves/
├── main.py              ✅ Single entry point (auto-launches GUI)
├── gui/
│   ├── __init__.py
│   └── app.py           ✅ Complete GUI interface
├── core/                ✅ Core modules
├── skill/               ✅ Skills folder
└── README.md            ✅ This file
```

### **Features:**
- ✅ Beautiful dark theme GUI
- ✅ Quick action buttons
- ✅ Voice & text input
- ✅ Web support (Gmail, Facebook, etc.)
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

**JARVIS installs everything automatically when you run main.py!**

---

## 💡 Tips

### **1. Quick Actions:**
- Use left panel buttons for instant access
- No typing needed!
- One click = instant action

### **2. Web Access:**
- Gmail, Facebook, YouTube - direct buttons
- No need to type URLs
- Instant access to favorite sites

### **3. Voice Commands:**
- Click Voice button
- Speak clearly
- JARVIS responds with voice

### **4. Natural Language:**
```
✅ "gmail kholo"
✅ "facebook kholo"
✅ "gaana bajao"
✅ "volume badhao"
```

---

## 🐛 Troubleshooting

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
- **Memory Usage:** ~60MB
- **CPU Usage:** <5% idle

---

## 🎨 Screenshots

### **Main Interface:**
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 JARVIS                              ● Ready             │
│  Your Personal AI Assistant                                 │
├──────────────┬──────────────────────────────────────────────┤
│              │  💬 Conversation                             │
│  ⚡ Quick    │  ┌────────────────────────────────────────┐ │
│  Actions     │  │ [12:30:45] 🤖 JARVIS: Hello!          │ │
│              │  │ [12:30:50] 👤 You: gmail kholo        │ │
│  🌐 Web      │  │ [12:30:51] 🤖 JARVIS: Opening Gmail...│ │
│  • Chrome    │  └────────────────────────────────────────┘ │
│  • Gmail     │                                              │
│  • Facebook  │  ┌────────────────────────────────────────┐ │
│  • YouTube   │  │ Type here...          [Send] [Voice]   │ │
│              │  └────────────────────────────────────────┘ │
│  📱 Apps     │                                              │
│  • Word      │                                              │
│  • Excel     │                                              │
│              │                                              │
│  🎵 Media    │                                              │
│  🔊 System   │                                              │
│  ⚡ Power    │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Want to add features?

1. Fork repository
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## 📄 License

MIT License - Free to use and modify

---

## 👨‍💻 Author

**Aryan Kaushik**
- GitHub: [@Aryankaushik541](https://github.com/Aryankaushik541)

---

## ⭐ Support

If you like JARVIS:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code

---

## 🎉 Quick Examples

### **Example 1: Open Gmail**
```
Click: Gmail button (left panel)
Result: Gmail opens in browser
```

### **Example 2: Play Music**
```
Type: "gaana bajao"
Click: Send
Result: YouTube opens and plays music
```

### **Example 3: Control Volume**
```
Click: Volume Up button
Result: System volume increases
```

### **Example 4: Voice Command**
```
Click: Voice button
Say: "chrome kholo"
Result: Chrome opens
```

---

**Made with ❤️ in India**

**JARVIS - Beautiful GUI, Full Control!**

---

## 🚀 Get Started Now!

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
python main.py
```

**Beautiful GUI opens automatically!** 🎉

**Just one command - python main.py - that's it!** ✨

# 🎨 JARVIS Modern GUI - Enhanced AI Agent

## 🚀 Quick Start

### Option 1: Modern GUI (Recommended)
```bash
python launch_modern.py
```

### Option 2: Original GUI
```bash
python main.py
```

---

## ✨ What's New in Modern GUI?

### 🎯 **Enhanced Features**

1. **🧵 Threaded Processing**
   - No GUI freezing during AI processing
   - Background command execution
   - Real-time status updates

2. **🎨 Modern Dark Theme**
   - Professional dark interface
   - Smooth animations
   - Better readability

3. **🧠 Smart Intent Detection**
   - Automatic command understanding
   - Multi-language support (Hindi + English)
   - Context-aware responses

4. **💬 Conversation Memory**
   - Remembers previous conversations
   - Context-aware responses
   - Better follow-up handling

5. **📊 Live Statistics**
   - Real-time stats display
   - Query tracking
   - Success rate monitoring

6. **⚡ Quick Actions**
   - One-click shortcuts
   - Frequently used commands
   - Customizable actions

---

## 🎨 GUI Features

### **Main Interface**

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

### **Key Components**

1. **Header Bar**
   - Title and branding
   - Real-time status indicator
   - Color-coded status (Green=Ready, Orange=Processing, Red=Error)

2. **Conversation Panel**
   - Scrollable chat history
   - Timestamped messages
   - Color-coded message types
   - Clear chat button

3. **Statistics Panel**
   - Skills loaded count
   - Tools available count
   - Queries processed
   - Success rate percentage

4. **Quick Actions Panel**
   - YouTube shortcut
   - Browser shortcut
   - Movies shortcut
   - Search shortcut
   - Settings access

5. **Input Area**
   - Text input field
   - Send button
   - Voice input button
   - Keyboard shortcuts (Enter to send)

---

## 🧠 Enhanced AI Agent

### **Smart Intent Detection**

The enhanced AI agent automatically detects user intent from natural language:

#### **Supported Intents**

| Intent | Hindi Examples | English Examples |
|--------|---------------|------------------|
| **YouTube** | "youtube खोल", "गाना चला" | "open youtube", "play song" |
| **Browser** | "browser खोल", "internet खोल" | "open browser", "open chrome" |
| **Movie** | "movie चला", "फिल्म देख" | "play movie", "watch film" |
| **Search** | "google पर खोज", "क्या है" | "search google", "what is" |
| **System** | "computer बंद कर", "volume बढ़ा" | "shutdown", "volume up" |
| **File** | "file खोल", "folder बना" | "open file", "create folder" |
| **Time** | "समय बता", "date क्या है" | "what time", "tell date" |
| **Weather** | "मौसम कैसा है" | "how's the weather" |
| **Email** | "email भेज" | "send email" |
| **Screenshot** | "screenshot ले" | "take screenshot" |

### **Context Awareness**

The agent maintains conversation context:

```python
User: "youtube खोल"
JARVIS: "Opening YouTube! 🎵"

User: "wahan pe gaana search kar"  # Refers to YouTube
JARVIS: "Searching for song on YouTube..."
```

### **Entity Extraction**

Automatically extracts relevant information:

```python
"play despacito on youtube"
→ Intent: youtube
→ Entity: {query: "despacito"}

"search for python tutorials"
→ Intent: search
→ Entity: {query: "python tutorials"}
```

---

## 🎯 Usage Examples

### **Voice Commands**

1. **YouTube**
   ```
   "youtube kholo"
   "gaana sunao"
   "play despacito"
   ```

2. **Browser**
   ```
   "browser kholo"
   "chrome open karo"
   "internet kholo"
   ```

3. **Movies**
   ```
   "movie chalao"
   "inception play karo"
   "film dekho"
   ```

4. **Search**
   ```
   "google par search karo"
   "what is AI"
   "python kya hai"
   ```

5. **System**
   ```
   "volume badhao"
   "computer band karo"
   "restart karo"
   ```

### **Text Commands**

Simply type in the input field:
- `open youtube`
- `play song`
- `search python`
- `what time is it`
- `take screenshot`

---

## ⚙️ Configuration

### **Settings Dialog**

Access via Quick Actions → Settings

**Available Options:**
- ✅ Enable/Disable voice responses
- 🎨 Theme selection (coming soon)
- 🌐 Language preference (coming soon)
- 🔊 Voice settings (coming soon)

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

## 🔧 Technical Details

### **Architecture**

```
┌─────────────────────────────────────────────┐
│           Modern GUI (Tkinter)              │
│  ┌───────────────────────────────────────┐  │
│  │  Command Queue (Thread-Safe)          │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │  Enhanced AI Agent                    │  │
│  │  - Intent Detection                   │  │
│  │  - Entity Extraction                  │  │
│  │  - Context Management                 │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │  JARVIS Engine                        │  │
│  │  - Skill Registry                     │  │
│  │  - Tool Execution                     │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │  Skills (21 skills, 69 tools)         │  │
│  │  - YouTube, Browser, Movies, etc.     │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### **Threading Model**

1. **Main Thread**: GUI rendering and user interaction
2. **Command Processor Thread**: Background command processing
3. **Voice Thread**: Voice recognition (when active)
4. **TTS Thread**: Text-to-speech output

### **Performance**

- ⚡ **Non-blocking UI**: GUI never freezes
- 🚀 **Fast response**: < 1s for simple commands
- 💾 **Memory efficient**: Conversation history limited to 20 exchanges
- 🔄 **Concurrent processing**: Multiple threads for smooth operation

---

## 🐛 Troubleshooting

### **GUI doesn't open**
```bash
# Check tkinter installation
python -c "import tkinter"

# Linux: Install tkinter
sudo apt-get install python3-tk

# macOS: Should be pre-installed
# Windows: Should be pre-installed
```

### **Voice not working**
```bash
# Install dependencies
pip install SpeechRecognition pyaudio pyttsx3

# Linux: Install portaudio
sudo apt-get install portaudio19-dev

# macOS: Install portaudio
brew install portaudio
```

### **Ollama connection error**
```bash
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags

# Pull model if needed
ollama pull llama3.2
```

### **Skills not loading**
```bash
# Check skill directory
ls -la skill/

# Verify Python path
python -c "import sys; print(sys.path)"

# Run with debug
python launch_modern.py --debug
```

---

## 📚 API Reference

### **EnhancedAIAgent**

```python
from core.enhanced_agent import EnhancedAIAgent

# Initialize
agent = EnhancedAIAgent(engine)

# Process query
response = agent.process_query("open youtube")

# Detect intent
intent, confidence = agent.detect_intent("play song")

# Extract entities
entities = agent.extract_entities("play despacito", "youtube")

# Get stats
stats = agent.get_stats()

# Clear history
agent.clear_history()
```

### **ModernJarvisGUI**

```python
from gui.modern_app import ModernJarvisGUI
import tkinter as tk

# Create GUI
root = tk.Tk()
app = ModernJarvisGUI(root)

# Add message
app.add_message("JARVIS", "Hello!", "jarvis")

# Update status
app.update_status("Ready", "#00ff88")

# Run
root.mainloop()
```

---

## 🎓 Development

### **Adding New Intents**

Edit `core/enhanced_agent.py`:

```python
self.intent_patterns = {
    # ... existing intents ...
    'custom': [
        r'(custom|कस्टम).*(pattern|पैटर्न)',
    ],
}

def _execute_custom(self, query: str, entities: Dict) -> str:
    """Execute custom action"""
    # Your implementation
    return "Custom action executed!"
```

### **Adding Quick Actions**

Edit `gui/modern_app.py`:

```python
actions = [
    # ... existing actions ...
    ("🎯 Custom", self._quick_custom),
]

def _quick_custom(self):
    self.command_queue.put("custom command")
```

### **Customizing Theme**

Edit colors in `gui/modern_app.py`:

```python
# Background colors
bg_primary = '#0a0a0a'
bg_secondary = '#1a1a1a'
bg_tertiary = '#2a2a2a'

# Text colors
text_primary = '#ffffff'
text_secondary = '#888888'

# Accent colors
accent_green = '#00ff88'
accent_blue = '#4488ff'
accent_orange = '#ff8800'
accent_red = '#ff4444'
```

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

This project is part of JARVIS - Personal AI Assistant

---

## 🙏 Credits

- **Original JARVIS**: Base framework and skills
- **Modern GUI**: Enhanced interface and AI agent
- **Ollama**: Local AI processing
- **Python Community**: Amazing libraries

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Aryankaushik541/Zarves/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aryankaushik541/Zarves/discussions)
- **Email**: [Your Email]

---

**Made with ❤️ for the AI community**

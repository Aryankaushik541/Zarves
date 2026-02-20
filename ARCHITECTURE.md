# 🏗️ ZARVES - System Architecture

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ZARVES AI AGENT                      │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Voice Engine │    │  Offline AI  │    │   Browser    │
│              │    │    Brain     │    │  Controller  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Microphone  │    │  Knowledge   │    │   Chrome/    │
│   Speaker    │    │     Base     │    │   Firefox    │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 🔄 Data Flow

```
User Voice Input
      │
      ▼
┌─────────────────┐
│ Speech          │
│ Recognition     │ (Google Speech API)
└─────────────────┘
      │
      ▼ (Text)
┌─────────────────┐
│ AI Processing   │
│ - Pattern Match │
│ - Context Check │
│ - Learning      │
└─────────────────┘
      │
      ▼ (Action)
┌─────────────────┐
│ Action          │
│ Execution       │
│ - Browser       │
│ - System        │
│ - Response      │
└─────────────────┘
      │
      ▼ (Response)
┌─────────────────┐
│ Text-to-Speech  │
│ Output          │
└─────────────────┘
      │
      ▼
User Audio Output
```

---

## 🧩 Component Details

### 1. Voice Engine (`VoiceEngine`)

```python
┌─────────────────────────────────────┐
│         Voice Engine                │
├─────────────────────────────────────┤
│ • Speech Recognition                │
│   - Microphone input                │
│   - Google Speech API               │
│   - Hindi + English support         │
│                                     │
│ • Text-to-Speech                    │
│   - pyttsx3 engine                  │
│   - Voice customization             │
│   - Multi-language output           │
└─────────────────────────────────────┘
```

**Key Methods:**
- `listen()` - Capture voice input
- `speak(text)` - Convert text to speech
- `_setup_voice()` - Configure voice properties

---

### 2. Offline AI Brain (`OfflineAI` / `EnhancedAI`)

```python
┌─────────────────────────────────────┐
│         Offline AI Brain            │
├─────────────────────────────────────┤
│ • Knowledge Base                    │
│   - Command patterns                │
│   - Website mappings                │
│   - Action definitions              │
│                                     │
│ • Pattern Matching                  │
│   - Direct match                    │
│   - Fuzzy match                     │
│   - Smart inference                 │
│                                     │
│ • Learning System                   │
│   - Command history                 │
│   - Frequency tracking              │
│   - Pattern learning                │
│                                     │
│ • Context Management (Pro)          │
│   - Conversation flow               │
│   - Follow-up commands              │
│   - Smart suggestions               │
└─────────────────────────────────────┘
```

**Key Methods:**
- `understand(text)` - Process command
- `respond(action)` - Generate response
- `_learn(text)` - Learn from interaction
- `_smart_match(text)` - Pattern matching

---

### 3. Browser Controller (`BrowserController`)

```python
┌─────────────────────────────────────┐
│       Browser Controller            │
├─────────────────────────────────────┤
│ • Selenium WebDriver                │
│   - Chrome automation               │
│   - Auto driver management          │
│   - Window control                  │
│                                     │
│ • Navigation                        │
│   - URL opening                     │
│   - Search execution                │
│   - Back/Forward/Refresh            │
│                                     │
│ • Page Interaction                  │
│   - Element clicking                │
│   - Text input                      │
│   - Scrolling                       │
│   - Screenshots                     │
└─────────────────────────────────────┘
```

**Key Methods:**
- `open_browser(url)` - Open website
- `search(query, engine)` - Search
- `close()` - Close browser

---

### 4. System Controller (`SystemController`)

```python
┌─────────────────────────────────────┐
│       System Controller             │
├─────────────────────────────────────┤
│ • Power Management                  │
│   - Shutdown                        │
│   - Restart                         │
│   - Sleep                           │
│                                     │
│ • System Information                │
│   - CPU usage                       │
│   - Memory usage                    │
│   - Time/Date                       │
└─────────────────────────────────────┘
```

**Key Methods:**
- `shutdown()` - Shutdown system
- `restart()` - Restart system
- `sleep()` - Sleep mode
- `get_system_info()` - System stats

---

## 🔀 Command Processing Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Voice Input: "Zarves open Google"                   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Speech Recognition                                   │
│    Input: Audio                                         │
│    Output: "zarves open google" (text)                  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 3. AI Processing                                        │
│    • Normalize: "zarves open google"                    │
│    • Pattern Match: "open google"                       │
│    • Knowledge Base Lookup                              │
│    • Action: {"action": "open_browser",                 │
│               "url": "https://www.google.com"}          │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Action Execution                                     │
│    • Initialize browser (if needed)                     │
│    • Navigate to URL                                    │
│    • Wait for page load                                 │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Response Generation                                  │
│    • Text: "Browser khol raha hoon"                     │
│    • TTS: Audio output                                  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Learning                                             │
│    • Save to history                                    │
│    • Update patterns                                    │
│    • Improve accuracy                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ File Structure

```
Zarves/
│
├── 🚀 Main Entry Points
│   ├── zarves_advanced.py      # Basic AI agent
│   ├── zarves_pro.py           # Enhanced AI agent
│   └── main.py                 # Original entry
│
├── 🧠 Core AI Modules
│   └── core/
│       ├── engine.py           # AI engine
│       ├── voice.py            # Voice processing
│       ├── autonomous_coder.py # Self-coding
│       └── ...
│
├── 🛠️ Skills/Capabilities
│   └── skill/
│       ├── smart_browser_control.py  # Browser automation
│       ├── web_ops.py                # Web operations
│       ├── system_ops.py             # System control
│       └── ...
│
├── 🎨 GUI Components
│   └── gui/
│       └── ...
│
├── 📚 Documentation
│   ├── README.md               # Main documentation
│   ├── QUICK_START.md          # Quick start (Hindi)
│   ├── FEATURES.md             # Features list
│   ├── ARCHITECTURE.md         # This file
│   └── RUN_ME_FIRST.md         # First-time guide
│
├── 🔧 Configuration
│   ├── requirements.txt        # Dependencies
│   ├── .env.template           # Environment template
│   └── .gitignore              # Git ignore
│
└── 📦 Installation
    ├── install.bat             # Windows installer
    └── install.sh              # Linux/Mac installer
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│         User's Computer             │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │   Zarves AI Agent             │ │
│  │   (Runs Locally)              │ │
│  └───────────────────────────────┘ │
│              │                      │
│              ▼                      │
│  ┌───────────────────────────────┐ │
│  │   Local AI Processing         │ │
│  │   • No cloud API              │ │
│  │   • No data upload            │ │
│  │   • Offline capable           │ │
│  └───────────────────────────────┘ │
│              │                      │
│              ▼                      │
│  ┌───────────────────────────────┐ │
│  │   Local Storage               │ │
│  │   • Command history           │ │
│  │   • Learning data             │ │
│  │   • User preferences          │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
         │
         ▼ (Only for web browsing)
┌─────────────────────────────────────┐
│         Internet                    │
│   (Only when opening websites)      │
└─────────────────────────────────────┘
```

**Security Features:**
- ✅ All processing local
- ✅ No cloud dependencies
- ✅ No data transmission
- ✅ Open source code
- ✅ User control

---

## 🔄 State Management

```python
┌─────────────────────────────────────┐
│         Agent State                 │
├─────────────────────────────────────┤
│ • running: bool                     │
│ • browser_open: bool                │
│ • current_url: str                  │
│ • last_action: dict                 │
│ • conversation_history: list        │
│ • command_history: list             │
│ • session_start: datetime           │
│ • commands_executed: int            │
│ • errors_count: int                 │
└─────────────────────────────────────┘
```

---

## 🧪 Testing Flow

```
┌─────────────────────────────────────┐
│ 1. Unit Tests                       │
│    • Voice engine                   │
│    • AI processing                  │
│    • Browser control                │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 2. Integration Tests                │
│    • Voice → AI → Action            │
│    • End-to-end flow                │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 3. User Acceptance Testing          │
│    • Real voice commands            │
│    • Real browser actions           │
│    • Real user scenarios            │
└─────────────────────────────────────┘
```

---

## 📊 Performance Optimization

### 1. Voice Recognition
```python
• Ambient noise adjustment
• Timeout optimization
• Language detection
• Parallel processing
```

### 2. AI Processing
```python
• Pattern caching
• Quick lookup tables
• Lazy loading
• Memory optimization
```

### 3. Browser Control
```python
• WebDriver reuse
• Page load optimization
• Element caching
• Smart waiting
```

---

## 🔮 Future Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  ZARVES v3.0 (Future)                   │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Advanced   │    │  Local LLM   │    │  Multi-App   │
│    Voice     │    │  (Ollama)    │    │   Control    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Continuous  │    │  Advanced    │    │  WhatsApp    │
│  Listening   │    │  Reasoning   │    │  Email       │
│              │    │              │    │  Calendar    │
└──────────────┘    └──────────────┘    └──────────────┘
```

**Planned Features:**
- Local LLM integration (Ollama)
- Continuous listening mode
- Multi-app automation
- Advanced reasoning
- Plugin system
- Mobile app
- Cloud sync (optional)

---

## 🛠️ Technology Stack

### Core Technologies
```
┌─────────────────────────────────────┐
│ Python 3.7+                         │
├─────────────────────────────────────┤
│ • SpeechRecognition                 │
│ • pyttsx3                           │
│ • Selenium                          │
│ • psutil                            │
│ • pyautogui                         │
└─────────────────────────────────────┘
```

### Optional Technologies
```
┌─────────────────────────────────────┐
│ Advanced Features                   │
├─────────────────────────────────────┤
│ • Ollama (Local LLM)                │
│ • OpenCV (Computer Vision)          │
│ • PyQt5 (GUI)                       │
└─────────────────────────────────────┘
```

---

## 📈 Scalability

### Current Capacity
- Commands/minute: 10-20
- Concurrent browsers: 1
- Memory usage: 100-200 MB
- CPU usage: 5-40%

### Optimization Strategies
1. Command caching
2. Browser pooling
3. Lazy initialization
4. Resource cleanup
5. Memory management

---

**Architecture designed for:**
- ✅ Simplicity
- ✅ Performance
- ✅ Privacy
- ✅ Extensibility
- ✅ Reliability

**Made with ❤️ for developers**

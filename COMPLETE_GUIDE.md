# 🎯 JARVIS - Complete Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Autonomous AI Coder](#autonomous-ai-coder)
4. [Modern GUI](#modern-gui)
5. [Classic GUI](#classic-gui)
6. [Voice Commands](#voice-commands)
7. [Skills & Tools](#skills--tools)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**JARVIS** ek complete AI assistant hai with **3 powerful modes**:

### **1. 🤖 Autonomous AI Coder**
- Full-stack projects generate karta hai
- Internet se research karta hai
- Khud errors debug karta hai
- Terminal commands execute karta hai

### **2. 🎨 Modern GUI**
- Beautiful dark theme
- Threaded processing (no freezing)
- Smart intent detection
- Conversation memory

### **3. 📺 Classic GUI**
- All-in-one file
- Auto-setup everything
- Simple and fast
- Voice + text control

---

## 🚀 Quick Start

### **Installation**

```bash
# 1. Clone repository
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Install dependencies (optional - auto-installed)
pip install -r requirements.txt

# 3. Start Ollama (if not running)
ollama serve
```

### **Choose Your Mode**

```bash
# Mode 1: Autonomous Coder (Generate Projects)
python autonomous_coder_cli.py

# Mode 2: Modern GUI (Enhanced Interface)
python launch_modern.py

# Mode 3: Classic GUI (All-in-One)
python main.py
```

---

## 🤖 Autonomous AI Coder

### **What It Does**

```
Input: "E-commerce website with cart and payment"

Process:
1. 🔍 Research best practices
2. 💻 Generate code files
3. 📦 Install dependencies
4. 🐛 Debug automatically
5. ✅ Working project ready!

Output: Complete React/Django/MERN/Android app
```

### **Supported Technologies**

| Technology | Description | Time | Files |
|-----------|-------------|------|-------|
| **React** | Modern React app | 2-3 min | 10-15 |
| **Django** | REST API backend | 3-4 min | 15-20 |
| **MERN** | Full-stack app | 4-5 min | 20-25 |
| **Android** | Native Android | 5-6 min | 25-30 |

### **Usage Examples**

#### **Example 1: React E-commerce**

```bash
python autonomous_coder_cli.py
```

```
Select: 1 (React)
Name: ecommerce-shop
Requirements: E-commerce with products, cart, checkout, payment

Output:
✅ Product listing component
✅ Shopping cart with Redux
✅ Checkout flow
✅ Payment integration
✅ User authentication
✅ Responsive design
```

#### **Example 2: Django Blog API**

```bash
python -m core.autonomous_coder \
  --type django \
  --name blog-api \
  --requirements "Blog API with posts, comments, auth"
```

```
Output:
✅ Post model with CRUD
✅ Comment system
✅ JWT authentication
✅ Admin panel
✅ API documentation
```

#### **Example 3: MERN Social Media**

```bash
python -m core.autonomous_coder \
  --type mern \
  --name social-app \
  --requirements "Social media with profiles, posts, likes"
```

```
Output:
✅ User profiles
✅ Post creation
✅ Like/comment system
✅ Real-time updates
✅ MongoDB database
```

### **How Self-Debugging Works**

```python
# Automatic debugging process
1. Generate code
2. Run tests
3. Detect errors
   ❌ SyntaxError: Missing import
4. Fix with AI
   ✅ Added import statement
5. Re-test
6. Repeat until success
```

**Example Debug Session:**

```
Attempt 1: SyntaxError detected
   🔧 Fixing: Missing import statement
   ✅ Fixed!

Attempt 2: TypeError detected
   🔧 Fixing: Incorrect parameter type
   ✅ Fixed!

Attempt 3: No errors
   ✅ Success! Project ready!
```

### **Internet Research**

Agent automatically researches:

```
Query: "best practices for React development 2024"

Searches:
1. DuckDuckGo search
2. Extract top 5 results
3. Analyze with AI
4. Extract:
   - Best practices
   - Recommended libraries
   - Architecture patterns
   - Code examples

Apply to code generation
```

---

## 🎨 Modern GUI

### **Features**

1. **🧵 Threaded Processing**
   - GUI never freezes
   - Background command execution
   - Real-time updates

2. **🧠 Smart Intent Detection**
   - Understands Hindi + English
   - Automatic command parsing
   - Context awareness

3. **💬 Conversation Memory**
   - Remembers last 20 exchanges
   - Context-aware responses
   - Better follow-ups

4. **📊 Live Statistics**
   - Skills loaded
   - Tools available
   - Queries processed
   - Success rate

5. **⚡ Quick Actions**
   - One-click shortcuts
   - Frequently used commands
   - Customizable

### **Usage**

```bash
# Start Modern GUI
python launch_modern.py
```

**Interface:**

```
┌─────────────────────────────────────────┐
│  🤖 JARVIS          ● Ready             │
├─────────────────────────────────────────┤
│  💬 Conversation    📊 Statistics       │
│  ┌────────────┐    ┌──────────────┐    │
│  │ Chat here  │    │ Skills: 22   │    │
│  │            │    │ Tools: 74    │    │
│  │            │    │ Queries: 15  │    │
│  └────────────┘    └──────────────┘    │
│                                         │
│  ⚡ Quick Actions                       │
│  [YouTube] [Browser] [Movies] [Code]   │
├─────────────────────────────────────────┤
│  Type command...    [Send] [🎤]        │
└─────────────────────────────────────────┘
```

### **Commands**

```bash
# Text commands
"open youtube"
"play song"
"generate react app"
"search python"

# Voice commands
"youtube kholo"
"gaana sunao"
"react app banao"
```

---

## 📺 Classic GUI

### **Features**

- ✅ All-in-one file (main.py)
- ✅ Auto-installs everything
- ✅ Simple interface
- ✅ Voice + text control
- ✅ Fast startup

### **Usage**

```bash
# Start Classic GUI
python main.py
```

**What Happens:**

```
1. Check dependencies
   ✅ Installing if needed

2. Check Ollama
   ✅ Installing if needed
   ✅ Starting server
   ✅ Pulling model

3. Open GUI
   ✅ Window opens
   ✅ Ready to use!
```

---

## 🎤 Voice Commands

### **Supported Commands**

#### **YouTube**
```
Hindi:
- "youtube kholo"
- "gaana sunao"
- "video chalao"

English:
- "open youtube"
- "play song"
- "play video"
```

#### **Browser**
```
Hindi:
- "browser kholo"
- "chrome kholo"
- "internet kholo"

English:
- "open browser"
- "open chrome"
- "open internet"
```

#### **Movies**
```
Hindi:
- "movie chalao"
- "film dekho"
- "inception play karo"

English:
- "play movie"
- "watch film"
- "play inception"
```

#### **Search**
```
Hindi:
- "google par search karo"
- "python kya hai"
- "AI ke baare mein batao"

English:
- "search on google"
- "what is python"
- "tell me about AI"
```

#### **System**
```
Hindi:
- "volume badhao"
- "volume kam karo"
- "computer band karo"

English:
- "volume up"
- "volume down"
- "shutdown computer"
```

#### **Coding (NEW!)**
```
Hindi:
- "react app banao"
- "django api banao"
- "android app banao"

English:
- "generate react app"
- "create django api"
- "build android app"
```

---

## 🎓 Skills & Tools

### **Complete List (22 Skills, 74 Tools)**

#### **1. 🤖 AI & Development**
- **Autonomous Coder** (NEW!)
  - generate_react_app
  - generate_django_app
  - generate_mern_app
  - generate_android_app
  - debug_project

- **Self-Coding AI**
  - write_code
  - fix_bugs
  - optimize_code

- **AI Architect**
  - design_system
  - create_architecture

- **Code Generator**
  - generate_function
  - generate_class

#### **2. 🎵 Entertainment**
- **YouTube Player**
  - play_video
  - search_video
  - download_video

- **Movie Downloader**
  - search_movie
  - download_movie

- **Music Operations**
  - play_music
  - control_playback

#### **3. 🌐 Web & Internet**
- **Web Operations**
  - open_website
  - browse_url

- **Internet Search**
  - google_search
  - web_scraping

- **Email Operations**
  - send_email
  - read_email

#### **4. 💻 System Control**
- **System Operations**
  - shutdown
  - restart
  - sleep
  - volume_control

- **Master PC Control**
  - advanced_control
  - process_management

- **File Operations**
  - create_file
  - delete_file
  - move_file

- **Screenshot**
  - take_screenshot
  - save_screenshot

#### **5. 🛠️ Utilities**
- **DateTime Operations**
  - get_time
  - get_date
  - set_alarm

- **Weather Operations**
  - get_weather
  - forecast

- **Memory Operations**
  - remember
  - recall

- **Text Operations**
  - text_to_speech
  - speech_to_text

- **Terminal Operations**
  - run_command
  - execute_script

---

## 🔧 Advanced Usage

### **1. Custom Project Generation**

```python
from core.autonomous_coder import AutonomousCoder

# Create coder
coder = AutonomousCoder(
    ollama_url="http://localhost:11434",
    model="llama3.2"
)

# Generate project
result = coder.generate_fullstack_project(
    project_type='react',
    project_name='my-app',
    requirements='Custom requirements here',
    output_dir='./output'
)

print(f"Success: {result['success']}")
print(f"Files: {result['files_generated']}")
```

### **2. Custom Intent Detection**

```python
from core.enhanced_agent import EnhancedAIAgent

# Create agent
agent = EnhancedAIAgent(engine)

# Add custom intent
agent.intent_patterns['custom'] = [
    r'(custom|कस्टम).*(action|एक्शन)',
]

# Add executor
def custom_executor(query, entities):
    return "Custom action executed!"

agent.action_executors['custom'] = custom_executor
```

### **3. Terminal Command Execution**

```python
from core.autonomous_coder import AutonomousCoder

coder = AutonomousCoder()

# Execute command
output = coder._run_terminal_command(
    'npm install',
    cwd='/path/to/project'
)

print(output)

# View history
print(coder.terminal_history)
```

### **4. Research Integration**

```python
# Research a topic
research_data = coder._research_project(
    project_type='react',
    requirements='e-commerce website'
)

print(research_data['best_practices'])
print(research_data['libraries'])
print(research_data['architecture'])
```

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. Ollama Not Running**

```bash
# Check if running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2
```

#### **2. GUI Not Opening**

```bash
# Check tkinter
python -c "import tkinter"

# Linux: Install
sudo apt-get install python3-tk

# macOS: Should be pre-installed
# Windows: Should be pre-installed
```

#### **3. Voice Not Working**

```bash
# Install dependencies
pip install SpeechRecognition pyaudio pyttsx3

# Linux: Install portaudio
sudo apt-get install portaudio19-dev

# macOS: Install portaudio
brew install portaudio

# Windows: Should work out of box
```

#### **4. Code Generation Fails**

```bash
# Check internet
ping google.com

# Check Ollama model
ollama list

# Try different model
ollama pull codellama
ollama pull mistral

# Increase timeout
# Edit core/autonomous_coder.py
# Change timeout=60 to timeout=120
```

#### **5. Dependencies Not Installing**

```bash
# For npm
npm cache clean --force
rm -rf node_modules
npm install

# For pip
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt

# For Gradle
./gradlew clean
./gradlew build --refresh-dependencies
```

---

## 📊 Performance Tips

### **1. Faster Code Generation**

```python
# Use faster model
coder = AutonomousCoder(model="llama3.2")  # Faster
# vs
coder = AutonomousCoder(model="codellama")  # More accurate
```

### **2. Reduce Debug Attempts**

```python
# Set max attempts
coder.max_debug_attempts = 3  # Default: 5
```

### **3. Optimize Research**

```python
# Reduce research queries
coder.research_queries = [
    "best practices for {project_type}",
    "common libraries for {project_type}"
]
```

### **4. Memory Management**

```python
# Clear conversation history
agent.clear_history()

# Limit history size
agent.conversation_history = agent.conversation_history[-20:]
```

---

## 🎯 Best Practices

### **1. Project Generation**

- ✅ Be specific in requirements
- ✅ Mention key features
- ✅ Specify technology preferences
- ✅ Include design requirements

**Good:**
```
"E-commerce website with:
- Product listing with filters
- Shopping cart with Redux
- Stripe payment integration
- User authentication with JWT
- Responsive Material-UI design"
```

**Bad:**
```
"Make an e-commerce site"
```

### **2. Voice Commands**

- ✅ Speak clearly
- ✅ Use wake word ("Jarvis")
- ✅ Keep commands simple
- ✅ Wait for response

### **3. Error Handling**

- ✅ Let auto-debug run first
- ✅ Check terminal output
- ✅ Review generated code
- ✅ Manual fix if needed

---

## 🚀 Next Steps

### **After Installation**

1. **Try Autonomous Coder**
   ```bash
   python autonomous_coder_cli.py
   ```

2. **Explore Modern GUI**
   ```bash
   python launch_modern.py
   ```

3. **Test Voice Commands**
   - Say "Jarvis, youtube kholo"
   - Say "Jarvis, generate react app"

4. **Generate Your First Project**
   - Choose project type
   - Describe requirements
   - Let AI do the work!

5. **Customize**
   - Add custom intents
   - Create quick actions
   - Modify theme

---

## 📚 Additional Resources

- **[Autonomous Coder Guide](AUTONOMOUS_CODER.md)** - Detailed coder documentation
- **[Modern GUI Guide](MODERN_GUI.md)** - GUI features and usage
- **[Improvements Guide](IMPROVEMENTS.md)** - What's new
- **[Quick Start](QUICKSTART.md)** - 5-minute setup

---

## 🤝 Community

- **GitHub**: [Aryankaushik541/Zarves](https://github.com/Aryankaushik541/Zarves)
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Contributions**: Pull requests welcome!

---

## 🎉 Summary

**JARVIS** aapko 3 powerful modes deta hai:

1. **🤖 Autonomous Coder**
   - Full-stack projects generate karo
   - Self-debugging
   - Production-ready code

2. **🎨 Modern GUI**
   - Beautiful interface
   - Smart AI agent
   - Voice + text control

3. **📺 Classic GUI**
   - Simple and fast
   - All-in-one file
   - Auto-setup

**Start now:**

```bash
# Generate projects
python autonomous_coder_cli.py

# Or use GUI
python launch_modern.py

# Or classic
python main.py
```

---

**Made with ❤️ for developers by developers**

**Happy Coding! 🚀**

# JARVIS - Autonomous AI Assistant 🤖

> **Your Voice. Your Command. Complete System Control.**

JARVIS is not just an AI assistant - it's a **fully autonomous agent** that can control your entire Mac system. Create websites, develop applications, install software, manage files, and execute complex tasks with just your voice.

## 🚀 What Makes JARVIS Special?

### **Truly Autonomous**
- Just speak your command - JARVIS handles everything
- No manual coding, no terminal commands, no file management
- Multi-step task execution without supervision
- Smart decision-making and error recovery

### **Full System Control**
- **Web Development**: Create full-stack websites (React, HTML/CSS/JS)
- **App Development**: Build Python apps (GUI, CLI, automation)
- **Software Installation**: Install any application via Homebrew
- **Terminal Access**: Execute any shell command
- **File Management**: Organize, create, edit, move files
- **Git Operations**: Clone, commit, push, pull repositories
- **Code Generation**: Generate code in any language

## 🎯 Quick Examples

```
"Jarvis, create a portfolio website"
→ Creates complete website with HTML/CSS/JS and opens in browser

"Jarvis, install Visual Studio Code"
→ Installs VS Code using Homebrew

"Jarvis, build a GUI calculator app"
→ Creates Python app with Tkinter and runs it

"Jarvis, organize my Downloads folder"
→ Sorts files by type into organized folders

"Jarvis, clone my GitHub repo and install dependencies"
→ Clones repo and runs npm install
```

## ✨ Core Features

### 🌐 Web Development
- **React Apps**: Full create-react-app setup
- **Vanilla Websites**: HTML/CSS/JavaScript
- **Responsive Design**: Modern, beautiful UIs
- **Auto-deployment**: Opens in browser automatically

### 🐍 Python Development
- **GUI Apps**: Tkinter-based applications
- **CLI Tools**: Command-line utilities
- **Automation**: Task automation scripts
- **Data Science**: Jupyter notebooks and analysis tools

### 📦 Application Management
- **Install Anything**: Python, Node, Docker, VS Code, etc.
- **Homebrew Integration**: Automatic package management
- **Dependency Handling**: Manages all dependencies
- **GUI & CLI Apps**: Both supported

### 💻 Terminal Control
- **Any Command**: Execute shell commands
- **Directory Context**: Run in specific folders
- **Output Capture**: See command results
- **Error Handling**: Graceful failure recovery

### 📁 File Operations
- **Smart Organization**: Auto-sort by file type
- **Batch Operations**: Move/copy/delete multiple files
- **Project Templates**: Complete folder structures
- **Content Creation**: Create files with content

### 🔧 Git Integration
- **Clone Repos**: From any Git URL
- **Commit & Push**: Automated workflows
- **Status Checks**: Monitor repository state
- **Branch Management**: Create and switch branches

## 🎮 Interaction Modes

### Voice Mode (Default)
```bash
python main.py
```
- Hands-free operation
- Wake word: "Jarvis"
- Natural language understanding
- Text-to-speech responses

### Text Mode (Silent)
```bash
python main.py --text
```
- Type commands instead of speaking
- Perfect for quiet environments
- Faster for debugging
- Same powerful capabilities

## 📋 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

### 2. Set up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.template .env
```

Edit `.env` and add your **Groq API Key**:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from: [Groq Console](https://console.groq.com)

### 5. Run JARVIS
```bash
python main.py
```

## 🎯 Usage Examples

### Web Development
```
"Jarvis, create a todo app with React"
"Jarvis, build a landing page for my startup"
"Jarvis, make a portfolio website with dark theme"
```

### App Development
```
"Jarvis, create a GUI calculator"
"Jarvis, build a CLI tool for file management"
"Jarvis, make an automation script for organizing photos"
```

### Installation & Setup
```
"Jarvis, install Python and Node.js"
"Jarvis, set up my development environment"
"Jarvis, install Docker and Postman"
```

### File Management
```
"Jarvis, organize my Downloads folder"
"Jarvis, create a project structure for a web app"
"Jarvis, move all PDFs to Documents"
```

### Git Operations
```
"Jarvis, clone https://github.com/user/repo.git"
"Jarvis, commit my changes with message 'Added features'"
"Jarvis, push to GitHub"
```

### Code Generation
```
"Jarvis, create a Python script to scrape websites"
"Jarvis, write JavaScript for form validation"
"Jarvis, generate HTML for a contact form"
```

## 🏗️ Project Structure

```
Zarves/
├── main.py              # Entry point
├── core/                # Core engine
│   ├── engine.py        # AI engine with autonomous capabilities
│   ├── voice.py         # Voice I/O
│   ├── registry.py      # Skill management
│   └── skill.py         # Base skill class
├── gui/                 # Futuristic HUD interface
│   └── app.py          # PyQt6 GUI
├── skill/              # Autonomous skills
│   ├── code_generator.py      # Web & app development
│   ├── terminal_ops.py        # Terminal & installation
│   ├── advanced_file_ops.py   # File management
│   ├── system_ops.py          # System control
│   ├── web_ops.py             # Web operations
│   ├── weather_ops.py         # Weather info
│   ├── email_ops.py           # Email management
│   ├── file_ops.py            # Basic file ops
│   ├── text_ops.py            # Text processing
│   ├── memory_ops.py          # Memory/notes
│   ├── datetime_ops.py        # Date/time
│   └── screenshot_ops.py      # Screenshots
├── requirements.txt     # Dependencies
├── .env.template       # Environment template
├── README.md           # This file
├── AUTONOMOUS_GUIDE.md # Detailed autonomous features guide
└── TESTING.md          # Testing guide

```

## 🔧 Tech Stack

- **Language**: Python 3
- **GUI**: PyQt6 (Futuristic HUD)
- **AI Engine**: Groq API (llama-3.3-70b-versatile)
- **Voice**: SpeechRecognition + pyttsx3
- **Package Manager**: Homebrew (macOS)
- **Web**: React, HTML/CSS/JavaScript
- **Automation**: subprocess, os, shutil

## 🎓 Documentation

- **[AUTONOMOUS_GUIDE.md](AUTONOMOUS_GUIDE.md)** - Complete guide to autonomous features
- **[TESTING.md](TESTING.md)** - Testing and troubleshooting guide
- **[.env.template](.env.template)** - Environment configuration

## 🌟 Key Capabilities

| Feature | Description |
|---------|-------------|
| 🌐 **Full-Stack Web Dev** | Create React apps or vanilla websites |
| 🐍 **Python Apps** | GUI, CLI, automation, data science |
| 📦 **App Installation** | Install any software via Homebrew |
| 💻 **Terminal Control** | Execute any shell command |
| 📁 **File Management** | Organize, create, edit, batch operations |
| 🔧 **Git Integration** | Clone, commit, push, pull |
| 🎨 **Code Generation** | Any language, any file type |
| 🤖 **Multi-Step Tasks** | Complex autonomous workflows |
| 🧠 **Smart Decisions** | AI chooses best approach |
| 🔄 **Error Recovery** | Handles failures gracefully |

## 🚨 System Requirements

- **OS**: macOS (currently optimized for Mac)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space
- **Internet**: Required for AI and installations
- **Microphone**: For voice mode

## 🎮 Controls

### Voice Commands
- Say **"Jarvis"** followed by your command
- Or use direct commands: "open", "create", "install", etc.

### GUI Controls
- **Click HUD**: Pause/Resume listening
- **Close Window**: Shutdown JARVIS

### Text Mode
- Type commands directly
- Press Ctrl+C to exit

## 🔐 Privacy & Security

- All processing happens locally except AI calls
- No data stored on external servers
- Groq API used only for natural language processing
- File operations require explicit commands
- Terminal commands executed with user permissions

## 🐛 Troubleshooting

### Common Issues

**"GROQ_API_KEY not found"**
- Add your API key to `.env` file

**"Command not working"**
- Try rephrasing with more details
- Use wake word "Jarvis"
- Check console for errors

**"Installation failed"**
- JARVIS will install Homebrew automatically
- Check internet connection
- Verify app name spelling

**"Voice not recognized"**
- Check microphone permissions
- Speak clearly after "Listening..." prompt
- Try text mode: `python main.py --text`

See [TESTING.md](TESTING.md) for detailed troubleshooting.

## 🚀 Future Roadmap

- [ ] Windows & Linux support
- [ ] Mobile app development (iOS/Android)
- [ ] Database management
- [ ] API creation and testing
- [ ] Cloud deployment integration
- [ ] Machine learning workflows
- [ ] Video/Image editing
- [ ] System monitoring
- [ ] Multi-language support
- [ ] Voice customization

## 📜 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- Groq for powerful AI inference
- PyQt6 for beautiful GUI framework
- Homebrew for package management
- Open source community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Aryankaushik541/Zarves/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aryankaushik541/Zarves/discussions)

---

## 🎯 Quick Start

```bash
# 1. Clone
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.template .env
# Add your GROQ_API_KEY to .env

# 4. Run
python main.py

# 5. Speak
"Jarvis, create a website for me"
```

---

**Built with ❤️ by Aryan Kaushik**

**Your Voice. Your Command. Complete Control. 🚀**

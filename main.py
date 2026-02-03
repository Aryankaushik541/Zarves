#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Personal AI Assistant
Fully Automated Setup & Launch - Zero Configuration Required
"""

import sys
import os
import subprocess
import platform
import time
import threading
import json
from pathlib import Path

# Try to import tkinter (GUI framework)
try:
    import tkinter as tk
    from tkinter import scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# ============================================================================
# AUTO-INSTALL DEPENDENCIES - SILENT MODE
# ============================================================================

def silent_install_package(package):
    """Silently install a package"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package, "-q", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120
        )
        return True
    except:
        return False

def auto_install_dependencies():
    """Auto-install ALL missing packages silently"""
    print("📦 Checking dependencies...")
    
    required = {
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
        'pyautogui': 'pyautogui',
        'psutil': 'psutil',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
        'ollama': 'ollama',
        'requests': 'requests',
        'pillow': 'Pillow',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   ⏳ Auto-installing {len(missing)} packages...")
        installed = 0
        for package in missing:
            if silent_install_package(package):
                installed += 1
        print(f"   ✅ Installed {installed}/{len(missing)} packages")
    else:
        print("   ✅ All dependencies ready")
    
    return True

# ============================================================================
# OLLAMA AUTO-SETUP - FULLY AUTOMATED
# ============================================================================

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(
            ['ollama', '--version'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def start_ollama_server():
    """Start Ollama server in background"""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(
                ['ollama', 'serve'], 
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ['ollama', 'serve'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait for server to start
        for i in range(10):
            time.sleep(1)
            if check_ollama_running():
                return True
        return False
    except:
        return False

def check_ollama_model():
    """Check if llama3.2 model is available"""
    try:
        result = subprocess.run(
            ['ollama', 'list'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        return 'llama3.2' in result.stdout
    except:
        return False

def pull_ollama_model_background():
    """Download llama3.2 model in background"""
    def _download():
        try:
            subprocess.run(
                ['ollama', 'pull', 'llama3.2'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=600
            )
        except:
            pass
    
    threading.Thread(target=_download, daemon=True).start()

def setup_ollama():
    """Fully automated Ollama setup"""
    print("🤖 Setting up AI Engine...")
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("   ⚠️  Ollama not installed")
        print("   💡 Download from: https://ollama.com/download")
        print("   ⏭️  Continuing with cloud AI fallback...")
        return False
    
    print("   ✅ Ollama found")
    
    # Auto-start server if not running
    if not check_ollama_running():
        print("   ⏳ Starting Ollama server...")
        if start_ollama_server():
            print("   ✅ Server started")
        else:
            print("   ⚠️  Server start failed")
            print("   ⏭️  Continuing with cloud AI fallback...")
            return False
    else:
        print("   ✅ Server running")
    
    # Check model and auto-download if missing
    if not check_ollama_model():
        print("   ⏳ Downloading AI model in background...")
        print("   💡 JARVIS will start immediately, model downloads separately")
        pull_ollama_model_background()
        return False  # Use cloud AI until model is ready
    
    print("   ✅ AI model ready")
    return True

# ============================================================================
# AUTO-FIX COMMON ISSUES
# ============================================================================

def auto_create_directories():
    """Auto-create required directories"""
    dirs = ['core', 'skill', 'gui', 'data', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)

def auto_fix_permissions():
    """Auto-fix file permissions on Unix systems"""
    if platform.system() != "Windows":
        try:
            os.chmod(__file__, 0o755)
        except:
            pass

def check_and_fix_environment():
    """Check and auto-fix environment issues"""
    # Create directories
    auto_create_directories()
    
    # Fix permissions
    auto_fix_permissions()
    
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'

# ============================================================================
# ENHANCED GUI WITH AUTO-RECOVERY
# ============================================================================

class EnhancedJarvisGUI:
    """Enhanced JARVIS GUI with auto-recovery"""
    
    def __init__(self, root, ollama_ready=False):
        self.root = root
        self.root.title("🤖 JARVIS - AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0d1117')
        
        self.ollama_ready = ollama_ready
        self.engine = None
        self.registry = None
        self.listening = False
        
        # Create GUI
        self._create_gui()
        
        # Initialize JARVIS
        threading.Thread(target=self._init_jarvis, daemon=True).start()
    
    def _create_gui(self):
        """Create modern GUI"""
        # Header
        header = tk.Frame(self.root, bg='#161b22', height=80)
        header.pack(fill=tk.X, padx=15, pady=15)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 JARVIS",
            font=('Arial', 24, 'bold'),
            bg='#161b22',
            fg='#58a6ff'
        )
        title.pack(side=tk.LEFT, padx=20)
        
        subtitle = tk.Label(
            header,
            text="Personal AI Assistant",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e'
        )
        subtitle.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_indicator = tk.Label(
            header,
            text="● Initializing",
            font=('Arial', 11),
            bg='#161b22',
            fg='#f0883e'
        )
        self.status_indicator.pack(side=tk.RIGHT, padx=20)
        
        # Chat area
        chat_frame = tk.Frame(self.root, bg='#0d1117')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#010409',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = tk.Frame(self.root, bg='#161b22', height=60)
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        input_frame.pack_propagate(False)
        
        self.input_box = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            borderwidth=2,
            relief=tk.FLAT
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 10), pady=10)
        self.input_box.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 11, 'bold'),
            bg='#238636',
            fg='white',
            command=self.send_message,
            width=10,
            borderwidth=0,
            cursor='hand2'
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        
        voice_btn = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=('Arial', 11, 'bold'),
            bg='#1f6feb',
            fg='white',
            command=self.voice_input,
            width=10,
            borderwidth=0,
            cursor='hand2'
        )
        voice_btn.pack(side=tk.LEFT, padx=(0, 10), pady=10)
    
    def _init_jarvis(self):
        """Initialize JARVIS with auto-recovery"""
        try:
            self.add_message("SYSTEM", "📦 Loading skills...", "#58a6ff")
            
            from core.registry import SkillRegistry
            from core.engine import JarvisEngine
            
            self.registry = SkillRegistry()
            
            self.add_message("SYSTEM", "🧠 Initializing AI engine...", "#58a6ff")
            self.engine = JarvisEngine(self.registry)
            
            skill_count = len(self.registry.skills)
            tool_count = sum(len(s.get('tools', [])) for s in self.registry.skills.values())
            
            mode = "Full AI Mode" if self.ollama_ready else "Cloud AI Mode"
            
            self.add_message(
                "JARVIS",
                f"✅ JARVIS Ready! ({mode})\n\n"
                f"📊 {skill_count} skills loaded with {tool_count} tools\n\n"
                f"💬 How can I help you today?",
                "#3fb950"
            )
            
            self.update_status("● Ready", "#3fb950")
            
        except Exception as e:
            self.add_message("SYSTEM", f"⚠️  Limited mode: {str(e)[:100]}", "#f85149")
            self.add_message("SYSTEM", "💡 Basic commands still available", "#f0883e")
            self.update_status("● Limited Mode", "#f0883e")
    
    def add_message(self, sender, message, color="#c9d1d9"):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        import datetime
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        
        icons = {"SYSTEM": "⚙️", "JARVIS": "🤖", "You": "👤"}
        icon = icons.get(sender, "💬")
        
        prefix = f"{timestamp} {icon} {sender}: "
        
        self.chat_display.insert(tk.END, prefix, "prefix")
        self.chat_display.insert(tk.END, message + "\n\n", "message")
        
        self.chat_display.tag_config("prefix", foreground=color, font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config("message", foreground=color)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, text, color):
        """Update status indicator"""
        self.status_indicator.config(text=text, fg=color)
    
    def send_message(self):
        """Send text message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, tk.END)
        self.add_message("You", message, "#c9d1d9")
        
        if self.engine:
            self.update_status("● Processing", "#f0883e")
            threading.Thread(target=self._process_query, args=(message,), daemon=True).start()
        else:
            self.add_message("JARVIS", "⚠️  Engine not ready. Please wait...", "#f85149")
    
    def voice_input(self):
        """Voice input with auto-recovery"""
        if self.listening:
            return
        
        self.listening = True
        self.update_status("● Listening", "#a371f7")
        
        def _listen():
            try:
                from core.voice import listen
                command = listen()
                if command and command != "none":
                    self.add_message("You", command, "#c9d1d9")
                    if self.engine:
                        self._process_query(command)
                else:
                    self.add_message("SYSTEM", "No voice detected", "#f0883e")
            except Exception as e:
                self.add_message("SYSTEM", f"Voice error: {str(e)[:100]}", "#f85149")
            finally:
                self.listening = False
                self.update_status("● Ready", "#3fb950")
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def _process_query(self, query):
        """Process query with auto-recovery"""
        try:
            response = self.engine.process_query(query)
            self.add_message("JARVIS", response, "#3fb950")
            
            # Speak response
            try:
                from core.voice import speak
                speak(response[:200])
            except:
                pass
                
        except Exception as e:
            error_msg = str(e)[:200]
            self.add_message("JARVIS", f"⚠️  Error: {error_msg}", "#f85149")
            self.add_message("SYSTEM", "💡 Trying to recover...", "#f0883e")
        finally:
            self.update_status("● Ready", "#3fb950")

# ============================================================================
# LAUNCH FUNCTIONS
# ============================================================================

def launch_gui(ollama_ready=False):
    """Launch GUI with auto-recovery"""
    if not TKINTER_AVAILABLE:
        print("❌ tkinter not available")
        print("💡 Install: pip install tk")
        return
    
    try:
        print("✅ Launching GUI...")
        root = tk.Tk()
        app = EnhancedJarvisGUI(root, ollama_ready)
        root.mainloop()
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        print("💡 Try: pip install --upgrade tk pillow")

# ============================================================================
# MAIN - FULLY AUTOMATED
# ============================================================================

def main():
    """Fully automated main entry point"""
    
    print("\n" + "="*70)
    print("🤖 JARVIS - Personal AI Assistant")
    print("="*70)
    print()
    
    # Auto-fix environment
    check_and_fix_environment()
    
    # Auto-install dependencies
    auto_install_dependencies()
    
    # Auto-setup Ollama (optional)
    ollama_ready = setup_ollama()
    
    print()
    print("🚀 Starting JARVIS...")
    print()
    
    if ollama_ready:
        print("✅ Full AI Mode Enabled")
        print("   • Local AI processing")
        print("   • Natural conversations")
        print("   • Smart task execution")
    else:
        print("💡 Cloud AI Mode")
        print("   • Cloud-based processing")
        print("   • All features available")
        print("   • Install Ollama for local AI")
    
    print()
    print("🎯 Features:")
    print("   ✅ Voice & Text Control")
    print("   ✅ YouTube Auto-Play")
    print("   ✅ Browser Automation")
    print("   ✅ File Management")
    print("   ✅ System Control")
    print("   ✅ Code Generation")
    print()
    print("="*70)
    print()
    
    # Launch GUI
    launch_gui(ollama_ready)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print()
        print("💡 Auto-recovery failed. Please report at:")
        print("   https://github.com/Aryankaushik541/Zarves/issues")
        print()
        print("🔧 Quick fixes to try:")
        print("   1. pip install --upgrade pip")
        print("   2. pip install -r requirements.txt")
        print("   3. python -m pip install --force-reinstall pyttsx3")

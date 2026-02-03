#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Personal AI Assistant
Complete all-in-one launcher with GUI
"""

import sys
import os
import subprocess
import platform
import time
import threading
from pathlib import Path

# ============================================================================
# OLLAMA SETUP FUNCTIONS
# ============================================================================

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except:
        return False

def install_ollama():
    """Install Ollama based on platform"""
    system = platform.system()
    
    print("   📥 Installing Ollama...")
    print()
    
    if system == "Darwin":  # macOS
        try:
            subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh'], 
                         capture_output=True, check=True)
            subprocess.run(['sh', '-'], 
                         input=subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh'], 
                                            capture_output=True, check=True).stdout,
                         check=True)
            print("   ✅ Ollama installed successfully!")
            return True
        except:
            print("   ⚠️  Auto-install failed")
            print("   💡 Please install manually: https://ollama.com/download")
            return False
    
    elif system == "Linux":
        try:
            subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh', '|', 'sh'], 
                         shell=True, check=True)
            print("   ✅ Ollama installed successfully!")
            return True
        except:
            print("   ⚠️  Auto-install failed")
            print("   💡 Please install manually: https://ollama.com/download")
            return False
    
    elif system == "Windows":
        print("   ⚠️  Windows detected - manual installation required")
        print()
        print("   📥 Download from: https://ollama.com/download/windows")
        print()
        input("   Press Enter after installing Ollama...")
        return check_ollama_installed()
    
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
            subprocess.Popen(['ollama', 'serve'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(['ollama', 'serve'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        print("   ⏳ Starting Ollama server...")
        for i in range(10):
            time.sleep(1)
            if check_ollama_running():
                print("   ✅ Ollama server started!")
                return True
        
        return False
    except:
        return False

def check_ollama_model():
    """Check if llama3.2 model is available"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return 'llama3.2' in result.stdout
    except:
        return False

def pull_ollama_model():
    """Download llama3.2 model"""
    print()
    print("   📥 Downloading AI model (llama3.2)...")
    print("   ⏳ This may take 2-5 minutes (~2GB download)...")
    print()
    
    try:
        result = subprocess.run(['ollama', 'pull', 'llama3.2'],
                              capture_output=False,
                              text=True,
                              timeout=600)  # 10 minute timeout
        
        if result.returncode == 0:
            print()
            print("   ✅ Model downloaded successfully!")
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        print()
        print("   ⚠️  Download timed out")
        return False
    except:
        return False

def setup_ollama():
    """Complete Ollama setup"""
    print("🤖 Setting up AI Engine (Ollama)...")
    print()
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("   ⚠️  Ollama not found!")
        print()
        
        response = input("   Install Ollama now? (y/n): ").lower().strip()
        if response == 'y':
            if not install_ollama():
                print()
                print("   ⚠️  Ollama installation failed!")
                print("   💡 JARVIS will run in limited mode")
                print()
                return False
        else:
            print()
            print("   ⚠️  Skipping Ollama installation")
            print("   💡 JARVIS will run in limited mode")
            print()
            return False
    else:
        print("   ✅ Ollama found!")
    
    # Check if server is running
    if not check_ollama_running():
        if not start_ollama_server():
            print()
            print("   ⚠️  Failed to start Ollama server")
            print("   💡 Please run manually: ollama serve")
            print("   💡 JARVIS will run in limited mode")
            print()
            return False
    else:
        print("   ✅ Ollama server running!")
    
    # Check if model exists
    if not check_ollama_model():
        print("   ⚠️  AI model (llama3.2) not found")
        print()
        
        response = input("   Download model now? (y/n): ").lower().strip()
        if response == 'y':
            if not pull_ollama_model():
                print()
                print("   ⚠️  Model download failed!")
                print("   💡 JARVIS will run in limited mode")
                print()
                return False
        else:
            print()
            print("   ⚠️  Skipping model download")
            print("   💡 JARVIS will run in limited mode")
            print()
            return False
    else:
        print("   ✅ AI model ready!")
    
    print()
    print("✅ AI Engine ready!")
    print()
    return True

# ============================================================================
# AUTO-INSTALL DEPENDENCIES
# ============================================================================

def auto_install_dependencies():
    """Auto-install missing packages"""
    print("📦 Checking Python dependencies...")
    print()
    
    required = {
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
        'pyautogui': 'pyautogui',
        'psutil': 'psutil',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
        'ollama': 'ollama',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   ⏳ Installing {len(missing)} missing packages...")
        print()
        for package in missing:
            print(f"      Installing {package}...", end=" ")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
                print("✅")
            except:
                print("⚠️ (optional)")
        print()
        print("✅ Dependencies ready!")
    else:
        print("   ✅ All dependencies installed!")
    
    print()
    return True

# ============================================================================
# SIMPLE GUI - ALL IN ONE
# ============================================================================

class SimpleJarvisGUI:
    """Simple JARVIS GUI - all in one"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - AI Assistant")
        self.root.geometry("900x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize JARVIS
        self.engine = None
        self.registry = None
        self.listening = False
        
        # Create GUI
        self._create_gui()
        
        # Initialize JARVIS in background
        try:
            from core.registry import SkillRegistry
            from core.engine import JarvisEngine
            from core.voice import speak, listen
            self.speak = speak
            self.listen = listen
            threading.Thread(target=self._init_jarvis, daemon=True).start()
        except Exception as e:
            self.add_message("SYSTEM", f"⚠️  JARVIS core not available: {e}", "red")
    
    def _create_gui(self):
        """Create simple GUI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2a2a2a', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 JARVIS - Personal AI Assistant",
            font=('Arial', 18, 'bold'),
            bg='#2a2a2a',
            fg='#00ff00'
        )
        title_label.pack(pady=15)
        
        # Chat area
        chat_frame = tk.Frame(self.root, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#0a0a0a',
            fg='#ffffff',
            insertbackground='white',
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = tk.Frame(self.root, bg='#2a2a2a')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_box = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='#3a3a3a',
            fg='white',
            insertbackground='white'
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_box.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 11, 'bold'),
            bg='#00aa00',
            fg='white',
            command=self.send_message,
            width=10
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        voice_btn = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=('Arial', 11, 'bold'),
            bg='#0066cc',
            fg='white',
            command=self.voice_input,
            width=10
        )
        voice_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="● Initializing...",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#ffaa00',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 5))
    
    def _init_jarvis(self):
        """Initialize JARVIS engine"""
        try:
            from core.registry import SkillRegistry
            from core.engine import JarvisEngine
            
            self.add_message("SYSTEM", "📦 Loading skills...", "#00aaff")
            self.registry = SkillRegistry()
            
            self.add_message("SYSTEM", "🧠 Initializing AI engine...", "#00aaff")
            self.engine = JarvisEngine(self.registry)
            
            self.add_message("SYSTEM", "🎤 Voice assistant ready!", "#00aaff")
            
            # Success message
            skill_count = len(self.registry.skills)
            tool_count = sum(len(s.get('tools', [])) for s in self.registry.skills.values())
            
            self.add_message(
                "JARVIS",
                f"✅ JARVIS Ready!\n\n📊 Loaded {skill_count} skills with {tool_count} tools\n\n💬 How can I help you today?",
                "#00ff00"
            )
            
            self.update_status("● Ready", "#00ff00")
            
        except Exception as e:
            self.add_message("SYSTEM", f"❌ Error initializing JARVIS: {e}", "red")
            self.update_status("● Error", "red")
    
    def add_message(self, sender, message, color="#ffffff"):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        
        # Add message
        if sender == "SYSTEM":
            prefix = f"{timestamp} ⚙️ SYSTEM: "
        elif sender == "JARVIS":
            prefix = f"{timestamp} 🤖 JARVIS: "
        else:
            prefix = f"{timestamp} 👤 You: "
        
        self.chat_display.insert(tk.END, prefix, "prefix")
        self.chat_display.insert(tk.END, message + "\n\n", "message")
        
        # Apply colors
        self.chat_display.tag_config("prefix", foreground=color, font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config("message", foreground=color)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, text, color):
        """Update status bar"""
        self.status_label.config(text=text, fg=color)
    
    def send_message(self):
        """Send text message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, tk.END)
        self.add_message("You", message, "#ffffff")
        
        # Process with JARVIS
        if self.engine:
            self.update_status("● Processing...", "#ffaa00")
            threading.Thread(target=self._process_query, args=(message,), daemon=True).start()
        else:
            self.add_message("JARVIS", "⚠️  JARVIS engine not ready yet. Please wait...", "red")
    
    def voice_input(self):
        """Voice input"""
        if self.listening:
            return
        
        self.listening = True
        self.update_status("● Listening...", "#ff00ff")
        
        def _listen():
            try:
                command = self.listen()
                if command and command != "none":
                    self.add_message("You", command, "#ffffff")
                    if self.engine:
                        self._process_query(command)
                else:
                    self.add_message("SYSTEM", "No voice detected", "#ffaa00")
            except Exception as e:
                self.add_message("SYSTEM", f"Voice error: {e}", "red")
            finally:
                self.listening = False
                self.update_status("● Ready", "#00ff00")
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def _process_query(self, query):
        """Process query with JARVIS"""
        try:
            response = self.engine.process_query(query)
            self.add_message("JARVIS", response, "#00ff00")
            
            # Speak response (limit length)
            try:
                self.speak(response[:200])
            except:
                pass
                
        except Exception as e:
            self.add_message("JARVIS", f"Error: {e}", "red")
        finally:
            self.update_status("● Ready", "#00ff00")


def launch_gui():
    """Launch GUI"""
    try:
        import tkinter as tk
        from tkinter import scrolledtext
        
        print("✅ GUI framework (tkinter) available")
        print()
        print("🎨 Opening GUI window...")
        print()
        
        root = tk.Tk()
        app = SimpleJarvisGUI(root)
        
        print("✅ GUI window opened!")
        print("💡 If you don't see the window, check your taskbar\n")
        
        root.mainloop()
        
    except ImportError:
        print("❌ Error: tkinter not found!")
        print()
        print("💡 Install tkinter:")
        if platform.system() == "Linux":
            print("   sudo apt-get install python3-tk")
        elif platform.system() == "Darwin":
            print("   brew install python-tk")
        else:
            print("   Reinstall Python with tkinter support")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Try installing dependencies manually:")
        print("   pip install pyttsx3 SpeechRecognition pyautogui psutil selenium webdriver-manager ollama")
        print()

# ============================================================================
# MAIN - ALL IN ONE
# ============================================================================

def main():
    """Main entry point - All in one"""
    
    print("\n" + "="*70)
    print("🤖 JARVIS - Personal AI Assistant")
    print("="*70)
    print()
    
    # Install Python dependencies
    auto_install_dependencies()
    
    # Setup Ollama (optional but recommended)
    ollama_ready = setup_ollama()
    
    # Launch GUI
    print("🚀 Launching JARVIS GUI...")
    print()
    
    if ollama_ready:
        print("💡 Full Mode Enabled:")
        print("   ✅ Local AI processing")
        print("   ✅ Natural conversations")
        print("   ✅ Smart task execution")
    else:
        print("💡 Limited Mode:")
        print("   ⚠️  Basic commands only")
        print("   ⚠️  No AI conversations")
        print("   💡 Install Ollama for full features")
    
    print()
    print("🎵 Features:")
    print("   ✅ YouTube Auto-Play")
    print("   ✅ Browser Auto-Login")
    print("   ✅ PC Movie Search")
    print("   ✅ VLC Auto-Play")
    print("   ✅ Voice & Text Control")
    print()
    print("="*70)
    print()
    
    # Launch GUI
    launch_gui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print()
        print("💡 For help, create an issue at:")
        print("   https://github.com/Aryankaushik541/Zarves/issues")

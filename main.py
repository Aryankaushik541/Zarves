#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Personal AI Assistant
Main entry point with automatic setup
"""

import sys
import os
import subprocess
import platform
import time

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
# MAIN - AUTO-LAUNCH GUI
# ============================================================================

def main():
    """Main entry point - Auto-launches GUI"""
    
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
    
    try:
        # Import and run simple GUI
        from jarvis_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ Error: GUI module not found")
        print(f"   Details: {e}")
        print()
        print("💡 Make sure jarvis_gui.py exists")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Try installing dependencies manually:")
        print("   pip install pyttsx3 SpeechRecognition pyautogui psutil selenium webdriver-manager ollama")
        print()


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

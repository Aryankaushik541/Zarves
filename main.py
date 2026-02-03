#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Complete AI Assistant
Beautiful GUI Interface - Auto-Launch
YouTube Auto-Play Support!
Just run: python main.py
"""

import sys
import os
import subprocess
import platform
import time
import urllib.request
import shutil

# ============================================================================
# AUTO-INSTALL OLLAMA
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

def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        import urllib.request
        urllib.request.urlopen('http://localhost:11434/api/tags', timeout=2)
        return True
    except:
        return False

def start_ollama_server():
    """Start Ollama server in background"""
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(['ollama', 'serve'], 
                           creationflags=subprocess.CREATE_NO_WINDOW,
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
        
        print("   ⚠️  Ollama server start timeout")
        return False
    except Exception as e:
        print(f"   ⚠️  Failed to start Ollama: {e}")
        return False

def check_ollama_model():
    """Check if llama3.2 model is available"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        return 'llama3.2' in result.stdout
    except:
        return False

def pull_ollama_model():
    """Pull llama3.2 model"""
    try:
        print("   📥 Downloading AI model (llama3.2)...")
        print("   ⏳ This may take 2-5 minutes (~2GB download)...")
        print()
        
        # Run ollama pull with live output
        process = subprocess.Popen(['ollama', 'pull', 'llama3.2'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  text=True,
                                  bufsize=1)
        
        for line in process.stdout:
            line = line.strip()
            if line:
                print(f"   {line}")
        
        process.wait()
        
        if process.returncode == 0:
            print()
            print("   ✅ Model downloaded successfully!")
            return True
        else:
            print()
            print("   ⚠️  Model download failed")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Failed to download model: {e}")
        return False

def install_ollama():
    """Install Ollama based on OS"""
    system = platform.system()
    
    print("   📥 Installing Ollama...")
    print()
    
    try:
        if system == 'Windows':
            print("   ⚠️  Windows detected!")
            print()
            print("   Please install Ollama manually:")
            print("   1. Download: https://ollama.com/download/windows")
            print("   2. Run the installer")
            print("   3. Restart this script")
            print()
            input("   Press Enter after installing Ollama...")
            return check_ollama_installed()
            
        elif system == 'Darwin':  # macOS
            print("   🍎 macOS detected - Installing Ollama...")
            result = subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh'],
                                  capture_output=True,
                                  text=True)
            if result.returncode == 0:
                install_script = result.stdout
                subprocess.run(['sh', '-c', install_script], check=True)
                print("   ✅ Ollama installed!")
                return True
            else:
                print("   ⚠️  Installation failed")
                return False
                
        elif system == 'Linux':
            print("   🐧 Linux detected - Installing Ollama...")
            result = subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh'],
                                  capture_output=True,
                                  text=True)
            if result.returncode == 0:
                install_script = result.stdout
                subprocess.run(['sh', '-c', install_script], check=True)
                print("   ✅ Ollama installed!")
                return True
            else:
                print("   ⚠️  Installation failed")
                return False
        else:
            print(f"   ⚠️  Unsupported OS: {system}")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Installation error: {e}")
        return False

def setup_ollama():
    """Complete Ollama setup"""
    print("🤖 Setting up AI Engine (Ollama)...")
    print()
    
    # Check if installed
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
    
    # Check if running
    if not check_ollama_running():
        print("   ⚠️  Ollama server not running")
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
        # Import and run GUI directly
        from gui.app import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ Error: GUI module not found")
        print(f"   Details: {e}")
        print()
        print("💡 Make sure 'gui' folder exists with app.py")
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
        print("💡 For help, see: https://github.com/Aryankaushik541/Zarves/blob/main/FIXES.md")

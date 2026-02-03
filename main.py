#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Autonomous AI Assistant with Self-Healing + Auto-Install + Voice Mode
Fully autonomous operation with auto-detection and error recovery
Automatically installs missing dependencies on startup
Natural Indian Language Support - Koi bhi admi bole, JARVIS samajh jayega!
Voice Mode - Talk naturally, no typing needed!
"""

import sys
import os

# ============================================================================
# CRITICAL: Qt environment setup MUST be before ANY imports
# This suppresses Qt DPI warnings on Windows
# ============================================================================
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
os.environ['QT_SCALE_FACTOR'] = '1'
os.environ['QT_DEVICE_PIXEL_RATIO'] = '0'

# Suppress Python warnings
import warnings
warnings.filterwarnings("ignore")

# Now safe to import other modules
import threading 
import time
import subprocess
from dotenv import load_dotenv
from core.self_healing import self_healing

# Auto-detect mode based on environment
AUTO_TEXT_MODE = False
AUTO_DEBUG_MODE = True  # Always log errors for self-healing

# Load Env with error handling
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  Error loading .env: {e}")
    self_healing.auto_fix_error(e, ".env loading")


def auto_install_package(package_name):
    """Automatically install a missing package"""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "-q"])
        print(f"✅ {package_name} installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False


def auto_install_from_requirements():
    """Install all packages from requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("⚠️  requirements.txt not found")
        return False
    
    try:
        print("📦 Installing all dependencies from requirements.txt...")
        print("   This may take a few minutes on first run...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✅ All dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to install from requirements.txt: {e}")
        return False


def auto_fix_missing_imports():
    """Automatically detect and fix missing imports"""
    print("\n" + "="*70)
    print("🔧 JARVIS Auto-Dependency Installer")
    print("="*70)
    print()
    
    # Core required packages with their import names and pip names
    required_packages = {
        'ollama': 'ollama',
        'selenium': 'selenium',
        'bs4': 'beautifulsoup4',
        'requests': 'requests',
        'pywhatkit': 'pywhatkit',
        'webdriver_manager': 'webdriver-manager',
        'speech_recognition': 'SpeechRecognition',
        'pyttsx3': 'pyttsx3',
        'dotenv': 'python-dotenv',
    }
    
    # Optional packages (won't block startup)
    optional_packages = {
        'PyQt5': 'PyQt5',
        'cv2': 'opencv-python',
        'pyautogui': 'pyautogui',
    }
    
    missing_required = []
    missing_optional = []
    
    # Check required packages
    print("🔍 Checking required packages...")
    for import_name, pip_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"   ✅ {pip_name}")
        except ImportError:
            print(f"   ❌ {pip_name} - MISSING")
            missing_required.append(pip_name)
    
    print()
    
    # Check optional packages
    print("🔍 Checking optional packages...")
    for import_name, pip_name in optional_packages.items():
        try:
            __import__(import_name)
            print(f"   ✅ {pip_name}")
        except ImportError:
            print(f"   ⚠️  {pip_name} - OPTIONAL (not required)")
            missing_optional.append(pip_name)
    
    print()
    
    # Install missing required packages
    if missing_required:
        print(f"📦 Found {len(missing_required)} missing required package(s)")
        print("🔧 Auto-installing missing packages...")
        print()
        
        # Try installing from requirements.txt first (faster)
        print("📋 Installing from requirements.txt...")
        if auto_install_from_requirements():
            print("✅ All packages installed from requirements.txt!")
            return True
        else:
            # Fallback: install individually
            print("⚠️  requirements.txt failed, installing individually...")
            for package in missing_required:
                auto_install_package(package)
            return True
    else:
        print("✅ All required packages are installed!")
        return False


def check_ollama():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama...")
    
    # Check if ollama command exists
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ Ollama installed: {version}")
        else:
            print("   ❌ Ollama not found")
            print()
            print("💡 Install Ollama:")
            print("   Windows: https://ollama.com/download/windows")
            print("   Mac: brew install ollama")
            print("   Linux: curl -fsSL https://ollama.com/install.sh | sh")
            print()
            return False
    except FileNotFoundError:
        print("   ❌ Ollama not found")
        print()
        print("💡 Install Ollama:")
        print("   Windows: https://ollama.com/download/windows")
        print("   Mac: brew install ollama")
        print("   Linux: curl -fsSL https://ollama.com/install.sh | sh")
        print()
        return False
    except Exception as e:
        print(f"   ⚠️  Could not check Ollama: {e}")
        return False
    
    # Check if llama3.2 model is available
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if 'llama3.2' in result.stdout:
            print("   ✅ llama3.2 model found")
            return True
        else:
            print("   ⚠️  llama3.2 model not found")
            print()
            print("📥 Pulling llama3.2 model...")
            print("   This may take a few minutes (one-time download)...")
            try:
                subprocess.run(['ollama', 'pull', 'llama3.2'], timeout=300)
                print("   ✅ Model downloaded successfully!")
                return True
            except Exception as e:
                print(f"   ❌ Failed to pull model: {e}")
                print()
                print("💡 Manually pull model:")
                print("   ollama pull llama3.2")
                print()
                return False
    except Exception as e:
        print(f"   ⚠️  Could not check models: {e}")
        return False


def auto_create_env_file():
    """Automatically create .env file from template"""
    if os.path.exists('.env'):
        return True
    
    if not os.path.exists('.env.template'):
        print("⚠️  .env.template not found")
        return False
    
    try:
        print("🔧 Creating .env file from template...")
        with open('.env.template', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created")
        print("💡 Optional: Configure Ollama settings in .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env: {e}")
        return False


def run_startup_checks():
    """
    Run automatic startup checks and fixes.
    Automatically installs missing dependencies without user intervention.
    """
    print("\n" + "="*70)
    print("🤖 JARVIS Startup Checks")
    print("="*70)
    print()
    
    # Check and install dependencies
    deps_installed = auto_fix_missing_imports()
    
    # Check Ollama
    ollama_ok = check_ollama()
    
    # Create .env if needed
    auto_create_env_file()
    
    print("="*70)
    
    if deps_installed:
        print()
        print("🔄 Dependencies were installed. Please restart JARVIS:")
        print("   python main.py")
        print()
        sys.exit(0)
    
    if not ollama_ok:
        print()
        print("⚠️  Ollama setup incomplete. Please:")
        print("   1. Install Ollama")
        print("   2. Run: ollama serve")
        print("   3. Run: ollama pull llama3.2")
        print("   4. Restart JARVIS")
        print()
        
        # Ask if user wants to continue anyway
        try:
            response = input("Continue anyway? (y/n): ").lower()
            if response != 'y':
                sys.exit(0)
        except:
            pass
    
    print()
    print("✅ Startup checks complete!")
    print()


# Run startup checks before importing skills
run_startup_checks()

# Now import skills (after dependencies are installed)
try:
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from core.voice import listen, speak
except ImportError as e:
    print(f"❌ Failed to load core modules: {e}")
    print("🔧 Attempting to fix...")
    auto_install_from_requirements()
    print()
    print("🔄 Please restart JARVIS:")
    print("   python main.py")
    sys.exit(1)


def main():
    """Main entry point for JARVIS"""
    print("\n" + "="*70)
    print("🤖 JARVIS - Your Personal AI Assistant")
    print("="*70)
    print()
    print("💡 Features:")
    print("   • Voice Mode - Talk naturally, no typing!")
    print("   • Natural Conversations - Like talking to a friend")
    print("   • Emotion Detection - Understands your mood")
    print("   • Context Memory - Remembers previous tasks")
    print("   • YouTube Auto-Music - 'youtube kholo' plays trending songs")
    print("   • Movie Downloader - 'vegamovies se Inception download karo'")
    print("   • And much more!")
    print()
    print("="*70)
    print()
    
    # Initialize registry and engine
    try:
        print("🔧 Initializing JARVIS...")
        registry = SkillRegistry()
        
        # Load all skills from skill directory
        print("📦 Loading skills...")
        try:
            skills_dir = os.path.join(os.path.dirname(__file__), 'skill')
            registry.load_skills(skills_dir)
            print(f"✅ Loaded {len(registry.skills)} skills")
        except Exception as e:
            print(f"❌ Failed to load skills: {e}")
            print("🔧 Attempting to fix import error...")
            
            # Try to auto-fix
            if "selenium" in str(e).lower():
                print("📦 selenium नहीं मिला। Auto-install कर रहा हूँ...")
                auto_install_package("selenium")
                auto_install_package("webdriver-manager")
                print()
                print("✅ selenium installed! Please restart JARVIS:")
                print("   python main.py")
                sys.exit(0)
            elif "pywhatkit" in str(e).lower():
                print("📦 pywhatkit नहीं मिला। Auto-install कर रहा हूँ...")
                auto_install_package("pywhatkit")
                print()
                print("✅ pywhatkit installed! Please restart JARVIS:")
                print("   python main.py")
                sys.exit(0)
            else:
                # Generic fix - install all from requirements
                print("📦 Installing all dependencies...")
                auto_install_from_requirements()
                print()
                print("✅ Dependencies installed! Please restart JARVIS:")
                print("   python main.py")
                sys.exit(0)
        
        # Initialize engine
        print("🧠 Initializing AI engine...")
        engine = JarvisEngine(registry)
        print("✅ JARVIS ready!")
        print()
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        self_healing.auto_fix_error(e, "JARVIS initialization")
        sys.exit(1)
    
    # Ask user for mode preference
    print("="*70)
    print("🎙️  Choose Mode:")
    print("="*70)
    print()
    print("1. 🎤 Voice Mode (Recommended) - Talk naturally")
    print("2. ⌨️  Text Mode - Type commands")
    print()
    
    mode_choice = input("Enter choice (1 or 2, default=1): ").strip()
    
    if mode_choice == "2":
        # Text mode
        use_voice = False
        print()
        print("="*70)
        print("⌨️  Text Mode Activated")
        print("="*70)
        print()
        print("💬 Try these natural commands:")
        print("   • 'hello jarvis'")
        print("   • 'gaana bajao' (auto-plays trending music)")
        print("   • 'youtube kholo'")
        print("   • 'volume badhao'")
        print("   • 'vegamovies se Inception download karo'")
        print("   • 'thanks!' (see empathetic response)")
        print()
        print("Type 'quit' or 'exit' to stop")
        print("="*70)
        print()
    else:
        # Voice mode (default)
        use_voice = True
        print()
        print("="*70)
        print("🎤 Voice Mode Activated")
        print("="*70)
        print()
        print("💬 How to use:")
        print("   1. Say 'Jarvis' to activate")
        print("   2. Then give your command")
        print("   3. JARVIS will respond with voice")
        print()
        print("💡 Examples:")
        print("   • 'Jarvis, gaana bajao'")
        print("   • 'Jarvis, youtube kholo'")
        print("   • 'Jarvis, volume badhao'")
        print()
        print("Say 'stop listening' or 'exit' to quit")
        print("="*70)
        print()
        
        # Initial greeting
        speak("Hello! I'm JARVIS. Say my name followed by your command.")
    
    # Main conversation loop
    while True:
        try:
            if use_voice:
                # Voice mode
                user_input = listen()
                
                if user_input == "none":
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'alvida', 'stop listening']:
                    speak("Goodbye! Have a great day!")
                    break
                
                # Process query with personal assistant
                response = engine.process_query(user_input)
                speak(response)
                
            else:
                # Text mode
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'alvida']:
                    print("\n🤖 JARVIS: Goodbye! Have a great day! 👋")
                    break
                
                # Process query with personal assistant
                print("\n🤖 JARVIS: ", end="", flush=True)
                response = engine.process_query(user_input)
                print(response)
            
        except KeyboardInterrupt:
            if use_voice:
                speak("Goodbye! Have a great day!")
            else:
                print("\n\n🤖 JARVIS: Goodbye! Have a great day! 👋")
            break
        except Exception as e:
            error_msg = f"Error: {e}"
            if use_voice:
                speak("Sorry, I encountered an error. Please try again.")
            else:
                print(f"\n⚠️  {error_msg}")
            
            # Try to auto-fix
            if self_healing.auto_fix_error(e, f"Processing query: {user_input}"):
                retry_msg = "Let me try that again..."
                if use_voice:
                    speak(retry_msg)
                else:
                    print(f"🔄 {retry_msg}")
                
                try:
                    response = engine.process_query(user_input)
                    if use_voice:
                        speak(response)
                    else:
                        print(f"\n🤖 JARVIS: {response}")
                except:
                    fail_msg = "Still having trouble. Please try rephrasing."
                    if use_voice:
                        speak(fail_msg)
                    else:
                        print(f"❌ {fail_msg}")
            else:
                if not use_voice:
                    print("💡 Please try rephrasing your request.")


if __name__ == "__main__":
    main()

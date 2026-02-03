#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Autonomous AI Assistant with Self-Healing + Auto-Install
Fully autonomous operation with auto-detection and error recovery
Automatically installs missing dependencies on startup
Natural Indian Language Support - Koi bhi admi bole, JARVIS samajh jayega!
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
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_required.append(package)
    
    # Check optional packages
    print("\n🔍 Checking optional packages...")
    for module, package in optional_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️  {package} - MISSING (optional)")
            missing_optional.append(package)
    
    print()
    
    # Install missing required packages
    if missing_required:
        print(f"📦 Found {len(missing_required)} missing required package(s)")
        print("🔧 Auto-installing missing packages...")
        print()
        
        # Try installing from requirements.txt first (faster)
        if os.path.exists('requirements.txt'):
            print("📋 Installing from requirements.txt...")
            if auto_install_from_requirements():
                print("✅ All packages installed from requirements.txt!")
                return True
        
        # Fallback: Install individually
        print("📦 Installing packages individually...")
        for package in missing_required:
            auto_install_package(package)
        
        print()
        print("✅ Dependency installation complete!")
        print("🔄 Please restart JARVIS for changes to take effect")
        print()
        return True
    
    elif missing_optional:
        print(f"⚠️  {len(missing_optional)} optional package(s) missing")
        print("💡 Install for additional features:")
        for package in missing_optional:
            print(f"   pip install {package}")
        print()
    
    else:
        print("✅ All required packages are installed!")
        print()
    
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
            print(f"   ✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("   ❌ Ollama not found")
            print()
            print("📥 Please install Ollama:")
            print("   Windows: https://ollama.com/download/windows")
            print("   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh")
            print()
            return False
    except FileNotFoundError:
        print("   ❌ Ollama not found")
        print()
        print("📥 Please install Ollama:")
        print("   Windows: https://ollama.com/download/windows")
        print("   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh")
        print()
        return False
    except Exception as e:
        print(f"   ⚠️  Could not check Ollama: {e}")
        return False
    
    # Check if model is pulled
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
        print("   See OLLAMA_SETUP.md for details")
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
    print("🤖 JARVIS - Your Autonomous AI Assistant")
    print("="*70)
    print()
    print("💡 Features:")
    print("   • YouTube Auto-Music - 'youtube kholo' plays trending songs")
    print("   • Movie Downloader - 'vegamovies se Inception download karo'")
    print("   • Web Search - 'google search python'")
    print("   • System Control - 'volume badhao', 'brightness kam karo'")
    print("   • And much more!")
    print()
    print("="*70)
    print()
    
    # Initialize registry and engine
    try:
        print("🔧 Initializing JARVIS...")
        registry = SkillRegistry()
        
        # Load all skills
        print("📦 Loading skills...")
        try:
            registry.load_all_skills()
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
    
    # Start JARVIS
    print("="*70)
    print("🎤 JARVIS is listening...")
    print("="*70)
    print()
    print("💬 Try these commands:")
    print("   • 'hello jarvis'")
    print("   • 'youtube kholo' (auto-plays trending music)")
    print("   • 'gaana bajao'")
    print("   • 'google search python'")
    print("   • 'vegamovies se Inception download karo'")
    print()
    print("Type 'quit' or 'exit' to stop")
    print("="*70)
    print()
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 JARVIS: Goodbye! Have a great day!")
                break
            
            # Process query
            print("\n🤖 JARVIS: ", end="", flush=True)
            response = engine.process_query(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 JARVIS: Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if self_healing.auto_fix_error(e, f"Processing: {user_input}"):
                print("✅ Error fixed! Continuing...")
            else:
                print("⚠️  Continuing despite error...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Complete AI Assistant
Beautiful GUI Interface - Auto-Launch
Just run: python main.py
"""

import sys
import os
import subprocess

# ============================================================================
# AUTO-INSTALL DEPENDENCIES
# ============================================================================

def auto_install_dependencies():
    """Auto-install missing packages"""
    print("\n" + "="*70)
    print("🤖 JARVIS - Initializing...")
    print("="*70)
    print()
    
    required = {
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
        'pyautogui': 'pyautogui',
        'psutil': 'psutil',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📦 Installing {len(missing)} missing packages...")
        print()
        for package in missing:
            print(f"   ⏳ Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
                print(f"   ✅ {package} installed!")
            except:
                print(f"   ⚠️  {package} installation failed (optional)")
        print()
        print("✅ Dependencies ready!")
        print()
    
    return True

# ============================================================================
# MAIN - AUTO-LAUNCH GUI
# ============================================================================

def main():
    """Main entry point - Auto-launches GUI"""
    
    # Install dependencies
    auto_install_dependencies()
    
    # Launch GUI
    print("🚀 Launching JARVIS GUI...")
    print()
    print("💡 GUI Features:")
    print("   ✅ Beautiful visual interface")
    print("   ✅ Quick action buttons (Gmail, Facebook, YouTube, etc.)")
    print("   ✅ Voice & text input")
    print("   ✅ Full PC control")
    print("   ✅ Real-time status")
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
        print("   pip install pyttsx3 SpeechRecognition pyautogui psutil")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")

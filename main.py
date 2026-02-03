#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Complete AI Assistant
Auto-launches beautiful GUI interface
No terminal needed!
"""

import sys
import os
import subprocess

# ============================================================================
# AUTO-INSTALL DEPENDENCIES
# ============================================================================

def auto_install_dependencies():
    """Auto-install missing packages"""
    required = {
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
        'pyautogui': 'pyautogui',
        'psutil': 'psutil',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n📦 Installing {len(missing)} missing packages...")
        for package in missing:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        print("✅ All dependencies installed!\n")
        return True
    return False

# ============================================================================
# MAIN LAUNCHER
# ============================================================================

def main():
    """Main entry point - launches GUI"""
    
    print("\n" + "="*70)
    print("🤖 JARVIS - Your Personal AI Assistant")
    print("="*70)
    print()
    
    # Install dependencies if needed
    if auto_install_dependencies():
        print("🔄 Dependencies installed! Launching GUI...")
        print()
    
    # Launch GUI
    print("🚀 Launching JARVIS GUI...")
    print()
    print("💡 GUI Features:")
    print("   ✅ Beautiful visual interface")
    print("   ✅ Quick action buttons")
    print("   ✅ Voice & text input")
    print("   ✅ Web support (Gmail, Facebook, YouTube, etc.)")
    print("   ✅ Full PC control")
    print()
    print("="*70)
    print()
    
    try:
        # Import and run GUI
        from gui.app import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print()
        print("💡 Try running directly:")
        print("   python run_gui.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Try installing dependencies:")
        print("   pip install pyttsx3 SpeechRecognition pyautogui psutil")


if __name__ == "__main__":
    main()

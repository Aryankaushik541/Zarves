#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI Launcher
Simple launcher for JARVIS GUI interface
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run GUI
from gui.app import main

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖 JARVIS GUI - Starting...")
    print("="*70)
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Try installing dependencies:")
        print("   pip install pyttsx3 SpeechRecognition pyautogui psutil")

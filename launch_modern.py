#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS Modern GUI Launcher
Quick launcher for the enhanced modern interface
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🤖 JARVIS - Modern AI Assistant")
print("=" * 70)
print()

# Check dependencies
print("📦 Checking dependencies...")
try:
    import tkinter
    print("   ✅ tkinter available")
except ImportError:
    print("   ❌ tkinter not found")
    print("   💡 Install: sudo apt-get install python3-tk (Linux)")
    sys.exit(1)

try:
    import requests
    print("   ✅ requests available")
except ImportError:
    print("   ⚠️  Installing requests...")
    os.system(f"{sys.executable} -m pip install requests")

try:
    import pyttsx3
    print("   ✅ pyttsx3 available")
except ImportError:
    print("   ⚠️  Installing pyttsx3...")
    os.system(f"{sys.executable} -m pip install pyttsx3")

try:
    import speech_recognition
    print("   ✅ speech_recognition available")
except ImportError:
    print("   ⚠️  Installing speech_recognition...")
    os.system(f"{sys.executable} -m pip install SpeechRecognition")

print()
print("🚀 Launching Modern GUI...")
print()

# Import and run modern GUI
try:
    from gui.modern_app import main
    main()
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    print()
    print("💡 Troubleshooting:")
    print("   1. Make sure Ollama is running: ollama serve")
    print("   2. Check if all dependencies are installed")
    print("   3. Try running: python main.py")
    sys.exit(1)

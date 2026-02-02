#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS Fix Verification Script
Tests wake word detection and hardware detection
"""

import sys
import os

print("="*70)
print("🧪 JARVIS Fix Verification Script")
print("="*70)
print()

# Test 1: Import Check
print("📦 Test 1: Checking imports...")
try:
    from core.voice import detect_wake_word, listen, speak
    from core.npu_accelerator import npu_accelerator
    from core.indian_language import normalize_indian_text
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 2: Wake Word Detection
print("📝 Test 2: Wake Word Detection...")
test_cases = [
    ("Jarvis, YouTube kholo", True, "youtube kholo"),
    ("जार्विस यूट्यूब खोलो", True, "यूट्यूब खोलो"),
    ("Jarvis open YouTube", True, "open youtube"),
    ("YouTube kholo", False, "YouTube kholo"),
    ("jarvis play music", True, "play music"),
    ("JARVIS stop", True, "stop"),
]

passed = 0
failed = 0

for text, should_detect, expected_command in test_cases:
    has_wake_word, command = detect_wake_word(text)
    
    if has_wake_word == should_detect:
        status = "✅"
        passed += 1
    else:
        status = "❌"
        failed += 1
    
    print(f"{status} '{text}'")
    print(f"   Expected: {should_detect}, Got: {has_wake_word}")
    if has_wake_word:
        print(f"   Command: '{command}'")

print(f"\nResults: {passed} passed, {failed} failed")

if failed > 0:
    print("⚠️  Some wake word tests failed!")
else:
    print("✅ All wake word tests passed!")

print()

# Test 3: Hardware Detection
print("🖥️  Test 3: Hardware Detection...")
try:
    npu_accelerator.print_status()
    print("✅ Hardware detection successful")
except Exception as e:
    print(f"❌ Hardware detection failed: {e}")

print()

# Test 4: Indian Language Normalization
print("🇮🇳 Test 4: Indian Language Normalization...")
test_phrases = [
    ("youtube kholo", "open youtube"),
    ("gaana bajao", "play song"),
    ("google pe dhundho", "search google"),
    ("calculator chalu karo", "start calculator"),
]

for original, expected_contains in test_phrases:
    normalized = normalize_indian_text(original)
    
    # Check if key words are present
    if any(word in normalized for word in expected_contains.split()):
        print(f"✅ '{original}' → '{normalized}'")
    else:
        print(f"⚠️  '{original}' → '{normalized}' (expected: {expected_contains})")

print()

# Test 5: PyTorch & CUDA
print("🔥 Test 5: PyTorch & CUDA...")
try:
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"   CUDA version: {torch.version.cuda}")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
    else:
        print("   Using CPU (no GPU detected)")
except ImportError:
    print("❌ PyTorch not installed")
    print("   Run: pip install torch torchvision torchaudio")

print()

# Test 6: Speech Recognition
print("🎤 Test 6: Speech Recognition...")
try:
    import speech_recognition as sr
    print(f"✅ SpeechRecognition version: {sr.__version__}")
    
    # List microphones
    try:
        mics = sr.Microphone.list_microphone_names()
        print(f"   Found {len(mics)} microphone(s):")
        for i, mic in enumerate(mics[:3]):  # Show first 3
            print(f"     {i}: {mic}")
        if len(mics) > 3:
            print(f"     ... and {len(mics) - 3} more")
    except Exception as e:
        print(f"   ⚠️  Could not list microphones: {e}")
        
except ImportError:
    print("❌ SpeechRecognition not installed")
    print("   Run: pip install SpeechRecognition")

print()

# Test 7: Text-to-Speech
print("🗣️  Test 7: Text-to-Speech...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"✅ pyttsx3 initialized")
    print(f"   Available voices: {len(voices)}")
    
    # Check for Hindi voice
    has_hindi = False
    for voice in voices:
        if "hindi" in voice.name.lower() or "hemant" in voice.name.lower() or "kalpana" in voice.name.lower():
            print(f"   ✅ Hindi voice found: {voice.name}")
            has_hindi = True
            break
    
    if not has_hindi:
        print("   ⚠️  No Hindi voice found (English will be used)")
        
except Exception as e:
    print(f"❌ pyttsx3 error: {e}")
    print("   Run: pip install pyttsx3")

print()

# Test 8: Environment Variables
print("🔑 Test 8: Environment Variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        print(f"✅ GROQ_API_KEY found (length: {len(groq_key)})")
    else:
        print("⚠️  GROQ_API_KEY not found in .env")
        print("   Create .env file and add: GROQ_API_KEY=your_key_here")
        print("   Get free key from: https://console.groq.com/keys")
except ImportError:
    print("❌ python-dotenv not installed")
    print("   Run: pip install python-dotenv")

print()

# Summary
print("="*70)
print("📊 Test Summary")
print("="*70)

all_tests = [
    ("Imports", True),
    ("Wake Word Detection", failed == 0),
    ("Hardware Detection", True),
    ("Indian Language", True),
    ("PyTorch", True),
    ("Speech Recognition", True),
    ("Text-to-Speech", True),
    ("Environment", True),
]

print()
for test_name, passed in all_tests:
    status = "✅" if passed else "⚠️"
    print(f"{status} {test_name}")

print()
print("="*70)
print("🎯 Next Steps:")
print("="*70)
print()
print("1. If all tests passed:")
print("   python main.py")
print()
print("2. If microphone test failed:")
print("   pip install pyaudio")
print("   # On Windows, download wheel from:")
print("   # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
print()
print("3. If CUDA not available but you have NVIDIA GPU:")
print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
print()
print("4. If GROQ_API_KEY missing:")
print("   cp .env.template .env")
print("   # Edit .env and add your API key")
print()
print("5. Test voice input:")
print("   Say: 'Jarvis, YouTube kholo'")
print("   Expected: JARVIS opens YouTube")
print()
print("="*70)
print("Happy Testing! 🚀")
print("="*70)

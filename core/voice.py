import os
import sys
import pyttsx3
import speech_recognition as sr
import re
import time

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Wake word variations - supports Hindi, English, and common misspellings
WAKE_WORDS = [
    "jarvis",      # English
    "जार्विस",     # Hindi Devanagari
    "jarwis",      # Common misspelling
    "jaarvis",     # Common variation
]

# Global state for continuous listening
continuous_mode = False
last_command_time = 0
CONTINUOUS_TIMEOUT = 30  # 30 seconds of inactivity exits continuous mode

def detect_wake_word(text):
    """
    Detect wake word in both Hindi and English
    Returns: (has_wake_word, cleaned_command)
    """
    if not text:
        return False, ""
    
    text_lower = text.lower().strip()
    
    # Check for Hindi Devanagari "जार्विस"
    if "जार्विस" in text:
        # Remove wake word and return command
        command = text.replace("जार्विस", "").strip()
        return True, command
    
    # Check for English variations
    for wake_word in WAKE_WORDS:
        if wake_word in text_lower:
            # Remove wake word and return command
            # Use regex to remove wake word (case-insensitive)
            command = re.sub(r'\b' + wake_word + r'\b', '', text_lower, flags=re.IGNORECASE).strip()
            return True, command
    
    return False, text

def is_exit_command(text):
    """Check if user wants to exit continuous mode"""
    exit_commands = [
        "stop listening", "band karo", "bas", "enough", 
        "exit", "quit", "sleep", "so jao", "chup raho",
        "stop", "band", "ruk jao"
    ]
    text_lower = text.lower().strip()
    return any(cmd in text_lower for cmd in exit_commands)

# Set voice to deep male voice with Hindi support (cross-platform)
def set_deep_male_voice():
    voices = engine.getProperty('voices')
    
    # Platform-specific voice selection
    if sys.platform == "darwin":  # macOS
        # Try Hindi voice first (Lekha on macOS)
        for voice in voices:
            if "lekha" in voice.name.lower() or "hindi" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)  # Adjust speed
                return
        # Fallback to Daniel for deep male voice
        for voice in voices:
            if "daniel" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)
                return
    
    elif sys.platform == "win32":  # Windows
        # Try Hindi voice first (Microsoft Hemant or Kalpana)
        for voice in voices:
            if "hemant" in voice.name.lower() or "kalpana" in voice.name.lower() or "hindi" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)
                return
        # Fallback to David or Zira (English voices on Windows)
        for voice in voices:
            if "david" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)
                return
    
    # Generic fallback for any platform
    for voice in voices:
        if "hindi" in voice.name.lower() or "hi" in str(voice.languages).lower():
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 150)
            return
    
    # Final fallback to any male voice
    for voice in voices:
        if "male" in voice.name.lower() or "male" in str(voice.gender).lower():
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 150)
            return
    
    # If nothing found, use first available voice
    if voices:
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)

set_deep_male_voice()

def speak(text):
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
    
    # Print first so user sees it even if audio fails
    print(f"JARVIS: {text}")

    # Platform-specific TTS handling
    if sys.platform == "darwin":  # macOS
        try:
            # Escape quotes to prevent shell injection/errors
            clean_text = text.replace('"', '\\"').replace("'", "")
            # Try Hindi voice (Lekha), fallback to default
            result = os.system(f'say -v Lekha "{clean_text}" 2>/dev/null')
            if result == 0:
                return
            # Fallback to default voice if Lekha not available
            os.system(f'say "{clean_text}"')
            return
        except Exception as e:
            print(f"macOS TTS Error: {e}")
            # Fall through to pyttsx3
    
    elif sys.platform == "win32":  # Windows
        # Use pyttsx3 directly on Windows (works better than system commands)
        try:
            engine.say(text)
            engine.runAndWait()
            return
        except Exception as e:
            print(f"Windows TTS Error: {e}")
    
    # Generic fallback for Linux or other platforms
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def listen():
    """
    Listen for voice input with continuous mode support
    - First time: Requires wake word "Jarvis"
    - After wake word: Enters continuous mode for 30 seconds
    - In continuous mode: No wake word needed
    - Exit continuous mode: Say "stop listening" or wait 30 seconds
    
    Returns: command text or "none"
    """
    global continuous_mode, last_command_time
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Check if continuous mode timed out
        if continuous_mode and (time.time() - last_command_time) > CONTINUOUS_TIMEOUT:
            continuous_mode = False
            print("⏰ Continuous mode timed out. Say 'Jarvis' to activate again.")
        
        if continuous_mode:
            print("🎤 Listening (continuous mode - no wake word needed)...")
        else:
            print("Listening...")
        
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            
            recognized_text = None
            
            # Try Hindi recognition first, fallback to English
            try:
                query = r.recognize_google(audio, language='hi-IN')
                print(f"Hindi: {query}")
                recognized_text = query
            except:
                try:
                    query = r.recognize_google(audio, language='en-IN')
                    print(f"English: {query}")
                    recognized_text = query
                except:
                    # Final fallback to US English
                    try:
                        query = r.recognize_google(audio, language='en-US')
                        print(f"English (US): {query}")
                        recognized_text = query
                    except:
                        pass
            
            if not recognized_text:
                return "none"
            
            # Check for exit command in continuous mode
            if continuous_mode and is_exit_command(recognized_text):
                continuous_mode = False
                print("✅ Exiting continuous mode. Say 'Jarvis' to activate again.")
                speak("Continuous mode deactivated.")
                return "none"
            
            # Check for wake word
            has_wake_word, command = detect_wake_word(recognized_text)
            
            if continuous_mode:
                # In continuous mode, accept any command
                last_command_time = time.time()
                
                # If wake word is present, remove it
                if has_wake_word and command:
                    print(f"✅ Command: {command}")
                    return command.lower()
                else:
                    # No wake word, but in continuous mode - accept full text
                    print(f"✅ Command: {recognized_text}")
                    return recognized_text.lower()
            
            else:
                # Not in continuous mode - require wake word
                if has_wake_word:
                    # Activate continuous mode
                    continuous_mode = True
                    last_command_time = time.time()
                    
                    if command:
                        print(f"✅ Continuous mode activated! Command: {command}")
                        print("💡 Ab aap bina 'Jarvis' bole commands de sakte ho (30 sec tak)")
                        return command.lower()
                    else:
                        # Wake word detected but no command
                        print("✅ Continuous mode activated! Waiting for command...")
                        print("💡 Ab aap bina 'Jarvis' bole commands de sakte ho (30 sec tak)")
                        speak("Continuous mode activated. I'm listening.")
                        return "none"
                else:
                    # No wake word detected
                    print(f"Ignored (no wake word): {recognized_text}")
                    print("💡 Tip: Say 'Jarvis' pehle, phir command")
                    return "none"
            
        except sr.WaitTimeoutError:
            if continuous_mode:
                print("Timeout in continuous mode...")
            else:
                print("Timeout: No voice detected")
            return "none"
        except sr.UnknownValueError:
            print("Could not understand")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"

def reset_continuous_mode():
    """Reset continuous mode (useful for testing or manual reset)"""
    global continuous_mode, last_command_time
    continuous_mode = False
    last_command_time = 0
    print("✅ Continuous mode reset")

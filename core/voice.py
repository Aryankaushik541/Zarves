import os
import sys
import pyttsx3
import speech_recognition as sr
import re

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Wake word variations - supports Hindi, English, and common misspellings
WAKE_WORDS = [
    "jarvis",      # English
    "जार्विस",     # Hindi Devanagari
    "jarwis",      # Common misspelling
    "jaarvis",     # Common variation
]

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
    Listen for voice input with wake word detection
    Supports both Hindi and English
    Returns: command text (without wake word) or "none"
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
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
            
            # Check for wake word
            has_wake_word, command = detect_wake_word(recognized_text)
            
            if has_wake_word:
                if command:
                    print(f"✅ Command detected: {command}")
                    return command.lower()
                else:
                    # Wake word detected but no command
                    print("💡 Wake word detected. Waiting for command...")
                    return "none"
            else:
                # No wake word detected
                print(f"Ignored (no wake word): {recognized_text}")
                print("💡 Tip: Say 'Jarvis' pehle, phir command")
                return "none"
            
        except sr.WaitTimeoutError:
            print("Timeout: No voice detected")
            return "none"
        except sr.UnknownValueError:
            print("Could not understand")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"

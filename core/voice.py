import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

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
        text = "कार्य पूर्ण हुआ।"
    
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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("सुन रहा हूँ... (Listening...)")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("पहचान रहा हूँ... (Recognizing...)")
            
            # Try Hindi recognition first, fallback to English
            try:
                query = r.recognize_google(audio, language='hi-IN')
                print(f"Hindi: {query}")
            except:
                try:
                    query = r.recognize_google(audio, language='en-IN')
                    print(f"English: {query}")
                except:
                    # Final fallback to US English
                    query = r.recognize_google(audio, language='en-US')
                    print(f"English (US): {query}")
            
            return query.lower()
        except sr.WaitTimeoutError:
            print("Timeout: कोई आवाज़ नहीं सुनाई दी")
            return "none"
        except sr.UnknownValueError:
            print("समझ नहीं आया (Could not understand)")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"

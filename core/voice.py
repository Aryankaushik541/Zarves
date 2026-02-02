import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Set voice to deep male voice with Hindi support
def set_deep_male_voice():
    voices = engine.getProperty('voices')
    # Try to find Hindi voice first
    for voice in voices:
        if "hindi" in voice.name.lower() or "hi" in voice.languages:
            engine.setProperty('voice', voice.id)
            return
    # Fallback to Daniel for deep male voice on Mac
    for voice in voices:
        if "Daniel" in voice.name:
            engine.setProperty('voice', voice.id)
            return
    # Fallback to any male voice if Daniel not found
    for voice in voices:
        if "male" in voice.name.lower() or "male" in str(voice.gender).lower():
             engine.setProperty('voice', voice.id)
             return

set_deep_male_voice()

def speak(text):
    if "{" in text and "}" in text and "status" in text:
        text = "कार्य पूर्ण हुआ।"
    
    # Print first so user sees it even if audio fails
    print(f"JARVIS: {text}")

    # On macOS with a GUI/Threading environment, pyttsx3's loop often conflicts 
    # with the main thread event loop (PyQt). Default to system 'say' command on macOS
    # to avoid hangs/crashes unless we are strictly in a non-GUI text mode.
    if sys.platform == "darwin":
        try:
            # Escape quotes to prevent shell injection/errors
            clean_text = text.replace('"', '\\"').replace("'", "")
            # Use Hindi voice on macOS if available
            os.system(f'say -v Lekha "{clean_text}"')
            return
        except Exception as e2:
            print(f"TTS Fallback Error: {e2}")
            # Fall through to pyttsx3 if 'say' fails (unlikely)

    # Try pyttsx3
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("सुन रहा हूँ...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            print("पहचान रहा हूँ...")
            # Try Hindi recognition first, fallback to English
            try:
                query = r.recognize_google(audio, language='hi-IN')
            except:
                query = r.recognize_google(audio, language='en-IN')
            return query.lower()
        except Exception:
            return "none"

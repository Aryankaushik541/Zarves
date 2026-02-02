#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Autonomous AI Assistant with Self-Healing + NPU Acceleration
Fully autonomous operation with auto-detection and error recovery
Optimized for Omen PC with NPU support
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

# Import with self-healing
try:
    from core.voice import speak, listen
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from gui.app import run_gui as run_gui_app
    from core.npu_accelerator import npu_accelerator
except ImportError as e:
    print(f"⚠️  Import error detected: {e}")
    if self_healing.auto_fix_error(e, "Initial imports"):
        print("✅ Dependencies fixed! Please restart the application.")
        print("   python main.py")
        sys.exit(0)
    else:
        print("❌ Critical import error. Auto-installing dependencies...")
        print("   Please wait...")
        sys.exit(1)

# Check API key
if not os.environ.get("GROQ_API_KEY"):
    print("⚠️  GROQ_API_KEY not found.")
    if not self_healing.fix_api_key_error():
        print("❌ Please set GROQ_API_KEY in .env file")
        sys.exit(1)


class AutoMode:
    """Automatically detect best mode for running JARVIS"""
    
    @staticmethod
    def detect_voice_available():
        """Check if voice/microphone is available"""
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            # Try to access microphone
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except Exception as e:
            print(f"🎤 Voice input not available: {e}")
            return False
    
    @staticmethod
    def detect_gui_available():
        """Check if GUI can run"""
        try:
            from PyQt5.QtWidgets import QApplication
            # Try to create QApplication
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            return True
        except Exception as e:
            print(f"🖥️  GUI not available: {e}")
            return False
    
    @staticmethod
    def should_use_text_mode():
        """Decide if text mode should be used"""
        # Check if running in non-interactive environment
        if not sys.stdin.isatty():
            return True
        
        # Check if voice is available
        if not AutoMode.detect_voice_available():
            print("📝 Voice input not available. Using text mode.")
            return True
        
        return AUTO_TEXT_MODE
    
    @staticmethod
    def should_use_gui():
        """Decide if GUI should be used"""
        # Check if display is available
        if not os.environ.get('DISPLAY') and sys.platform != 'darwin' and sys.platform != 'win32':
            return False
        
        return AutoMode.detect_gui_available()


def normalize_hindi_command(query):
    """
    Normalize Hindi commands to English equivalents for better detection.
    Handles Devanagari script and transliterated Hindi.
    """
    # Hindi to English command mapping
    hindi_commands = {
        # Devanagari script
        'खोलो': 'open',
        'खोल': 'open',
        'बंद': 'close',
        'बंद करो': 'close',
        'शुरू': 'start',
        'शुरू करो': 'start',
        'बजाओ': 'play',
        'बजा': 'play',
        'रोको': 'stop',
        'रोक': 'stop',
        'ढूंढो': 'search',
        'ढूंढ': 'search',
        'खोजो': 'search',
        'खोज': 'search',
        'बनाओ': 'create',
        'बना': 'create',
        'लिखो': 'write',
        'लिख': 'write',
        'पढ़ो': 'read',
        'पढ़': 'read',
        'मिटाओ': 'delete',
        'मिटा': 'delete',
        'भेजो': 'send',
        'भेज': 'send',
        'युटुब': 'youtube',
        'यूट्यूब': 'youtube',
        'गूगल': 'google',
        'क्रोम': 'chrome',
        'ब्राउज़र': 'browser',
        'म्यूजिक': 'music',
        'संगीत': 'music',
        'गाना': 'song',
        'वीडियो': 'video',
        'फोटो': 'photo',
        'तस्वीर': 'photo',
        
        # Transliterated Hindi (Roman script)
        'karo': 'do',
        'band': 'close',
        'shuru': 'start',
        'bajao': 'play',
        'roko': 'stop',
        'dhundo': 'search',
        'khojo': 'search',
        'banao': 'create',
        'likho': 'write',
        'padho': 'read',
        'mitao': 'delete',
        'bhejo': 'send',
    }
    
    normalized = query.lower()
    
    # Replace Hindi words with English equivalents
    for hindi, english in hindi_commands.items():
        normalized = normalized.replace(hindi, english)
    
    return normalized


def jarvis_loop(pause_event, registry, use_text_mode):
    """
    Main loop for JARVIS with full autonomous operation.
    Automatically handles all errors and mode switching.
    """
    # Initialize Engine with retry
    jarvis = None
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries and jarvis is None:
        try:
            jarvis = JarvisEngine(registry)
        except Exception as e:
            retry_count += 1
            print(f"⚠️  Engine initialization error (attempt {retry_count}/{max_retries})")
            if self_healing.auto_fix_error(e, "JarvisEngine initialization"):
                print("✅ Error fixed! Retrying...")
                continue
            else:
                if retry_count >= max_retries:
                    print("❌ Failed to initialize JARVIS engine")
                    return
                time.sleep(2)
    
    if jarvis is None:
        print("❌ Could not start JARVIS")
        return

    # Startup message
    startup_msg = "Jarvis Online. Ready for command."
    if use_text_mode:
        print(f"JARVIS: {startup_msg}")
        print("💬 Text mode active. Type your commands.")
    else:
        try:
            speak(startup_msg)
            print("🎤 Voice mode active. Say 'Jarvis' followed by your command.")
            print("💡 Tip: Hindi commands bhi kaam karenge! (e.g., 'Jarvis, YouTube kholo')")
        except Exception as e:
            print(f"⚠️  TTS error: {e}")
            self_healing.auto_fix_error(e, "Startup TTS")
            print(f"JARVIS: {startup_msg}")
            use_text_mode = True  # Fallback to text mode

    # Main loop with error recovery
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            # Check for pause
            if pause_event.is_set():
                time.sleep(0.5)
                continue

            # Get user input - auto-detect mode
            if use_text_mode:
                try:
                    user_query = input("YOU: ").lower()
                except EOFError:
                    break
                except KeyboardInterrupt:
                    print("\n⚠️  Keyboard interrupt. Type 'quit' to exit.")
                    continue
            else:
                try:
                    user_query = listen()
                except Exception as e:
                    print(f"⚠️  Listen error: {e}")
                    if self_healing.auto_fix_error(e, "Voice listening"):
                        continue
                    else:
                        consecutive_errors += 1
                        if consecutive_errors >= max_consecutive_errors:
                            print("❌ Too many voice errors. Auto-switching to text mode.")
                            use_text_mode = True
                            print("💬 Text mode active. Type your commands.")
                        continue
            
            # Reset error counter on successful input
            consecutive_errors = 0
            
            # Double check pause after listening
            if pause_event.is_set():
                continue

            if user_query == "none" or not user_query: 
                continue
            
            # Normalize Hindi commands to English
            normalized_query = normalize_hindi_command(user_query)
            
            # Shutdown commands
            if any(cmd in normalized_query for cmd in ["quit", "exit", "shutdown", "band karo", "niklo"]):
                print("Shutting down JARVIS...")
                shutdown_msg = "Shutting down. Goodbye!"
                if use_text_mode:
                    print(f"JARVIS: {shutdown_msg}")
                else:
                    try:
                        speak(shutdown_msg)
                    except:
                        print(f"JARVIS: {shutdown_msg}")
                break
            
            # Mode switch commands
            if "text mode" in normalized_query or "text mod" in normalized_query:
                use_text_mode = True
                print("✅ Switched to text mode")
                continue
            
            if "voice mode" in normalized_query or "voice mod" in normalized_query:
                if AutoMode.detect_voice_available():
                    use_text_mode = False
                    print("✅ Switched to voice mode")
                else:
                    print("❌ Voice not available. Staying in text mode.")
                continue
            
            # Error report command
            if "error report" in normalized_query or "show errors" in normalized_query:
                report = jarvis.get_error_report()
                print(report)
                continue
            
            # NPU status command
            if "npu status" in normalized_query or "hardware status" in normalized_query:
                npu_accelerator.print_status()
                continue
            
            # Enhanced wake word / Command filtering Logic
            direct_commands = [
                "open", "close", "launch", "start",
                "volume", "mute", "unmute",
                "search", "find", "look up", "google",
                "create", "make", "write", "read", "delete",
                "who", "what", "when", "where", "how", "why",
                "thank", "hello", "hi", "hey",
                "play", "pause", "stop",
                "email", "send", "message",
                "weather", "time", "date",
                "screenshot", "capture",
                "youtube", "chrome", "browser",  # Added common apps
                "music", "song", "video", "photo"  # Added media types
            ]
            
            # Check both original and normalized query
            is_direct = any(cmd in normalized_query for cmd in direct_commands)
            has_wake_word = "jarvis" in user_query.lower()
            
            # If no wake word and not a direct command, ignore (only in voice mode)
            if not use_text_mode and not has_wake_word and not is_direct:
                print(f"Ignored (no wake word): {user_query}")
                print("💡 Tip: Say 'Jarvis' pehle, phir command")
                continue
            
            # Remove wake word for cleaner processing
            clean_query = user_query.replace("jarvis", "").strip()
            clean_query = clean_query.replace("please", "").replace("can you", "").replace("could you", "").strip()
            clean_query = clean_query.replace("कृपया", "").replace("जरा", "").replace("ज़रा", "").strip()
            
            # Use original query if it has direct commands (preserves Hindi)
            if is_direct and not has_wake_word:
                clean_query = user_query
            
            # Process query with error handling
            try:
                print(f"Processing: {clean_query}")
                response = jarvis.run_conversation(clean_query)
                
                # Check pause before speaking response
                if pause_event.is_set():
                    continue

                if response:
                    if use_text_mode:
                        print(f"JARVIS: {response}")
                    else:
                        try:
                            speak(response)
                        except Exception as e:
                            print(f"⚠️  TTS error: {e}")
                            self_healing.auto_fix_error(e, "Response TTS")
                            print(f"JARVIS: {response}")
                            
            except Exception as e:
                print(f"⚠️  Processing error: {e}")
                consecutive_errors += 1
                
                # Try to auto-fix
                if self_healing.auto_fix_error(e, f"Query processing: {clean_query}"):
                    print("✅ Error fixed! Please try again.")
                    consecutive_errors = 0
                else:
                    error_msg = "Sorry, system error hua. Please try again."
                    if use_text_mode:
                        print(f"JARVIS: {error_msg}")
                    else:
                        try:
                            speak(error_msg)
                        except:
                            print(f"JARVIS: {error_msg}")
                
                # Check if too many errors
                if consecutive_errors >= max_consecutive_errors:
                    print("❌ Too many consecutive errors. Resetting conversation...")
                    jarvis.reset_conversation()
                    consecutive_errors = 0
                    
        except KeyboardInterrupt:
            print("\n⚠️  Keyboard interrupt detected. Type 'quit' to exit or continue...")
            continue
        except Exception as e:
            print(f"❌ Unexpected error in main loop: {e}")
            self_healing.auto_fix_error(e, "Main loop")
            time.sleep(1)  # Prevent rapid error loops
    
    # Final error report
    if AUTO_DEBUG_MODE:
        print("\n" + "="*60)
        print(jarvis.get_error_report())
        print("="*60)


def main():
    """
    Fully autonomous main function.
    Auto-detects best mode and runs everything automatically.
    """
    print("="*60)
    print("🤖 JARVIS - Autonomous AI Assistant")
    print("⚡ NPU-Accelerated for Omen PC")
    print("="*60)
    print("🔧 Self-Healing System: Active")
    print("🧠 Auto-Mode Detection: Active")
    print("="*60)
    
    # Initialize NPU Accelerator
    print("\n🚀 Initializing NPU Acceleration...")
    try:
        # Setup NPU optimizations
        if npu_accelerator.npu_available:
            npu_accelerator.setup_openvino_npu()
            npu_accelerator.setup_onnx_runtime()
            npu_accelerator.optimize_for_speech_recognition()
            npu_accelerator.optimize_for_llm_inference()
        
        # Print NPU status
        npu_accelerator.print_status()
    except Exception as e:
        print(f"⚠️  NPU initialization warning: {e}")
        print("Continuing with CPU/GPU fallback...\n")
    
    # Auto-detect modes
    use_text_mode = AutoMode.should_use_text_mode()
    use_gui = AutoMode.should_use_gui()
    
    print(f"📊 Detected Configuration:")
    print(f"   Voice Mode: {'❌ Disabled' if use_text_mode else '✅ Enabled'}")
    print(f"   GUI Mode: {'✅ Enabled' if use_gui else '❌ Disabled'}")
    print(f"   Debug Logging: {'✅ Enabled' if AUTO_DEBUG_MODE else '❌ Disabled'}")
    print(f"   Hindi Support: ✅ Enabled")
    print()
    
    print("🚀 Starting JARVIS...\n")
    
    # 1. Initialize Registry and Load Skills
    try:
        registry = SkillRegistry()
        skills_dir = os.path.join(os.path.dirname(__file__), "skill")
        registry.load_skills(skills_dir)
        print(f"✅ Loaded {len(registry.skills)} skills successfully")
    except Exception as e:
        print(f"❌ Failed to load skills: {e}")
        if not self_healing.auto_fix_error(e, "Skill loading"):
            print("❌ Critical error. Exiting...")
            sys.exit(1)
        # Retry after fix
        registry = SkillRegistry()
        skills_dir = os.path.join(os.path.dirname(__file__), "skill")
        registry.load_skills(skills_dir)
    
    # 2. Setup Pause Event
    pause_event = threading.Event()
    
    # 3. Start JARVIS Loop in Background Thread
    jarvis_thread = threading.Thread(
        target=jarvis_loop, 
        args=(pause_event, registry, use_text_mode), 
        daemon=True
    )
    jarvis_thread.start()
    
    # 4. Start GUI or keep thread alive
    if use_gui:
        try:
            print("🖥️  Starting GUI...\n")
            run_gui_app(pause_event)
        except Exception as e:
            print(f"⚠️  GUI error: {e}")
            if self_healing.auto_fix_error(e, "GUI startup"):
                print("✅ GUI error fixed. Please restart: python main.py")
            else:
                print("❌ GUI failed. Running in terminal mode...")
                use_gui = False
    
    # If no GUI, keep main thread alive
    if not use_gui:
        print("💻 Running in terminal mode. Press Ctrl+C to exit.\n")
        try:
            jarvis_thread.join()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down JARVIS...")
            print("="*60)
            if AUTO_DEBUG_MODE:
                print(self_healing.get_error_report())
            print("="*60)
            print("Goodbye! 👋")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("🔧 Attempting auto-fix...")
        if self_healing.auto_fix_error(e, "Main function"):
            print("✅ Fixed! Please restart: python main.py")
        else:
            print("❌ Could not auto-fix. Please check the error above.")
            import traceback
            traceback.print_exc()
        sys.exit(1)

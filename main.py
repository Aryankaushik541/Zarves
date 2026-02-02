#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS - Autonomous AI Assistant with Self-Healing + NPU Acceleration
Fully autonomous operation with auto-detection and error recovery
Optimized for Omen PC with NPU support
Natural Indian Language Support - Koi bhi admi bole, JARVIS samajh jayega!
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


def run_startup_tests():
    """
    Run automatic startup tests to verify JARVIS is properly configured.
    This replaces the need to run test_fixes.py separately.
    """
    print("=" * 70)
    print("🧪 JARVIS Startup Verification")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # Test 1: Core Imports
    print("📦 Test 1: Checking core imports...")
    try:
        from core.voice import detect_wake_word, listen, speak
        from core.npu_accelerator import npu_accelerator
        from core.indian_language import normalize_indian_text
        print("✅ All core imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Run: pip install -r requirements.txt")
        all_passed = False
    print()
    
    # Test 2: Wake Word Detection
    print("📝 Test 2: Wake word detection...")
    try:
        from core.voice import detect_wake_word
        test_cases = [
            ("Jarvis, YouTube kholo", True),
            ("जार्विस यूट्यूब खोलो", True),
            ("YouTube kholo", False),
        ]
        
        passed = 0
        for text, should_detect in test_cases:
            has_wake_word, _ = detect_wake_word(text)
            if has_wake_word == should_detect:
                passed += 1
        
        if passed == len(test_cases):
            print(f"✅ Wake word detection working ({passed}/{len(test_cases)} tests passed)")
        else:
            print(f"⚠️  Wake word detection issues ({passed}/{len(test_cases)} tests passed)")
            all_passed = False
    except Exception as e:
        print(f"❌ Wake word test failed: {e}")
        all_passed = False
    print()
    
    # Test 3: Hardware Detection
    print("🖥️  Test 3: Hardware detection...")
    try:
        from core.npu_accelerator import npu_accelerator
        npu_accelerator.print_status()
        print("✅ Hardware detection successful")
    except Exception as e:
        print(f"⚠️  Hardware detection warning: {e}")
        # Not critical, don't fail
    print()
    
    # Test 4: PyTorch & CUDA
    print("🔥 Test 4: PyTorch & CUDA...")
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"   ✅ CUDA available: {torch.version.cuda}")
            print(f"   ✅ GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("   ℹ️  Using CPU (no GPU detected)")
    except ImportError:
        print("⚠️  PyTorch not installed (optional)")
    print()
    
    # Test 5: Speech Recognition
    print("🎤 Test 5: Speech recognition...")
    try:
        import speech_recognition as sr
        print(f"✅ SpeechRecognition installed")
        try:
            mics = sr.Microphone.list_microphone_names()
            print(f"   ✅ Found {len(mics)} microphone(s)")
        except:
            print("   ⚠️  No microphones detected (text mode will be used)")
    except ImportError:
        print("❌ SpeechRecognition not installed")
        print("   Run: pip install SpeechRecognition")
        all_passed = False
    print()
    
    # Test 6: Text-to-Speech
    print("🗣️  Test 6: Text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ pyttsx3 initialized")
    except Exception as e:
        print(f"⚠️  pyttsx3 warning: {e}")
        # Not critical
    print()
    
    # Test 7: Environment Variables
    print("🔑 Test 7: Environment variables...")
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        print(f"✅ GROQ_API_KEY found (length: {len(groq_key)})")
    else:
        print("⚠️  GROQ_API_KEY not found in .env")
        print("   Create .env file and add: GROQ_API_KEY=your_key_here")
        print("   Get free key from: https://console.groq.com/keys")
        all_passed = False
    print()
    
    # Summary
    print("=" * 70)
    if all_passed:
        print("✅ All critical tests passed! JARVIS is ready.")
    else:
        print("⚠️  Some tests failed. JARVIS may have limited functionality.")
        print("   Check the errors above and install missing dependencies.")
    print("=" * 70)
    print()
    
    return all_passed


# Import with self-healing
try:
    from core.voice import speak, listen
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from gui.app import run_gui as run_gui_app
    from core.npu_accelerator import npu_accelerator
    from core.indian_language import normalize_indian_text, extract_intent_from_indian_text, is_indian_question
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


def jarvis_loop(pause_event, registry, use_text_mode):
    """
    Main loop for JARVIS with full autonomous operation.
    Automatically handles all errors and mode switching.
    Supports natural Indian language input.
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
        print("💡 Hinglish bhi chalega! (e.g., 'YouTube kholo', 'gaana bajao')")
    else:
        try:
            speak(startup_msg)
            print("🎤 Voice mode active. Say 'Jarvis' followed by your command.")
            print("💡 Natural Indian language supported!")
            print("   Examples: 'Jarvis, YouTube kholo', 'Jarvis, gaana bajao'")
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
                    user_query = input("YOU: ")
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
            
            # Store original query for display
            original_query = user_query
            
            # Normalize Indian language to English
            # This handles Hinglish, Indian English, and Hindi commands
            normalized_query = normalize_indian_text(user_query)
            
            # Show what was understood
            if normalized_query != user_query.lower():
                print(f"📝 Understood as: {normalized_query}")
            
            # Shutdown commands
            shutdown_commands = ["quit", "exit", "shutdown", "band karo", "niklo", "bye", "goodbye"]
            if any(cmd in normalized_query for cmd in shutdown_commands):
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
                    speak("Voice mode activated")
                else:
                    print("❌ Voice mode not available")
                continue

            # Process query with error handling
            try:
                response = jarvis.process_query(normalized_query)
                
                # Output response
                if use_text_mode:
                    print(f"JARVIS: {response}")
                else:
                    try:
                        speak(response)
                    except Exception as e:
                        print(f"⚠️  TTS error: {e}")
                        print(f"JARVIS: {response}")
                        
            except Exception as e:
                error_msg = f"Error processing query: {str(e)}"
                print(f"❌ {error_msg}")
                
                # Try to auto-fix
                if self_healing.auto_fix_error(e, f"Query processing: {normalized_query}"):
                    print("✅ Error fixed! Please try again.")
                else:
                    # Provide helpful error message
                    if use_text_mode:
                        print("JARVIS: I encountered an error. Please try rephrasing your request.")
                    else:
                        try:
                            speak("I encountered an error. Please try again.")
                        except:
                            print("JARVIS: I encountered an error. Please try rephrasing your request.")
                
        except KeyboardInterrupt:
            print("\n⚠️  Keyboard interrupt. Type 'quit' to exit.")
            continue
        except Exception as e:
            print(f"❌ Unexpected error in main loop: {e}")
            if self_healing.auto_fix_error(e, "Main loop"):
                print("✅ Error fixed! Continuing...")
                continue
            else:
                print("❌ Critical error. Restarting loop...")
                time.sleep(2)


def main():
    """Main entry point with automatic mode detection and startup tests"""
    
    # Run startup tests automatically
    print()
    tests_passed = run_startup_tests()
    
    if not tests_passed:
        print("⚠️  Warning: Some tests failed. Continue anyway? (y/n)")
        try:
            choice = input().lower()
            if choice != 'y':
                print("Exiting. Please fix the errors and try again.")
                sys.exit(1)
        except:
            pass  # Continue anyway in non-interactive mode
        print()
    
    # Auto-detect modes
    use_text_mode = AutoMode.should_use_text_mode()
    use_gui = AutoMode.should_use_gui()
    
    # Print startup banner
    print("=" * 60)
    print("🤖 JARVIS - Autonomous AI Assistant")
    print("=" * 60)
    print()
    print("⚙️  Configuration:")
    print(f"   Voice Mode: {'❌ Disabled' if use_text_mode else '✅ Enabled'}")
    print(f"   GUI Mode: {'✅ Enabled' if use_gui else '❌ Disabled'}")
    print(f"   Debug Logging: {'✅ Enabled' if AUTO_DEBUG_MODE else '❌ Disabled'}")
    print(f"   Indian Language: ✅ Enabled (Hinglish + Hindi)")
    print()
    
    print("💡 Example Commands:")
    print("   • YouTube kholo")
    print("   • Gaana bajao")
    print("   • Google pe dhundho")
    print("   • Time kya hua hai?")
    print("   • Calculator chalu karo")
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
            print("=" * 60)
            if AUTO_DEBUG_MODE:
                print(self_healing.get_error_report())
            print("=" * 60)
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

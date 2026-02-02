import os
import sys
import argparse
import threading 
import time
from dotenv import load_dotenv
from core.self_healing import self_healing

# Load Env with error handling
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  .env load करने में error: {e}")
    self_healing.auto_fix_error(e, ".env loading")

# Import with self-healing
try:
    from core.voice import speak, listen
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from gui.app import run_gui as run_gui_app
except ImportError as e:
    print(f"⚠️  Import error detect हुआ: {e}")
    if self_healing.auto_fix_error(e, "Initial imports"):
        print("✅ Dependencies fixed! Please restart the application.")
        sys.exit(0)
    else:
        print("❌ Critical import error. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

# Check API key
if not os.environ.get("GROQ_API_KEY"):
    print("⚠️  GROQ_API_KEY not found.")
    if not self_healing.fix_api_key_error():
        print("❌ Please set GROQ_API_KEY in .env file")
        sys.exit(1)

def jarvis_loop(pause_event, registry, args):
    """
    Main loop for JARVIS with self-healing capabilities.
    Automatically recovers from errors and continues running.
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
    if args.text:
        print(f"JARVIS: {startup_msg}")
    else:
        try:
            speak(startup_msg)
        except Exception as e:
            print(f"⚠️  TTS error: {e}")
            self_healing.auto_fix_error(e, "Startup TTS")
            print(f"JARVIS: {startup_msg}")

    # Main loop with error recovery
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            # Check for pause
            if pause_event.is_set():
                time.sleep(0.5)
                continue

            # Get user input
            if args.text:
                try:
                    user_query = input("YOU: ").lower()
                except EOFError:
                    break
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
                            print("❌ Too many consecutive errors. Switching to text mode.")
                            args.text = True
                        continue
            
            # Reset error counter on successful input
            consecutive_errors = 0
            
            # Double check pause after listening
            if pause_event.is_set():
                continue

            if user_query == "none" or not user_query: 
                continue
                
            # Shutdown commands
            if "quit" in user_query or "exit" in user_query or "shutdown" in user_query: 
                print("Shutting down JARVIS loop...")
                shutdown_msg = "Shutting down."
                if args.text:
                    print(f"JARVIS: {shutdown_msg}")
                else:
                    try:
                        speak(shutdown_msg)
                    except:
                        print(f"JARVIS: {shutdown_msg}")
                break
            
            # Error report command
            if "error report" in user_query or "show errors" in user_query:
                report = jarvis.get_error_report()
                print(report)
                continue
            
            # Wake word / Command filtering Logic
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
                "बजाओ", "खोलो", "बंद", "ढूंढो"  # Hindi commands
            ]
            
            is_direct = any(cmd in user_query for cmd in direct_commands)
            
            # If no wake word and not a direct command, ignore
            if "jarvis" not in user_query and not is_direct:
                print(f"Ignored: {user_query}")
                continue
            
            # Remove wake word for cleaner processing
            clean_query = user_query.replace("jarvis", "").strip()
            clean_query = clean_query.replace("please", "").replace("can you", "").replace("could you", "").strip()
            
            # Process query with error handling
            try:
                print(f"Processing: {clean_query}")
                response = jarvis.run_conversation(clean_query)
                
                # Check pause before speaking response
                if pause_event.is_set():
                    continue

                if response:
                    if args.text:
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
                    error_msg = "System error. Please try again."
                    if args.text:
                        print(f"JARVIS: {error_msg}")
                    else:
                        try:
                            speak(error_msg)
                        except:
                            print(f"JARVIS: {error_msg}")
                
                # Check if too many errors
                if consecutive_errors >= max_consecutive_errors:
                    print("❌ Too many consecutive errors. Resetting...")
                    jarvis.reset_conversation()
                    consecutive_errors = 0
                    
        except KeyboardInterrupt:
            print("\n⚠️  Keyboard interrupt detected. Shutting down...")
            break
        except Exception as e:
            print(f"❌ Unexpected error in main loop: {e}")
            self_healing.auto_fix_error(e, "Main loop")
            time.sleep(1)  # Prevent rapid error loops

def main():
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant with Self-Healing")
    parser.add_argument("--text", action="store_true", help="Run in text mode (no voice I/O)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with detailed error logs")
    args = parser.parse_args()

    print("🚀 Starting JARVIS with Self-Healing System...")
    
    # 1. Initialize Registry and Load Skills
    try:
        registry = SkillRegistry()
        skills_dir = os.path.join(os.path.dirname(__file__), "skill")
        registry.load_skills(skills_dir)
        print(f"✅ Loaded {len(registry.skills)} skills")
    except Exception as e:
        print(f"❌ Failed to load skills: {e}")
        if not self_healing.auto_fix_error(e, "Skill loading"):
            sys.exit(1)
        # Retry after fix
        registry = SkillRegistry()
        skills_dir = os.path.join(os.path.dirname(__file__), "skill")
        registry.load_skills(skills_dir)
    
    # 2. Setup Pause Event
    pause_event = threading.Event()
    
    # 3. Start JARVIS Loop in Background Thread
    t = threading.Thread(target=jarvis_loop, args=(pause_event, registry, args), daemon=True)
    t.start()
    
    # 4. Start GUI in Main Thread
    try:
        run_gui_app(pause_event)
    except Exception as e:
        print(f"⚠️  GUI error: {e}")
        if self_healing.auto_fix_error(e, "GUI startup"):
            print("✅ GUI error fixed. Please restart.")
        else:
            print("❌ Running in text-only mode...")
            args.text = True
            # Keep the thread alive
            try:
                t.join()
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
    
    # Print final error report if debug mode
    if args.debug:
        print("\n" + "="*60)
        print(self_healing.get_error_report())
        print("="*60)

if __name__ == "__main__":
    main()

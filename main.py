#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 ZARVES - Main Entry Point
Voice-Controlled AI Assistant

Run this file to start Zarves Pro
"""

import sys
import os

def main():
    """Main entry point - runs Zarves Pro"""
    
    print("""
    ╔═══════════════════════════════════════╗
    ║     🤖 ZARVES AI AGENT               ║
    ║  Voice-Controlled Smart Assistant     ║
    ╚═══════════════════════════════════════╝
    
    Starting Zarves Pro...
    """)
    
    try:
        # Import and run Zarves Pro
        from zarves_pro import main as zarves_main
        zarves_main()
        
    except ImportError:
        print("⚠️ Zarves Pro not found. Trying basic version...")
        try:
            from zarves_advanced import main as zarves_main
            zarves_main()
        except ImportError:
            print("""
            ❌ Error: Zarves files not found!
            
            Please ensure these files exist:
            - zarves_pro.py (recommended)
            - zarves_advanced.py (basic)
            
            Run: python zarves_pro.py
            Or: python zarves_advanced.py
            """)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Zarves stopped by user. Goodbye!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor help, read RUN_ME_FIRST.md")
        sys.exit(1)


if __name__ == "__main__":
    main()

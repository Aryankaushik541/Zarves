#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 ZARVES PRO - Enhanced AI Agent
Advanced version with better AI, more features, and smarter responses

New Features:
- Context-aware conversations
- Better pattern recognition
- Website-specific actions
- Smart suggestions
- Command history
- Error recovery
"""

import os
import sys
import time
import json
import re
from datetime import datetime
from pathlib import Path

# Import base Zarves
try:
    from zarves_advanced import (
        OfflineAI, VoiceEngine, BrowserController, 
        SystemController, ZarvesAgent
    )
except ImportError:
    print("❌ Please ensure zarves_advanced.py is in the same directory")
    sys.exit(1)


class EnhancedAI(OfflineAI):
    """
    Enhanced AI with better understanding and context
    """
    
    def __init__(self):
        super().__init__()
        self.context = []
        self.last_action = None
        self.command_history = []
        self.user_preferences = {}
        
        # Enhanced knowledge base
        self.knowledge_base.update({
            # Social media
            "open linkedin": {"action": "open_browser", "url": "https://www.linkedin.com"},
            "open reddit": {"action": "open_browser", "url": "https://www.reddit.com"},
            "open pinterest": {"action": "open_browser", "url": "https://www.pinterest.com"},
            
            # Entertainment
            "open spotify": {"action": "open_browser", "url": "https://open.spotify.com"},
            "open netflix": {"action": "open_browser", "url": "https://www.netflix.com"},
            "open prime video": {"action": "open_browser", "url": "https://www.primevideo.com"},
            "open hotstar": {"action": "open_browser", "url": "https://www.hotstar.com"},
            
            # Shopping
            "open amazon": {"action": "open_browser", "url": "https://www.amazon.in"},
            "open flipkart": {"action": "open_browser", "url": "https://www.flipkart.com"},
            "open myntra": {"action": "open_browser", "url": "https://www.myntra.com"},
            
            # Education
            "open coursera": {"action": "open_browser", "url": "https://www.coursera.org"},
            "open udemy": {"action": "open_browser", "url": "https://www.udemy.com"},
            "open khan academy": {"action": "open_browser", "url": "https://www.khanacademy.org"},
            
            # Tools
            "open github": {"action": "open_browser", "url": "https://www.github.com"},
            "open stackoverflow": {"action": "open_browser", "url": "https://stackoverflow.com"},
            "open chatgpt": {"action": "open_browser", "url": "https://chat.openai.com"},
            
            # News
            "open news": {"action": "open_browser", "url": "https://news.google.com"},
            "open bbc": {"action": "open_browser", "url": "https://www.bbc.com"},
            
            # Context-aware commands
            "play music": {"action": "open_browser", "url": "https://open.spotify.com"},
            "watch video": {"action": "open_browser", "url": "https://www.youtube.com"},
            "check email": {"action": "open_browser", "url": "https://mail.google.com"},
            "online shopping": {"action": "open_browser", "url": "https://www.amazon.in"},
        })
    
    def understand(self, text):
        """Enhanced understanding with context"""
        text = text.lower().strip()
        
        # Save to history
        self.command_history.append({
            "text": text,
            "time": datetime.now().isoformat()
        })
        
        # Context-aware processing
        if self.last_action:
            # Follow-up commands
            if text in ["yes", "haan", "ok", "sure", "do it"]:
                return self.last_action
            elif text in ["no", "nahi", "cancel", "stop"]:
                return {"action": "respond", "response": "Theek hai, cancel kar diya"}
        
        # Smart pattern matching
        action = self._smart_match(text)
        if action:
            self.last_action = action
            return action
        
        # Fallback to base AI
        return super().understand(text)
    
    def _smart_match(self, text):
        """Smart pattern matching with context"""
        
        # Website detection
        if "open" in text or "kholo" in text:
            # Extract website name
            words = text.split()
            for i, word in enumerate(words):
                if word in ["open", "kholo"]:
                    if i + 1 < len(words):
                        site = " ".join(words[i+1:])
                        
                        # Check if it's a known site
                        for key in self.knowledge_base:
                            if site in key:
                                return self.knowledge_base[key]
                        
                        # Try to construct URL
                        site_clean = site.replace(" ", "")
                        if not site_clean.endswith(".com"):
                            site_clean += ".com"
                        
                        return {
                            "action": "open_browser",
                            "url": f"https://www.{site_clean}"
                        }
        
        # Search with context
        if any(word in text for word in ["search", "find", "dhundo", "khojo"]):
            query = text
            for word in ["search", "find", "dhundo", "khojo", "for", "karo"]:
                query = query.replace(word, "")
            query = query.strip()
            
            # Determine search engine
            if "youtube" in text:
                return {
                    "action": "search",
                    "engine": "youtube",
                    "query": query.replace("youtube", "").strip()
                }
            else:
                return {
                    "action": "search",
                    "engine": "google",
                    "query": query
                }
        
        # Play/Watch commands
        if "play" in text or "chalao" in text:
            query = text.replace("play", "").replace("chalao", "").strip()
            return {
                "action": "search",
                "engine": "youtube",
                "query": query
            }
        
        # Navigation
        if "back" in text or "peeche" in text:
            return {"action": "navigate", "direction": "back"}
        if "forward" in text or "aage" in text:
            return {"action": "navigate", "direction": "forward"}
        if "refresh" in text or "reload" in text:
            return {"action": "navigate", "direction": "refresh"}
        
        return None
    
    def get_suggestions(self):
        """Get smart suggestions based on history"""
        suggestions = []
        
        # Time-based suggestions
        hour = datetime.now().hour
        if 6 <= hour < 12:
            suggestions.append("Good morning! Check news?")
        elif 12 <= hour < 17:
            suggestions.append("Good afternoon! Need anything?")
        elif 17 <= hour < 21:
            suggestions.append("Good evening! Relax with music?")
        else:
            suggestions.append("Good night! Time to sleep?")
        
        # History-based suggestions
        if len(self.command_history) > 0:
            last_cmd = self.command_history[-1]["text"]
            if "youtube" in last_cmd:
                suggestions.append("Want to search more videos?")
            elif "google" in last_cmd:
                suggestions.append("Need another search?")
        
        return suggestions


class ZarvesProAgent(ZarvesAgent):
    """
    Enhanced Zarves Agent with Pro features
    """
    
    def __init__(self):
        print("🚀 Initializing Zarves PRO...")
        self.ai = EnhancedAI()  # Use enhanced AI
        self.voice = VoiceEngine()
        self.browser = BrowserController()
        self.system = SystemController()
        self.running = False
        
        # Pro features
        self.session_start = datetime.now()
        self.commands_executed = 0
        self.errors_count = 0
        
        print("✅ Zarves PRO is ready!")
        self.voice.speak("Zarves Pro taiyar hai! Main aur bhi smart hoon ab!")
    
    def execute_action(self, action):
        """Execute action with error handling"""
        try:
            self.commands_executed += 1
            
            action_type = action.get("action")
            
            if action_type == "navigate":
                direction = action.get("direction")
                if direction == "back":
                    self.voice.speak("Peeche ja raha hoon")
                    self.browser.driver.back() if self.browser.driver else None
                elif direction == "forward":
                    self.voice.speak("Aage ja raha hoon")
                    self.browser.driver.forward() if self.browser.driver else None
                elif direction == "refresh":
                    self.voice.speak("Page refresh kar raha hoon")
                    self.browser.driver.refresh() if self.browser.driver else None
            else:
                # Use parent class method
                super().execute_action(action)
                
        except Exception as e:
            self.errors_count += 1
            print(f"❌ Error: {e}")
            self.voice.speak("Kuch galat ho gaya. Phir se try karo.")
    
    def show_stats(self):
        """Show session statistics"""
        duration = datetime.now() - self.session_start
        stats = f"""
        📊 Session Stats:
        ⏱️ Duration: {duration.seconds // 60} minutes
        ✅ Commands: {self.commands_executed}
        ❌ Errors: {self.errors_count}
        """
        print(stats)
    
    def run(self):
        """Enhanced run loop with better UX"""
        self.running = True
        
        # Show suggestions
        suggestions = self.ai.get_suggestions()
        if suggestions:
            print(f"\n💡 Suggestion: {suggestions[0]}\n")
        
        while self.running:
            # Listen for command
            command = self.voice.listen()
            
            if command is None:
                continue
            
            # Check for special commands
            if "stats" in command.lower() or "statistics" in command.lower():
                self.show_stats()
                continue
            
            # Check for exit
            if any(word in command.lower() for word in ['exit', 'quit', 'band karo', 'bye', 'alvida']):
                self.voice.speak("Zarves Pro band ho raha hai. Alvida!")
                self.show_stats()
                self.running = False
                break
            
            # Process command
            action = self.ai.understand(command)
            
            # Execute
            self.execute_action(action)
            
            # Show suggestions after some commands
            if self.commands_executed % 5 == 0:
                suggestions = self.ai.get_suggestions()
                if suggestions:
                    print(f"\n💡 {suggestions[0]}\n")


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════╗
    ║     🚀 ZARVES PRO v2.0               ║
    ║  Enhanced AI-Powered Voice Assistant  ║
    ╚═══════════════════════════════════════╝
    
    ✨ New Features:
    ✅ Smarter AI with context awareness
    ✅ More websites and services
    ✅ Better error handling
    ✅ Smart suggestions
    ✅ Session statistics
    ✅ Command history
    
    🎤 Enhanced Commands:
    - "Open LinkedIn/Reddit/Spotify"
    - "Play [song name]"
    - "Watch [video topic]"
    - "Go back/forward"
    - "Show stats"
    
    Say "Exit" to quit
    """)
    
    try:
        agent = ZarvesProAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'agent' in locals():
            agent.cleanup()
        print("👋 Zarves Pro stopped.")


if __name__ == "__main__":
    main()

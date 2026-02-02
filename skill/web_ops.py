import webbrowser
import json
import sys
from typing import List, Dict, Any, Callable
from core.skill import Skill

class WebSkill(Skill):
    @property
    def name(self) -> str:
        return "web_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Search Google for a query or topic",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "search_term": {
                                "type": "string",
                                "description": "The search query or topic to search for"
                            } 
                        }, 
                        "required": ["search_term"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_website",
                    "description": "Open a specific website URL in the browser",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "url": {
                                "type": "string",
                                "description": "The website URL to open (e.g., https://www.example.com)"
                            } 
                        }, 
                        "required": ["url"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_youtube",
                    "description": "Play a song or video on YouTube",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "The song name or video to play on YouTube"
                            } 
                        }, 
                        "required": ["query"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "google_search": self.google_search,
            "open_website": self.open_website,
            "play_youtube": self.play_youtube
        }

    def google_search(self, search_term):
        try:
            url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
            webbrowser.open(url)
            return json.dumps({"status": "success", "action": "search", "term": search_term})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def open_website(self, url):
        try:
            # Add https:// if not present
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return json.dumps({"status": "success", "action": "open_website", "url": url})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def play_youtube(self, query):
        """
        Play YouTube video/music with cross-platform support.
        Works on Windows, macOS, and Linux.
        """
        try:
            import pywhatkit as kit
            import time
            
            print(f"YouTube पर खोज रहा हूँ: {query}")
            
            # Platform-specific handling
            if sys.platform == "win32":  # Windows
                # On Windows, use close_tab=False to keep browser open
                kit.playonyt(query, open_web=True)
                time.sleep(2)  # Give browser time to open
            elif sys.platform == "darwin":  # macOS
                # On macOS, use default settings
                kit.playonyt(query, open_web=True)
                time.sleep(2)
            else:  # Linux and others
                kit.playonyt(query, open_web=True)
                time.sleep(2)
            
            return json.dumps({
                "status": "success", 
                "action": "play_youtube", 
                "query": query,
                "platform": sys.platform
            })
            
        except ImportError:
            # Fallback to webbrowser if pywhatkit not installed
            print("pywhatkit नहीं मिला, browser fallback उपयोग कर रहा हूँ...")
            try:
                # Create YouTube search URL that auto-plays first result
                search_query = query.replace(' ', '+')
                url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open(url)
                return json.dumps({
                    "status": "success", 
                    "action": "play_youtube_fallback", 
                    "query": query, 
                    "note": "pywhatkit install करें बेहतर playback के लिए: pip install pywhatkit"
                })
            except Exception as e:
                return json.dumps({"status": "error", "error": str(e)})
                
        except Exception as e:
            print(f"YouTube Error: {e}")
            # Final fallback
            try:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)
                return json.dumps({
                    "status": "partial_success", 
                    "action": "youtube_search", 
                    "query": query,
                    "error": str(e)
                })
            except Exception as e2:
                return json.dumps({"status": "error", "error": str(e2)})

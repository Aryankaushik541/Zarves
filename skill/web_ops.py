import webbrowser
import json
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
        try:
            import pywhatkit as kit
            # Use open_web=True to open in normal browser window instead of fullscreen
            kit.playonyt(query, open_web=True)
            return json.dumps({"status": "success", "action": "play_youtube", "query": query})
        except ImportError:
            # Fallback to browser if pywhatkit not installed
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return json.dumps({"status": "success", "action": "play_youtube_fallback", "query": query, "note": "Install pywhatkit for better YouTube playback"})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

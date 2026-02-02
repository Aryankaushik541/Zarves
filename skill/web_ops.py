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
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "google_search": self.google_search,
            "open_website": self.open_website
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

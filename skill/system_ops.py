import os
import json
import webbrowser
from typing import List, Dict, Any, Callable
from core.skill import Skill

class SystemSkill(Skill):
    @property
    def name(self) -> str:
        return "system_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
             {
                "type": "function",
                "function": {
                    "name": "set_volume",
                    "description": "Set system volume (0-100)",
                    "parameters": { "type": "object", "properties": { "level": {"type": "integer"} }, "required": ["level"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application or website. For web services like YouTube, Gmail, etc., opens in browser. For system apps like Safari, Chrome, etc., opens the application.",
                    "parameters": { "type": "object", "properties": { "app_name": {"type": "string", "description": "Name of the app or website to open (e.g., 'YouTube', 'Safari', 'Chrome', 'Gmail')"} }, "required": ["app_name"] }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "set_volume": self.set_volume,
            "open_app": self.open_app
        }

    def set_volume(self, level):
        try:
            os.system(f"osascript -e 'set volume output volume {level}'")
            return json.dumps({"status": "success", "level": level})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def open_app(self, app_name):
        try:
            # Map of web services to their URLs
            web_services = {
                "youtube": "https://www.youtube.com",
                "gmail": "https://mail.google.com",
                "google": "https://www.google.com",
                "facebook": "https://www.facebook.com",
                "twitter": "https://www.twitter.com",
                "instagram": "https://www.instagram.com",
                "reddit": "https://www.reddit.com",
                "github": "https://www.github.com",
                "linkedin": "https://www.linkedin.com",
                "netflix": "https://www.netflix.com",
                "spotify": "https://open.spotify.com",
                "amazon": "https://www.amazon.com",
            }
            
            app_lower = app_name.lower()
            
            # Check if it's a web service
            if app_lower in web_services:
                webbrowser.open(web_services[app_lower])
                return json.dumps({"status": "success", "opened": "browser", "service": app_name, "url": web_services[app_lower]})
            else:
                # Try to open as macOS application
                os.system(f"open -a '{app_name}'")
                return json.dumps({"status": "success", "opened": "app", "app": app_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

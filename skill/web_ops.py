import webbrowser
import json
import sys
import random
import requests
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
                    "description": "Play a song or video on YouTube. If query is empty or 'music'/'song', automatically plays a trending song. Use for: 'youtube kholo', 'youtube kholo aur music play karo', 'play X on youtube'",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "The song name or video to play. Leave empty or use 'music'/'song' to auto-play trending music. Examples: 'Kesariya', 'Arijit Singh', '' (empty for trending), 'music', 'song'"
                            } 
                        }, 
                        "required": [] 
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
    
    def _get_trending_song(self):
        """
        Fetch a trending song from YouTube
        """
        try:
            # Popular trending Hindi songs (fallback)
            trending_songs = [
                "Tauba Tauba Bad Newz",
                "Satranga Animal",
                "Arjan Vailly Animal", 
                "Maan Meri Jaan King",
                "Kesariya Brahmastra",
                "Chaleya Jawan",
                "Apna Bana Le Bhediya",
                "O Maahi Dunki",
                "Pehle Bhi Main Vishal Mishra",
                "Heeriye Jasleen Royal",
                "Tere Vaaste Zara Hatke",
                "Ve Kamleya Rocky Aur Rani",
                "Kahani Suno 2.0",
                "Hua Main Animal"
            ]
            
            # Try to fetch latest trending from YouTube
            try:
                search_query = "trending hindi songs 2024"
                url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=5)
                
                # Extract video titles
                import re
                titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)
                
                # Filter and get first valid song
                for title in titles[:10]:
                    if not any(skip in title.lower() for skip in ['mix', 'playlist', 'channel', 'hours']):
                        print(f"🎵 Found trending: {title}")
                        return title
                        
            except Exception as e:
                print(f"⚠️  Could not fetch live trending, using fallback: {e}")
            
            # Fallback to popular songs
            song = random.choice(trending_songs)
            print(f"🎵 Playing popular song: {song}")
            return song
            
        except Exception as e:
            print(f"⚠️  Trending fetch error: {e}")
            return "latest hindi songs 2024"
    
    def play_youtube(self, query=""):
        """
        Play YouTube video/music with cross-platform support.
        Auto-plays trending music if no query provided.
        Works on Windows, macOS, and Linux.
        """
        try:
            # Check if user wants music/song or left empty
            should_play_trending = (
                not query or 
                query.strip() == "" or 
                query.lower() in ["music", "song", "gaana", "gana", "kuch bhi", "anything"]
            )
            
            if should_play_trending:
                print("🎵 No specific song requested, playing trending music...")
                query = self._get_trending_song()
                print(f"🎵 Selected: {query}")
            
            import pywhatkit as kit
            import time
            
            print(f"🎵 YouTube पर खोज रहा हूँ: {query}")
            
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
                "platform": sys.platform,
                "auto_selected": should_play_trending
            })
            
        except ImportError:
            # Fallback to webbrowser if pywhatkit not installed
            print("pywhatkit नहीं मिला, browser fallback उपयोग कर रहा हूँ...")
            try:
                # Auto-select trending if needed
                if not query or query.strip() == "" or query.lower() in ["music", "song", "gaana"]:
                    query = self._get_trending_song()
                    print(f"🎵 Auto-selected: {query}")
                
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
                # Auto-select trending if needed
                if not query or query.strip() == "":
                    query = self._get_trending_song()
                
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

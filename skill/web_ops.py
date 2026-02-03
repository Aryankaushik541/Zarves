import webbrowser
import json
import sys
import random
import requests
import time
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
                    "description": "Play a song or video on YouTube with AUTO-PLAY. If query is empty or 'music'/'song', automatically plays a trending song. Use for: 'youtube kholo', 'youtube kholo aur music play karo', 'play X on youtube'",
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
    
    def _auto_play_with_selenium(self, query):
        """
        Use Selenium to automatically click and play the first video
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            print("🎬 Opening YouTube with auto-play...")
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Search on YouTube
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            driver.get(url)
            
            # Wait for video thumbnails to load
            print("⏳ Waiting for videos to load...")
            wait = WebDriverWait(driver, 10)
            
            # Find and click first video
            # YouTube uses different selectors, try multiple approaches
            try:
                # Method 1: Try ytd-video-renderer
                video = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
                ))
                print("✅ Found video, clicking to play...")
                video.click()
                
            except:
                # Method 2: Try alternative selector
                try:
                    video = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a#thumbnail")
                    ))
                    print("✅ Found video (alt method), clicking to play...")
                    video.click()
                except:
                    print("⚠️  Could not auto-click, but YouTube is open")
            
            # Keep browser open
            print("✅ YouTube opened and playing!")
            
            return json.dumps({
                "status": "success",
                "action": "auto_play_youtube",
                "query": query,
                "method": "selenium"
            })
            
        except ImportError as ie:
            print(f"⚠️  Selenium not available: {ie}")
            print("💡 Install for auto-play: pip install selenium webdriver-manager")
            return None
        except Exception as e:
            print(f"⚠️  Auto-play failed: {e}")
            return None
    
    def play_youtube(self, query=""):
        """
        Play YouTube video/music with AUTO-PLAY feature.
        Auto-plays trending music if no query provided.
        Uses Selenium to automatically click and play the first video.
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
            
            # Try Selenium auto-play first (best experience)
            selenium_result = self._auto_play_with_selenium(query)
            if selenium_result:
                return selenium_result
            
            # Fallback 1: Try pywhatkit
            print("🔄 Trying pywhatkit method...")
            try:
                import pywhatkit as kit
                
                print(f"🎵 YouTube पर खोज रहा हूँ: {query}")
                
                # Platform-specific handling
                if sys.platform == "win32":  # Windows
                    kit.playonyt(query, open_web=True)
                    time.sleep(2)
                elif sys.platform == "darwin":  # macOS
                    kit.playonyt(query, open_web=True)
                    time.sleep(2)
                else:  # Linux
                    kit.playonyt(query, open_web=True)
                    time.sleep(2)
                
                print("✅ YouTube opened (manual click needed)")
                
                return json.dumps({
                    "status": "success", 
                    "action": "play_youtube", 
                    "query": query,
                    "platform": sys.platform,
                    "auto_selected": should_play_trending,
                    "note": "Video search opened, click first result to play"
                })
                
            except ImportError:
                print("⚠️  pywhatkit not found")
                pass
            
            # Fallback 2: Direct browser open
            print("🔄 Using browser fallback...")
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(url)
            
            print("✅ YouTube opened (manual click needed)")
            
            return json.dumps({
                "status": "success", 
                "action": "play_youtube_fallback", 
                "query": query,
                "auto_selected": should_play_trending,
                "note": "YouTube search opened, click first video to play"
            })
                
        except Exception as e:
            print(f"❌ YouTube Error: {e}")
            # Final fallback
            try:
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

import webbrowser
import json
import sys
import random
import requests
import time
import threading
import atexit
from typing import List, Dict, Any, Callable
from core.skill import Skill

class MusicSkill(Skill):
    """
    Music playback skill with trending songs support and AUTO-PLAY
    Automatically fetches latest popular songs from YouTube and plays them
    """
    
    # Class variable to store active driver instances
    active_drivers = []
    
    # Fallback popular Hindi songs (if internet fails)
    POPULAR_HINDI_SONGS = [
        "Tum Hi Ho Aashiqui 2",
        "Kesariya Brahmastra",
        "Apna Bana Le Bhediya",
        "Chaleya Jawan",
        "Maan Meri Jaan King",
        "Kahani Suno 2.0",
        "Satranga Animal",
        "Arjan Vailly Animal",
        "Hua Main Animal",
        "O Maahi Dunki",
        "Tauba Tauba Bad Newz",
        "Pehle Bhi Main Vishal Mishra",
        "Tere Vaaste Zara Hatke Zara Bachke",
        "Ve Kamleya Rocky Aur Rani",
        "What Jhumka Arijit Singh",
        "Tum Kya Mile Pritam",
        "Heeriye Jasleen Royal",
        "Besharam Rang Pathaan",
        "Jhoome Jo Pathaan",
        "Naina Arijit Singh",
    ]
    
    def __init__(self):
        super().__init__()
        # Register cleanup on exit
        atexit.register(self._cleanup_drivers)
    
    @property
    def name(self) -> str:
        return "music_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "play_music",
                    "description": "Play music on YouTube with AUTO-PLAY. Supports Hindi songs, English songs, or any music request. Use this for commands like 'play music', 'gaana bajao', 'song sunao', 'new song bajao', 'latest song play karo', etc. Automatically plays trending songs if no specific song is mentioned.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "Song name, artist, or music type. If empty, 'random', 'new', 'latest', or 'trending', plays a currently trending song. Examples: 'Kesariya', 'Arijit Singh songs', 'romantic songs', 'latest Hindi songs', 'new song'"
                            },
                            "language": {
                                "type": "string",
                                "description": "Language preference: 'hindi', 'english', 'punjabi', 'tamil', etc. Default is 'hindi'",
                                "default": "hindi"
                            }
                        }, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_trending_song",
                    "description": "Play a currently trending/viral song from YouTube with AUTO-PLAY. Perfect for 'play new song', 'latest song bajao', 'trending song play karo'",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "language": {
                                "type": "string",
                                "description": "Language: 'hindi', 'english', 'punjabi', etc. Default is 'hindi'",
                                "default": "hindi"
                            }
                        }, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_hindi_song",
                    "description": "Play a specific Hindi song or a random popular Hindi song with AUTO-PLAY",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "song_name": {
                                "type": "string",
                                "description": "Hindi song name or artist. Leave empty for random popular song"
                            }
                        }, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_playlist",
                    "description": "Play a music playlist or mix on YouTube with AUTO-PLAY",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "playlist_type": {
                                "type": "string",
                                "description": "Type of playlist: 'romantic', 'party', 'sad', 'workout', 'bollywood hits', 'latest', etc."
                            },
                            "language": {
                                "type": "string",
                                "description": "Language: 'hindi', 'english', 'punjabi', etc.",
                                "default": "hindi"
                            }
                        }, 
                        "required": ["playlist_type"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "play_music": self.play_music,
            "play_trending_song": self.play_trending_song,
            "play_hindi_song": self.play_hindi_song,
            "play_playlist": self.play_playlist
        }

    def _cleanup_drivers(self):
        """
        Cleanup function called on exit - does NOT close browsers
        Just cleans up references
        """
        try:
            print(f"🧹 Cleaning up {len(self.active_drivers)} driver references...")
            self.active_drivers.clear()
        except:
            pass

    def _get_trending_songs(self, language="hindi", count=10):
        """
        Fetch trending songs from YouTube using web scraping
        """
        try:
            # Search for trending songs
            search_query = f"trending {language} songs 2024"
            url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # Extract video titles from response
            import re
            # Find video titles in the response
            titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)
            
            # Filter out non-song results (like "Mix", "Playlist", etc.)
            songs = []
            for title in titles[:count * 2]:  # Get extra to filter
                # Skip if it's a playlist/mix/channel
                if any(skip in title.lower() for skip in ['mix', 'playlist', 'channel', 'vevo', 'official']):
                    continue
                songs.append(title)
                if len(songs) >= count:
                    break
            
            return songs if songs else None
            
        except Exception as e:
            print(f"⚠️  Could not fetch trending songs: {e}")
            return None

    def _auto_play_with_selenium(self, query):
        """
        Use Selenium to automatically click and play the first video
        Browser will stay open PERMANENTLY using detach option
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
            
            # Setup Chrome options with DETACH to keep browser open
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # CRITICAL: This keeps Chrome open even after driver quits
            chrome_options.add_experimental_option("detach", True)
            
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable automation flags
            chrome_options.add_argument("--disable-infobars")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Store driver reference
            self.active_drivers.append(driver)
            
            # Search on YouTube
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            driver.get(url)
            
            # Wait for video thumbnails to load
            print("⏳ Waiting for videos to load...")
            wait = WebDriverWait(driver, 15)
            
            # Find and click first video
            video_clicked = False
            try:
                # Method 1: Try ytd-video-renderer
                video = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
                ))
                print("✅ Found video, clicking to play...")
                video.click()
                video_clicked = True
                
            except:
                # Method 2: Try alternative selector
                try:
                    video = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a#thumbnail")
                    ))
                    print("✅ Found video (alt method), clicking to play...")
                    video.click()
                    video_clicked = True
                except:
                    print("⚠️  Could not auto-click, but YouTube is open")
            
            # Wait a bit for video to start loading
            if video_clicked:
                time.sleep(3)
                print("✅ Video is playing!")
            
            # IMPORTANT: Don't quit driver - let it detach
            # The browser will stay open independently
            print("🎵 Browser will stay open. Close it manually when done.")
            
            return json.dumps({
                "status": "success",
                "action": "auto_play_music",
                "query": query,
                "method": "selenium_detached",
                "note": "Browser is now independent and will stay open until you close it manually."
            })
            
        except ImportError as ie:
            print(f"⚠️  Selenium not available: {ie}")
            print("💡 Install with: pip install selenium webdriver-manager")
            return None
        except Exception as e:
            print(f"⚠️  Auto-play failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def play_trending_song(self, language="hindi"):
        """
        Play a currently trending song with AUTO-PLAY
        """
        try:
            print(f"🔍 Fetching trending {language} songs...")
            trending = self._get_trending_songs(language, count=5)
            
            if trending:
                song = random.choice(trending)
                print(f"🎵 Found trending: {song}")
            else:
                # Fallback to search query
                song = f"latest {language} songs 2024"
                print(f"🎵 Playing: {song}")
            
            return self._play_on_youtube(song)
                
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def play_music(self, query="", language="hindi"):
        """
        Play music on YouTube with smart defaults, trending support, and AUTO-PLAY
        """
        try:
            # Check if user wants trending/new/latest songs
            if not query or query.lower() in ["random", "kuch bhi", "anything", "surprise me", 
                                               "new", "latest", "trending", "naya", "new song", 
                                               "latest song", "trending song"]:
                return self.play_trending_song(language)
            
            # Add language context if specified
            if language and language.lower() != "hindi":
                search_query = f"{query} {language} song"
            else:
                search_query = f"{query} hindi song"
            
            print(f"🎵 Playing: {search_query}")
            return self._play_on_youtube(search_query)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def play_hindi_song(self, song_name=""):
        """
        Play a Hindi song or random popular song with AUTO-PLAY
        """
        try:
            if not song_name:
                song = random.choice(self.POPULAR_HINDI_SONGS)
                print(f"🎵 Playing random Hindi song: {song}")
            else:
                song = f"{song_name} hindi song"
                print(f"🎵 Playing: {song}")
            
            return self._play_on_youtube(song)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def play_playlist(self, playlist_type, language="hindi"):
        """
        Play a music playlist/mix with AUTO-PLAY
        """
        try:
            search_query = f"{playlist_type} {language} songs playlist"
            print(f"🎵 Playing playlist: {search_query}")
            return self._play_on_youtube(search_query)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def _play_on_youtube(self, query):
        """
        Internal method to play on YouTube with AUTO-PLAY support
        Uses Selenium to automatically click and play the first video
        """
        try:
            # Try Selenium auto-play first (best experience)
            selenium_result = self._auto_play_with_selenium(query)
            if selenium_result:
                return selenium_result
            
            # Fallback 1: Try pywhatkit
            print("🔄 Trying pywhatkit method...")
            try:
                import pywhatkit as kit
                
                print(f"🔍 Searching YouTube: {query}")
                
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
                    "action": "play_music", 
                    "query": query,
                    "platform": sys.platform,
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
                "action": "play_music_fallback", 
                "query": query,
                "note": "YouTube search opened, click first video to play"
            })
                
        except Exception as e:
            print(f"❌ YouTube Error: {e}")
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

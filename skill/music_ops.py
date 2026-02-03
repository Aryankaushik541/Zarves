import webbrowser
import json
import sys
import random
import requests
import time
import threading
import atexit
import os
import subprocess
import platform
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

    def _find_chrome_path(self):
        """
        Find Chrome/Chromium executable path based on OS
        """
        system = platform.system()
        
        if system == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            ]
        elif system == "Darwin":  # macOS
            paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        else:  # Linux
            paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
                "/snap/bin/chromium",
            ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        return None

    def _open_youtube_subprocess(self, query):
        """
        Open YouTube in Chrome using subprocess - browser stays open permanently
        This is the MOST RELIABLE method as Chrome runs as independent process
        """
        try:
            chrome_path = self._find_chrome_path()
            
            if not chrome_path:
                print("⚠️  Chrome not found, using default browser...")
                return None
            
            print(f"🌐 Found Chrome at: {chrome_path}")
            
            # Build YouTube URL
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            
            print(f"🎬 Opening YouTube in independent Chrome process...")
            
            # Launch Chrome as independent process
            if platform.system() == "Windows":
                # Windows: Use CREATE_NEW_PROCESS_GROUP to detach
                subprocess.Popen(
                    [chrome_path, "--new-window", "--start-maximized", url],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Linux/Mac: Use nohup-like approach
                subprocess.Popen(
                    [chrome_path, "--new-window", "--start-maximized", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True  # Detach from parent process
                )
            
            print("✅ Chrome opened as independent process!")
            print("🎵 Browser will stay open permanently - close it manually when done")
            print("💡 Click the first video to play")
            
            return json.dumps({
                "status": "success",
                "action": "open_youtube_subprocess",
                "query": query,
                "method": "subprocess_independent",
                "chrome_path": chrome_path,
                "note": "Chrome opened as independent process. Click first video to play. Browser will stay open until you close it manually."
            })
            
        except Exception as e:
            print(f"⚠️  Subprocess method failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _auto_play_with_selenium(self, query):
        """
        Use Selenium to automatically click and play the first video
        Falls back to subprocess if Selenium fails
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            print("🎬 Opening YouTube with auto-play in GUI mode...")
            
            # Setup Chrome options for VISIBLE GUI MODE
            chrome_options = Options()
            
            # CRITICAL: Ensure GUI mode (NOT headless)
            chrome_options.headless = False
            
            # Window settings for visible browser
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # CRITICAL: This keeps Chrome open even after driver quits
            chrome_options.add_experimental_option("detach", True)
            
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable automation flags
            chrome_options.add_argument("--disable-infobars")
            
            # Force GUI display (especially for Linux/WSL)
            if sys.platform.startswith('linux'):
                if 'DISPLAY' not in os.environ:
                    os.environ['DISPLAY'] = ':0'
                    print("🖥️  Set DISPLAY=:0 for GUI mode")
            
            # Disable sandbox for better compatibility
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--enable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            print(f"🖥️  Platform: {sys.platform}")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Store driver reference
            self.active_drivers.append(driver)
            
            print("✅ Chrome browser opened in GUI mode!")
            
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
                
                # Scroll to element to ensure it's visible
                driver.execute_script("arguments[0].scrollIntoView(true);", video)
                time.sleep(0.5)
                
                video.click()
                video_clicked = True
                
            except:
                # Method 2: Try alternative selector
                try:
                    video = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a#thumbnail")
                    ))
                    print("✅ Found video (alt method), clicking to play...")
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", video)
                    time.sleep(0.5)
                    
                    video.click()
                    video_clicked = True
                except Exception as e:
                    print(f"⚠️  Could not auto-click: {e}")
                    print("📺 YouTube is open - manually click first video")
            
            # Wait for video to start
            if video_clicked:
                time.sleep(3)
                print("✅ Video is playing in GUI browser!")
            
            print("🎵 Browser window will stay open until you close it manually.")
            
            # DON'T quit driver - detach option should keep it open
            
            return json.dumps({
                "status": "success",
                "action": "auto_play_music",
                "query": query,
                "method": "selenium_gui_detached",
                "note": "Browser opened with detach mode and will stay open."
            })
            
        except ImportError as ie:
            print(f"⚠️  Selenium not available: {ie}")
            print("💡 Install with: pip install selenium webdriver-manager")
            return None
        except Exception as e:
            print(f"⚠️  Selenium auto-play failed: {e}")
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
        Internal method to play on YouTube with multiple fallback methods
        Priority: Subprocess > Selenium > Pywhatkit > Webbrowser
        """
        try:
            # Method 1: Subprocess (MOST RELIABLE - Chrome stays open permanently)
            print("🚀 Trying subprocess method (most reliable)...")
            subprocess_result = self._open_youtube_subprocess(query)
            if subprocess_result:
                return subprocess_result
            
            # Method 2: Selenium auto-play
            print("🔄 Trying Selenium auto-play...")
            selenium_result = self._auto_play_with_selenium(query)
            if selenium_result:
                return selenium_result
            
            # Method 3: Pywhatkit
            print("🔄 Trying pywhatkit method...")
            try:
                import pywhatkit as kit
                print(f"🔍 Searching YouTube: {query}")
                kit.playonyt(query, open_web=True)
                time.sleep(2)
                print("✅ YouTube opened (manual click needed)")
                
                return json.dumps({
                    "status": "success", 
                    "action": "play_music_pywhatkit", 
                    "query": query,
                    "note": "Video search opened, click first result to play"
                })
            except ImportError:
                print("⚠️  pywhatkit not found")
                pass
            
            # Method 4: Direct browser (final fallback)
            print("🔄 Using default browser fallback...")
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(url)
            
            print("✅ YouTube opened in default browser")
            
            return json.dumps({
                "status": "success", 
                "action": "play_music_webbrowser", 
                "query": query,
                "note": "YouTube search opened in default browser, click first video to play"
            })
                
        except Exception as e:
            print(f"❌ YouTube Error: {e}")
            return json.dumps({"status": "error", "error": str(e)})

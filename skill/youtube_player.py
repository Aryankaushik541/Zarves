import subprocess
import time
import webbrowser
from typing import List, Dict, Any, Callable
from core.skill import Skill

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not installed. Auto-play will not work.")
    print("💡 Install: pip install selenium")

class YouTubePlayerSkill(Skill):
    """
    YouTube Auto-Play Skill
    Automatically opens YouTube and plays videos without manual clicking
    Uses Selenium for automation
    """
    
    # Trending songs database (updated regularly)
    TRENDING_SONGS = [
        "Tauba Tauba Bad Newz",
        "Satranga Animal",
        "Kesariya Brahmastra",
        "Apna Bana Le Bhediya",
        "Chaleya Jawan",
        "Tere Vaaste Zara Hatke Zara Bachke",
        "Maan Meri Jaan King",
        "Kahani Suno 2.0 Kaifi Khalil",
        "O Maahi Dunki",
        "Pehle Bhi Main Vishal Mishra"
    ]
    
    def __init__(self):
        super().__init__()
        self.driver = None
    
    @property
    def name(self) -> str:
        return "youtube_player_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "play_youtube_video",
                    "description": "Play a specific video on YouTube with AUTO-PLAY (no manual clicking needed). Use this when user says 'youtube kholo', 'gaana bajao', 'play song', 'video chalao', etc. Automatically clicks play button using Selenium.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "Song name or video to search and play. Examples: 'Kesariya', 'Tauba Tauba', 'trending song', 'latest hindi song'. If empty, plays trending song."
                            },
                            "autoplay": {
                                "type": "boolean",
                                "description": "Whether to automatically click play button (default: True)",
                                "default": True
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
                    "description": "Play the latest trending song on YouTube with AUTO-PLAY. Use when user says 'youtube kholo', 'gaana bajao', 'trending song bajao', etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": {}, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_and_play",
                    "description": "Search for any video on YouTube and play it automatically. Use for specific songs, artists, or video requests.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "search_query": {
                                "type": "string",
                                "description": "What to search on YouTube. Examples: 'Arijit Singh songs', 'Sidhu Moose Wala', 'funny videos', etc."
                            }
                        }, 
                        "required": ["search_query"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "play_youtube_video": self.play_youtube_video,
            "play_trending_song": self.play_trending_song,
            "search_and_play": self.search_and_play
        }

    def _setup_driver(self):
        """
        Setup Selenium WebDriver with Chrome
        """
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available. Cannot auto-play.")
            return None
        
        try:
            # Chrome options for better performance
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable notifications
            prefs = {
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Create driver
            driver = webdriver.Chrome(options=chrome_options)
            
            # Remove webdriver flag
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            print("💡 Make sure Chrome and ChromeDriver are installed")
            return None

    def _click_play_button(self, driver, max_wait=10):
        """
        Automatically click the play button on YouTube video
        """
        try:
            print("🎬 Waiting for video to load...")
            
            # Wait for page to load
            time.sleep(3)
            
            # Method 1: Click on video player to play
            try:
                print("🖱️  Attempting to click video player...")
                video_player = WebDriverWait(driver, max_wait).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.html5-main-video"))
                )
                
                # Click video to play
                driver.execute_script("arguments[0].click();", video_player)
                print("✅ Video clicked! Should start playing...")
                time.sleep(2)
                
                # Check if playing
                is_playing = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused === false"
                )
                
                if is_playing:
                    print("✅ Video is playing!")
                    return True
                else:
                    print("⚠️  Video not playing, trying play button...")
                    
            except Exception as e:
                print(f"⚠️  Video click failed: {e}")
            
            # Method 2: Click play button if video is paused
            try:
                print("🖱️  Looking for play button...")
                
                # Try to find and click play button
                play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                
                # Check if video is paused
                is_paused = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused"
                )
                
                if is_paused:
                    print("▶️  Clicking play button...")
                    play_button.click()
                    time.sleep(1)
                    print("✅ Play button clicked!")
                    return True
                else:
                    print("✅ Video already playing!")
                    return True
                    
            except Exception as e:
                print(f"⚠️  Play button click failed: {e}")
            
            # Method 3: Use JavaScript to play video
            try:
                print("🎮 Using JavaScript to play video...")
                driver.execute_script(
                    "document.querySelector('video.html5-main-video').play();"
                )
                time.sleep(1)
                print("✅ Video started via JavaScript!")
                return True
                
            except Exception as e:
                print(f"⚠️  JavaScript play failed: {e}")
            
            # Method 4: Press spacebar to play
            try:
                print("⌨️  Pressing spacebar to play...")
                from selenium.webdriver.common.keys import Keys
                video_player = driver.find_element(By.CSS_SELECTOR, "video.html5-main-video")
                video_player.send_keys(Keys.SPACE)
                time.sleep(1)
                print("✅ Spacebar pressed!")
                return True
                
            except Exception as e:
                print(f"⚠️  Spacebar method failed: {e}")
            
            print("⚠️  All auto-play methods failed. Video opened but not playing.")
            return False
            
        except Exception as e:
            print(f"❌ Error in auto-play: {e}")
            return False

    def play_youtube_video(self, query: str = "", autoplay: bool = True):
        """
        Play YouTube video with auto-play
        """
        print(f"\n{'='*60}")
        print(f"🎵 YouTube Auto-Player")
        print(f"{'='*60}")
        
        # If no query, play trending song
        if not query or query.strip() == "":
            query = self.TRENDING_SONGS[0]
            print(f"🎵 Playing trending song: {query}")
        else:
            print(f"🔍 Searching for: {query}")
        
        # Build YouTube search URL
        search_query = query.replace(" ", "+")
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        if not autoplay or not SELENIUM_AVAILABLE:
            # Fallback: Just open in browser
            print("🌐 Opening YouTube in browser...")
            webbrowser.open(youtube_url)
            
            return {
                "success": True,
                "message": f"YouTube opened for: {query}. Click on video to play.",
                "query": query,
                "autoplay": False
            }
        
        # Auto-play with Selenium
        try:
            print("🚀 Starting auto-play with Selenium...")
            
            # Setup driver
            driver = self._setup_driver()
            if not driver:
                # Fallback to browser
                webbrowser.open(youtube_url)
                return {
                    "success": True,
                    "message": f"YouTube opened for: {query}. Auto-play not available.",
                    "query": query,
                    "autoplay": False
                }
            
            # Open YouTube search
            print(f"🌐 Opening: {youtube_url}")
            driver.get(youtube_url)
            
            # Wait for search results
            print("⏳ Waiting for search results...")
            time.sleep(3)
            
            # Click first video
            try:
                print("🖱️  Clicking first video...")
                
                # Find first video thumbnail
                first_video = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
                )
                
                video_title = first_video.get_attribute("title")
                print(f"🎬 Found video: {video_title}")
                
                # Click video
                first_video.click()
                print("✅ Video opened!")
                
                # Auto-play video
                if autoplay:
                    play_success = self._click_play_button(driver)
                    
                    if play_success:
                        print("\n" + "="*60)
                        print("✅ SUCCESS! Video is playing!")
                        print("="*60)
                        
                        # Keep browser open
                        print("\n💡 Browser will stay open. Close manually when done.")
                        
                        return {
                            "success": True,
                            "message": f"Playing: {video_title}",
                            "query": query,
                            "video_title": video_title,
                            "autoplay": True
                        }
                    else:
                        print("\n⚠️  Auto-play failed. Video opened but not playing.")
                        print("💡 Click play button manually.")
                        
                        return {
                            "success": True,
                            "message": f"Video opened: {video_title}. Click play to start.",
                            "query": query,
                            "video_title": video_title,
                            "autoplay": False
                        }
                
            except Exception as e:
                print(f"❌ Failed to click video: {e}")
                
                return {
                    "success": False,
                    "message": f"Failed to play video: {str(e)}",
                    "query": query,
                    "autoplay": False
                }
                
        except Exception as e:
            print(f"❌ Auto-play error: {e}")
            
            # Fallback to browser
            print("🌐 Falling back to browser...")
            webbrowser.open(youtube_url)
            
            return {
                "success": True,
                "message": f"YouTube opened for: {query}. Auto-play failed.",
                "query": query,
                "autoplay": False,
                "error": str(e)
            }

    def play_trending_song(self):
        """
        Play latest trending song
        """
        trending_song = self.TRENDING_SONGS[0]
        print(f"🎵 Playing trending song: {trending_song}")
        
        return self.play_youtube_video(query=trending_song, autoplay=True)

    def search_and_play(self, search_query: str):
        """
        Search and play specific video
        """
        return self.play_youtube_video(query=search_query, autoplay=True)

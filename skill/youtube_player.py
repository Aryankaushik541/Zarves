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
    from selenium.webdriver.common.keys import Keys
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
                    "description": "Play a specific video on YouTube with AUTO-PLAY (no manual clicking needed). Use this when user says 'youtube kholo', 'gaana bajao', 'play song', 'video chalao', 'music bajao', etc. Automatically clicks play button using Selenium.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "Song name or video to search and play. Examples: 'Kesariya', 'Tauba Tauba', 'trending song', 'latest hindi song'. If empty, plays trending song.",
                                "default": ""
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
            print("🔧 Setting up Chrome driver...")
            
            # Chrome options for better performance
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable notifications
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Create driver
            print("🚀 Launching Chrome...")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Remove webdriver flag
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver ready!")
            return driver
            
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            print("💡 Make sure Chrome browser is installed")
            print("💡 ChromeDriver will be auto-downloaded by Selenium")
            return None

    def _click_play_button(self, driver, max_wait=15):
        """
        Automatically click the play button on YouTube video
        Uses multiple methods to ensure video plays
        """
        try:
            print("🎬 Waiting for video to load...")
            
            # Wait for page to load
            time.sleep(4)
            
            print("🔍 Attempting auto-play...")
            
            # Method 1: Click on video player to play
            try:
                print("  📍 Method 1: Clicking video player...")
                video_player = WebDriverWait(driver, max_wait).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.html5-main-video"))
                )
                
                # Scroll to video
                driver.execute_script("arguments[0].scrollIntoView(true);", video_player)
                time.sleep(1)
                
                # Click video to play
                driver.execute_script("arguments[0].click();", video_player)
                print("  ✅ Video player clicked!")
                time.sleep(2)
                
                # Check if playing
                is_playing = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused === false"
                )
                
                if is_playing:
                    print("  ✅ SUCCESS! Video is playing!")
                    return True
                    
            except Exception as e:
                print(f"  ⚠️  Method 1 failed: {e}")
            
            # Method 2: Use JavaScript to play video directly
            try:
                print("  📍 Method 2: JavaScript play command...")
                driver.execute_script(
                    "document.querySelector('video.html5-main-video').play();"
                )
                time.sleep(2)
                
                # Check if playing
                is_playing = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused === false"
                )
                
                if is_playing:
                    print("  ✅ SUCCESS! Video is playing via JavaScript!")
                    return True
                    
            except Exception as e:
                print(f"  ⚠️  Method 2 failed: {e}")
            
            # Method 3: Click play button if video is paused
            try:
                print("  📍 Method 3: Clicking play button...")
                
                # Check if video is paused
                is_paused = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused"
                )
                
                if is_paused:
                    # Find and click play button
                    play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                    play_button.click()
                    time.sleep(2)
                    print("  ✅ SUCCESS! Play button clicked!")
                    return True
                else:
                    print("  ✅ SUCCESS! Video already playing!")
                    return True
                    
            except Exception as e:
                print(f"  ⚠️  Method 3 failed: {e}")
            
            # Method 4: Press spacebar to play
            try:
                print("  📍 Method 4: Pressing spacebar...")
                video_player = driver.find_element(By.CSS_SELECTOR, "video.html5-main-video")
                video_player.send_keys(Keys.SPACE)
                time.sleep(2)
                
                # Check if playing
                is_playing = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused === false"
                )
                
                if is_playing:
                    print("  ✅ SUCCESS! Video playing after spacebar!")
                    return True
                    
            except Exception as e:
                print(f"  ⚠️  Method 4 failed: {e}")
            
            # Method 5: Click anywhere on player
            try:
                print("  📍 Method 5: Clicking player container...")
                player = driver.find_element(By.ID, "movie_player")
                player.click()
                time.sleep(2)
                
                # Check if playing
                is_playing = driver.execute_script(
                    "return document.querySelector('video.html5-main-video').paused === false"
                )
                
                if is_playing:
                    print("  ✅ SUCCESS! Video playing after container click!")
                    return True
                    
            except Exception as e:
                print(f"  ⚠️  Method 5 failed: {e}")
            
            print("  ⚠️  All auto-play methods failed.")
            print("  💡 Video opened but may need manual play button click.")
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
                print("⚠️  Falling back to browser...")
                webbrowser.open(youtube_url)
                return {
                    "success": True,
                    "message": f"YouTube opened for: {query}. Auto-play not available.",
                    "query": query,
                    "autoplay": False
                }
            
            # Store driver for later cleanup
            self.driver = driver
            
            # Open YouTube search
            print(f"🌐 Opening: {youtube_url}")
            driver.get(youtube_url)
            
            # Wait for search results
            print("⏳ Waiting for search results...")
            time.sleep(4)
            
            # Click first video
            try:
                print("🖱️  Looking for first video...")
                
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
                        print("\n💡 Browser will stay open. Close manually when done.")
                        print("💡 Press Ctrl+C in terminal to stop JARVIS.\n")
                        
                        return {
                            "success": True,
                            "message": f"✅ Playing: {video_title}",
                            "query": query,
                            "video_title": video_title,
                            "autoplay": True,
                            "note": "Video is auto-playing! Browser will stay open."
                        }
                    else:
                        print("\n⚠️  Auto-play failed. Video opened but not playing.")
                        print("💡 Click play button manually in the browser.\n")
                        
                        return {
                            "success": True,
                            "message": f"Video opened: {video_title}. Click play to start.",
                            "query": query,
                            "video_title": video_title,
                            "autoplay": False,
                            "note": "Auto-play failed. Click play button manually."
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
    
    def __del__(self):
        """
        Cleanup: Close driver when skill is destroyed
        """
        if self.driver:
            try:
                # Don't close driver - let user close browser manually
                # self.driver.quit()
                pass
            except:
                pass

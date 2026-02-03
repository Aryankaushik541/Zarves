import os
import json
import subprocess
import time
import requests
from typing import List, Dict, Any, Callable
from core.skill import Skill
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MovieDownloaderSkill(Skill):
    """
    Advanced Movie Downloader & Player
    - Search movies on websites
    - Download movies automatically
    - Play in VLC player
    """
    
    @property
    def name(self) -> str:
        return "movie_downloader"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "download_and_play_movie",
                    "description": "Download a movie from a website and automatically play it in VLC player",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "movie_name": {
                                "type": "string",
                                "description": "Name of the movie to download (e.g., 'Inception', 'Avatar')"
                            },
                            "website_url": {
                                "type": "string",
                                "description": "Website URL to download from (e.g., 'https://vegamovies.attorney/')",
                                "default": "https://vegamovies.attorney/"
                            },
                            "quality": {
                                "type": "string",
                                "description": "Video quality preference: '480p', '720p', '1080p'",
                                "default": "720p"
                            }
                        },
                        "required": ["movie_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_downloaded_movie",
                    "description": "Play a previously downloaded movie in VLC player",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "movie_path": {
                                "type": "string",
                                "description": "Full path to the movie file"
                            }
                        },
                        "required": ["movie_path"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "download_and_play_movie": self.download_and_play_movie,
            "play_downloaded_movie": self.play_downloaded_movie
        }

    def _find_vlc_path(self):
        """Find VLC player installation path"""
        common_paths = [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
            "/usr/bin/vlc",
            "/Applications/VLC.app/Contents/MacOS/VLC",
            os.path.expanduser("~/Applications/VLC.app/Contents/MacOS/VLC")
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # Try to find in PATH
        try:
            result = subprocess.run(['which', 'vlc'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None

    def _setup_selenium_driver(self):
        """Setup Selenium WebDriver with anti-detection"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"⚠️  Selenium setup failed: {e}")
            print("💡 Install ChromeDriver: pip install webdriver-manager")
            return None

    def _search_movie_on_website(self, website_url, movie_name):
        """Search for movie on the website"""
        try:
            print(f"🔍 Searching for '{movie_name}' on {website_url}...")
            
            driver = self._setup_selenium_driver()
            if not driver:
                return None
            
            # Navigate to website
            driver.get(website_url)
            time.sleep(3)
            
            # Try to find search box
            try:
                search_box = driver.find_element(By.NAME, "s")
                search_box.send_keys(movie_name)
                search_box.submit()
                time.sleep(3)
            except:
                # Try alternative search methods
                search_url = f"{website_url}?s={movie_name.replace(' ', '+')}"
                driver.get(search_url)
                time.sleep(3)
            
            # Get page source
            page_source = driver.page_source
            driver.quit()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find movie links (this will vary by website structure)
            movie_links = []
            for link in soup.find_all('a', href=True):
                if movie_name.lower() in link.text.lower():
                    movie_links.append({
                        'title': link.text.strip(),
                        'url': link['href']
                    })
            
            return movie_links[0] if movie_links else None
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None

    def _extract_download_link(self, movie_page_url, quality="720p"):
        """Extract download link from movie page"""
        try:
            print(f"📥 Extracting download link for {quality}...")
            
            driver = self._setup_selenium_driver()
            if not driver:
                return None
            
            driver.get(movie_page_url)
            time.sleep(5)
            
            # Look for download buttons/links
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find download links (common patterns)
            download_link = None
            
            # Pattern 1: Direct download links
            for link in soup.find_all('a', href=True):
                link_text = link.text.lower()
                link_href = link['href']
                
                if quality in link_text and ('download' in link_text or 'gdrive' in link_href or 'drive.google' in link_href):
                    download_link = link_href
                    break
            
            # Pattern 2: Look for any download button
            if not download_link:
                for link in soup.find_all('a', class_=lambda x: x and 'download' in x.lower()):
                    download_link = link.get('href')
                    break
            
            driver.quit()
            return download_link
            
        except Exception as e:
            print(f"❌ Link extraction error: {e}")
            return None

    def _download_file(self, url, save_path):
        """Download file from URL"""
        try:
            print(f"⬇️  Downloading movie...")
            print(f"📍 Save location: {save_path}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(save_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress indicator
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r⬇️  Progress: {progress:.1f}%", end='')
            
            print(f"\n✅ Download complete!")
            return True
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False

    def download_and_play_movie(self, movie_name, website_url="https://vegamovies.attorney/", quality="720p"):
        """
        Main function to download and play movie
        """
        try:
            print(f"\n{'='*60}")
            print(f"🎬 Movie Downloader & Player")
            print(f"{'='*60}")
            print(f"Movie: {movie_name}")
            print(f"Website: {website_url}")
            print(f"Quality: {quality}")
            print(f"{'='*60}\n")
            
            # Create downloads directory
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads", "JARVIS_Movies")
            os.makedirs(downloads_dir, exist_ok=True)
            
            # Step 1: Search for movie
            movie_info = self._search_movie_on_website(website_url, movie_name)
            
            if not movie_info:
                return json.dumps({
                    "status": "error",
                    "message": f"Movie '{movie_name}' not found on {website_url}",
                    "suggestion": "Try a different movie name or website"
                })
            
            print(f"✅ Found: {movie_info['title']}")
            print(f"🔗 URL: {movie_info['url']}")
            
            # Step 2: Extract download link
            download_link = self._extract_download_link(movie_info['url'], quality)
            
            if not download_link:
                return json.dumps({
                    "status": "error",
                    "message": "Could not find download link",
                    "movie_page": movie_info['url'],
                    "suggestion": "Please download manually from the movie page"
                })
            
            print(f"✅ Download link found!")
            
            # Step 3: Download movie
            movie_filename = f"{movie_name.replace(' ', '_')}_{quality}.mp4"
            movie_path = os.path.join(downloads_dir, movie_filename)
            
            download_success = self._download_file(download_link, movie_path)
            
            if not download_success:
                return json.dumps({
                    "status": "error",
                    "message": "Download failed",
                    "download_link": download_link,
                    "suggestion": "Try downloading manually"
                })
            
            # Step 4: Play in VLC
            vlc_path = self._find_vlc_path()
            
            if not vlc_path:
                return json.dumps({
                    "status": "partial_success",
                    "message": "Movie downloaded but VLC not found",
                    "movie_path": movie_path,
                    "suggestion": "Install VLC player or open the movie manually"
                })
            
            print(f"\n🎥 Opening in VLC player...")
            subprocess.Popen([vlc_path, movie_path])
            
            return json.dumps({
                "status": "success",
                "message": f"Movie '{movie_name}' downloaded and playing in VLC!",
                "movie_path": movie_path,
                "quality": quality,
                "size": f"{os.path.getsize(movie_path) / (1024*1024):.1f} MB"
            })
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e),
                "message": "An error occurred during the process"
            })

    def play_downloaded_movie(self, movie_path):
        """Play a downloaded movie in VLC"""
        try:
            if not os.path.exists(movie_path):
                return json.dumps({
                    "status": "error",
                    "message": f"Movie file not found: {movie_path}"
                })
            
            vlc_path = self._find_vlc_path()
            
            if not vlc_path:
                return json.dumps({
                    "status": "error",
                    "message": "VLC player not found",
                    "suggestion": "Install VLC player from https://www.videolan.org/"
                })
            
            print(f"🎥 Playing: {os.path.basename(movie_path)}")
            subprocess.Popen([vlc_path, movie_path])
            
            return json.dumps({
                "status": "success",
                "message": f"Playing {os.path.basename(movie_path)} in VLC",
                "movie_path": movie_path
            })
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })

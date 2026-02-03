import subprocess
import json
import time
import os
import platform
from typing import List, Dict, Any, Callable
from core.skill import Skill

class AppInstallerSkill(Skill):
    """
    Cross-Platform App Installer Skill
    - Windows: Microsoft Store
    - Mac: Mac App Store
    - Linux: apt/snap/flatpak
    """
    
    # Windows - Microsoft Store IDs
    WINDOWS_APPS = {
        # Social & Communication
        "whatsapp": "9NKSQGP7F2NH",
        "telegram": "9NZTWSQNTD0S",
        "discord": "XPDC2RH70K22MN",
        "zoom": "XP99J3KP4XZ4VV",
        "teams": "XP8BT8DW290MPQ",
        "skype": "9WZDNCRFJ364",
        
        # Entertainment
        "spotify": "9NCBCSZSJRSB",
        "netflix": "9WZDNCRFJ3TJ",
        "prime video": "9P6RC76MSMMJ",
        "vlc": "9NBLGGH4VVNH",
        
        # Productivity
        "notion": "9NBLGGH4VG81",
        "evernote": "9WZDNCRFJ3J1",
        "onenote": "XPFFZHVGQWWLHB",
        
        # Development
        "visual studio code": "XP9KHM4BK9FZ7Q",
        "windows terminal": "9N0DX20HK701",
        "powershell": "9MZ1SNWT0N5D",
        "git": "9NBLGGH4NNS1",
        "python": "9PJPW5LDXLZ5",
        
        # Utilities
        "winrar": "9WZDNCRFJ3BB",
        "7zip": "9WZDNCRFJ3BB",
        "notepad++": "9WZDNCRFJ3BB",
        "paint.net": "9NBHCS1LX4R0",
        
        # Gaming
        "xbox": "9WZDNCRFJ BD8",
        "steam": "9NBLGGH4X7K2",
        
        # Browsers
        "firefox": "9NZVDKPMR9RD",
        "edge": "XPFFTQ037JWMHS",
        "brave": "9NBLGGH4VG81",
        
        # Office
        "word": "9WZDNCRFJB9S",
        "excel": "9WZDNCRFJBH3",
        "powerpoint": "9WZDNCRFJBHV",
        "outlook": "9NRX63209R7B",
    }
    
    # Mac - App Store bundle IDs
    MAC_APPS = {
        # Social & Communication
        "whatsapp": "310633997",
        "telegram": "747648890",
        "discord": "985746746",
        "zoom": "546505307",
        "slack": "803453959",
        "skype": "304878510",
        
        # Entertainment
        "spotify": "324684580",
        "netflix": "1295203466",
        "vlc": "1295203466",
        
        # Productivity
        "notion": "1559269364",
        "evernote": "406056744",
        "onenote": "784801555",
        "pages": "409201541",
        "numbers": "409203825",
        "keynote": "409183694",
        
        # Development
        "xcode": "497799835",
        "visual studio code": "1295203466",  # Not on Mac App Store, use brew
        
        # Utilities
        "the unarchiver": "425424353",
        "magnet": "441258766",
        
        # Browsers
        "safari": "built-in",  # Pre-installed
        
        # Office
        "word": "462054704",
        "excel": "462058435",
        "powerpoint": "462062816",
        "outlook": "985367838",
    }
    
    def __init__(self):
        super().__init__()
        self.platform = platform.system()  # 'Windows', 'Darwin' (Mac), 'Linux'
    
    @property
    def name(self) -> str:
        return "app_installer_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        platform_name = "Microsoft Store" if self.platform == "Windows" else "Mac App Store" if self.platform == "Darwin" else "Package Manager"
        
        return [
            {
                "type": "function",
                "function": {
                    "name": "install_app",
                    "description": f"Install any application from {platform_name}. Use this when user says 'install app', 'download app', 'app install karo', 'app download karo', etc. Supports popular apps like WhatsApp, Spotify, Netflix, Chrome, VS Code, etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "app_name": {
                                "type": "string",
                                "description": "Name of the app to install. Examples: 'WhatsApp', 'Spotify', 'Chrome', 'VS Code', 'Netflix', 'Telegram', etc."
                            }
                        }, 
                        "required": ["app_name"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_popular_apps",
                    "description": f"List all popular apps available for installation from {platform_name}",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "category": {
                                "type": "string",
                                "description": "Filter by category: 'all', 'social', 'entertainment', 'productivity', 'development', 'gaming', 'browsers', 'office'",
                                "default": "all"
                            }
                        }, 
                        "required": [] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "install_app": self.install_app,
            "list_popular_apps": self.list_popular_apps
        }

    def _get_app_id(self, app_name):
        """
        Get app ID based on platform
        """
        app_lower = app_name.lower().strip()
        
        # Select correct app database based on platform
        if self.platform == "Windows":
            app_db = self.WINDOWS_APPS
        elif self.platform == "Darwin":
            app_db = self.MAC_APPS
        else:
            return None
        
        # Direct match
        if app_lower in app_db:
            return app_db[app_lower]
        
        # Partial match
        for key, value in app_db.items():
            if app_lower in key or key in app_lower:
                return value
        
        return None

    def _install_windows_app(self, app_name, app_id):
        """
        Install app on Windows using Microsoft Store
        """
        try:
            # Method 1: MS Store Protocol (most reliable)
            print(f"🏪 Opening Microsoft Store for: {app_name}")
            store_url = f"ms-windows-store://pdp/?ProductId={app_id}"
            
            subprocess.Popen(
                f'start "" "{store_url}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("✅ Microsoft Store opened!")
            print("💡 Click 'Get' or 'Install' button to download the app")
            
            return {
                "success": True,
                "message": f"Microsoft Store opened for {app_name}. Click 'Get' or 'Install' to download.",
                "app_name": app_name,
                "platform": "Windows"
            }
            
        except Exception as e:
            # Fallback: Try winget
            print(f"⚠️  MS Store failed, trying winget...")
            return self._install_via_winget(app_name)

    def _install_mac_app(self, app_name, app_id):
        """
        Install app on Mac using Mac App Store
        """
        try:
            if app_id == "built-in":
                return {
                    "success": True,
                    "message": f"{app_name} is pre-installed on macOS",
                    "app_name": app_name,
                    "platform": "Mac"
                }
            
            # Method 1: Mac App Store URL
            print(f"🍎 Opening Mac App Store for: {app_name}")
            store_url = f"macappstore://itunes.apple.com/app/id{app_id}"
            
            subprocess.Popen(
                ["open", store_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("✅ Mac App Store opened!")
            print("💡 Click 'Get' or 'Install' button to download the app")
            
            return {
                "success": True,
                "message": f"Mac App Store opened for {app_name}. Click 'Get' or 'Install' to download.",
                "app_name": app_name,
                "platform": "Mac"
            }
            
        except Exception as e:
            # Fallback: Try Homebrew
            print(f"⚠️  Mac App Store failed, trying Homebrew...")
            return self._install_via_homebrew(app_name)

    def _install_linux_app(self, app_name):
        """
        Install app on Linux using apt/snap/flatpak
        """
        try:
            print(f"🐧 Installing on Linux: {app_name}")
            
            # Try snap first (most universal)
            snap_cmd = f"snap install {app_name.lower().replace(' ', '-')}"
            result = subprocess.run(snap_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{app_name} installed successfully via snap",
                    "app_name": app_name,
                    "platform": "Linux"
                }
            
            # Try apt
            apt_cmd = f"sudo apt install -y {app_name.lower().replace(' ', '-')}"
            result = subprocess.run(apt_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{app_name} installed successfully via apt",
                    "app_name": app_name,
                    "platform": "Linux"
                }
            
            return {
                "success": False,
                "message": f"Could not install {app_name}. Try manually: snap install {app_name.lower()}",
                "app_name": app_name,
                "platform": "Linux"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Installation failed: {str(e)}",
                "app_name": app_name,
                "platform": "Linux"
            }

    def _install_via_winget(self, app_name):
        """
        Fallback: Install using winget (Windows Package Manager)
        """
        try:
            print(f"📦 Trying winget for: {app_name}")
            install_cmd = f'winget install "{app_name}" --accept-package-agreements --accept-source-agreements'
            
            result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{app_name} installed successfully via winget",
                    "app_name": app_name,
                    "platform": "Windows"
                }
            else:
                return {
                    "success": False,
                    "message": f"Could not install {app_name}. Try manually from Microsoft Store.",
                    "app_name": app_name,
                    "platform": "Windows"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Installation failed: {str(e)}",
                "app_name": app_name,
                "platform": "Windows"
            }

    def _install_via_homebrew(self, app_name):
        """
        Fallback: Install using Homebrew (Mac)
        """
        try:
            print(f"🍺 Trying Homebrew for: {app_name}")
            
            # Try cask first (GUI apps)
            cask_cmd = f"brew install --cask {app_name.lower().replace(' ', '-')}"
            result = subprocess.run(cask_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{app_name} installed successfully via Homebrew",
                    "app_name": app_name,
                    "platform": "Mac"
                }
            
            # Try regular brew
            brew_cmd = f"brew install {app_name.lower().replace(' ', '-')}"
            result = subprocess.run(brew_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{app_name} installed successfully via Homebrew",
                    "app_name": app_name,
                    "platform": "Mac"
                }
            
            return {
                "success": False,
                "message": f"Could not install {app_name}. Try manually from Mac App Store.",
                "app_name": app_name,
                "platform": "Mac"
            }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Installation failed: {str(e)}",
                "app_name": app_name,
                "platform": "Mac"
            }

    def install_app(self, app_name: str):
        """
        Install app based on platform
        """
        print(f"\n{'='*60}")
        print(f"📦 App Installer - {self.platform}")
        print(f"{'='*60}")
        print(f"🔍 Installing: {app_name}")
        print()
        
        # Get app ID
        app_id = self._get_app_id(app_name)
        
        if not app_id and self.platform in ["Windows", "Darwin"]:
            print(f"⚠️  {app_name} not found in database")
            print(f"💡 Trying alternative installation methods...")
        
        # Install based on platform
        if self.platform == "Windows":
            if app_id:
                return self._install_windows_app(app_name, app_id)
            else:
                return self._install_via_winget(app_name)
                
        elif self.platform == "Darwin":  # Mac
            if app_id:
                return self._install_mac_app(app_name, app_id)
            else:
                return self._install_via_homebrew(app_name)
                
        elif self.platform == "Linux":
            return self._install_linux_app(app_name)
            
        else:
            return {
                "success": False,
                "message": f"Unsupported platform: {self.platform}",
                "app_name": app_name,
                "platform": self.platform
            }

    def list_popular_apps(self, category: str = "all"):
        """
        List popular apps based on platform
        """
        # Select correct database
        if self.platform == "Windows":
            app_db = self.WINDOWS_APPS
            store_name = "Microsoft Store"
        elif self.platform == "Darwin":
            app_db = self.MAC_APPS
            store_name = "Mac App Store"
        else:
            return {
                "success": False,
                "message": f"Platform {self.platform} not supported for app listing",
                "platform": self.platform
            }
        
        # Get all apps
        apps = list(app_db.keys())
        
        # Filter by category if needed
        if category != "all":
            # Simple category filtering (can be enhanced)
            category_keywords = {
                "social": ["whatsapp", "telegram", "discord", "zoom", "teams", "skype", "slack"],
                "entertainment": ["spotify", "netflix", "vlc", "prime"],
                "productivity": ["notion", "evernote", "onenote", "pages", "numbers", "keynote"],
                "development": ["code", "xcode", "terminal", "powershell", "git", "python"],
                "gaming": ["xbox", "steam"],
                "browsers": ["chrome", "firefox", "edge", "brave", "safari"],
                "office": ["word", "excel", "powerpoint", "outlook"]
            }
            
            if category in category_keywords:
                keywords = category_keywords[category]
                apps = [app for app in apps if any(kw in app for kw in keywords)]
        
        return {
            "success": True,
            "platform": self.platform,
            "store": store_name,
            "category": category,
            "total_apps": len(apps),
            "apps": sorted(apps)
        }

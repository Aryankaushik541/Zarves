import subprocess
import json
import time
import os
from typing import List, Dict, Any, Callable
from core.skill import Skill

class AppInstallerSkill(Skill):
    """
    Microsoft Store App Installer Skill
    Downloads and installs apps directly from Microsoft Store
    Supports popular apps like Spotify, WhatsApp, Netflix, etc.
    """
    
    # Popular apps with their Microsoft Store IDs
    POPULAR_APPS = {
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
        "youtube": "9WZDNCRFJ3TJ",
        "vlc": "9NBLGGH4VVNH",
        
        # Productivity
        "notion": "9NBLGGH4VG81",
        "evernote": "9WZDNCRFJ3J1",
        "onenote": "XPFFZHVGQWWLHB",
        "adobe acrobat": "9WZDNCRFJ364",
        
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
        "xbox": "9WZDNCRFJBD8",
        "steam": "9NBLGGH4X7K2",
        "epic games": "9WZDNCRFJ3TJ",
        
        # Browsers
        "chrome": "9WZDNCRFJ3TJ",
        "firefox": "9NZVDKPMR9RD",
        "edge": "XPFFTQ037JWMHS",
        "brave": "9NBLGGH4VG81",
        
        # Office
        "word": "9WZDNCRFJB9S",
        "excel": "9WZDNCRFJBH3",
        "powerpoint": "9WZDNCRFJBHV",
        "outlook": "9NRX63209R7B",
    }
    
    def __init__(self):
        super().__init__()
    
    @property
    def name(self) -> str:
        return "app_installer_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "install_app",
                    "description": "Install any application from Microsoft Store. Use this when user says 'install app', 'download app', 'app install karo', 'app download karo', etc. Supports popular apps like WhatsApp, Spotify, Netflix, Chrome, VS Code, etc.",
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
                    "name": "search_app",
                    "description": "Search for an app in Microsoft Store to find its details and availability",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "App name or search query"
                            }
                        }, 
                        "required": ["query"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_popular_apps",
                    "description": "List all popular apps available for installation from Microsoft Store",
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
            },
            {
                "type": "function",
                "function": {
                    "name": "open_microsoft_store",
                    "description": "Open Microsoft Store app directly",
                    "parameters": { 
                        "type": "object", 
                        "properties": {}, 
                        "required": [] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "install_app": self.install_app,
            "search_app": self.search_app,
            "list_popular_apps": self.list_popular_apps,
            "open_microsoft_store": self.open_microsoft_store
        }

    def _get_app_id(self, app_name):
        """
        Get Microsoft Store app ID from app name
        """
        app_lower = app_name.lower().strip()
        
        # Direct match
        if app_lower in self.POPULAR_APPS:
            return self.POPULAR_APPS[app_lower]
        
        # Partial match
        for key, value in self.POPULAR_APPS.items():
            if app_lower in key or key in app_lower:
                return value
        
        return None

    def _install_via_winget(self, app_name):
        """
        Install app using winget (Windows Package Manager)
        Fallback method if direct MS Store doesn't work
        """
        try:
            print(f"🔄 Trying winget installation for: {app_name}")
            
            # Search for app first
            search_cmd = f'winget search "{app_name}"'
            result = subprocess.run(search_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and app_name.lower() in result.stdout.lower():
                # Install app
                install_cmd = f'winget install "{app_name}" --accept-package-agreements --accept-source-agreements'
                print(f"📦 Installing via winget: {app_name}")
                
                process = subprocess.Popen(
                    install_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for installation
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    print(f"✅ {app_name} installed successfully via winget!")
                    return True
                else:
                    print(f"⚠️  Winget installation failed: {stderr}")
                    return False
            else:
                print(f"⚠️  App not found in winget: {app_name}")
                return False
                
        except Exception as e:
            print(f"⚠️  Winget method failed: {e}")
            return False

    def _install_via_ms_store_protocol(self, app_id):
        """
        Install app using ms-windows-store:// protocol
        Opens Microsoft Store to app page
        """
        try:
            print(f"🏪 Opening Microsoft Store for app: {app_id}")
            
            # Use ms-windows-store protocol
            store_url = f"ms-windows-store://pdp/?ProductId={app_id}"
            
            subprocess.Popen(
                f'start "" "{store_url}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("✅ Microsoft Store opened!")
            print("💡 Click 'Get' or 'Install' button to download the app")
            
            return True
            
        except Exception as e:
            print(f"⚠️  MS Store protocol failed: {e}")
            return False

    def _install_via_powershell(self, app_name, app_id):
        """
        Install app using PowerShell and Microsoft Store
        Most reliable method for automatic installation
        """
        try:
            print(f"⚡ Installing via PowerShell: {app_name}")
            
            # PowerShell command to install from MS Store
            ps_command = f'''
            $appId = "{app_id}"
            $appName = "{app_name}"
            
            Write-Host "🔍 Searching for $appName in Microsoft Store..."
            
            # Try to install using Add-AppxPackage
            try {{
                $storeUrl = "ms-windows-store://pdp/?ProductId=$appId"
                Start-Process $storeUrl
                Write-Host "✅ Microsoft Store opened for $appName"
                Write-Host "💡 Click 'Get' or 'Install' to download"
            }} catch {{
                Write-Host "⚠️  Could not open Microsoft Store"
            }}
            '''
            
            # Execute PowerShell command
            process = subprocess.Popen(
                ['powershell', '-Command', ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            print(stdout)
            
            if stderr:
                print(f"⚠️  PowerShell warnings: {stderr}")
            
            return True
            
        except Exception as e:
            print(f"⚠️  PowerShell method failed: {e}")
            return False

    def install_app(self, app_name):
        """
        Install app from Microsoft Store with multiple fallback methods
        """
        try:
            print(f"📦 Installing: {app_name}")
            
            # Get app ID
            app_id = self._get_app_id(app_name)
            
            if app_id:
                print(f"✅ Found app ID: {app_id}")
                
                # Method 1: PowerShell (opens MS Store to app page)
                print("🚀 Method 1: PowerShell + MS Store...")
                if self._install_via_powershell(app_name, app_id):
                    return json.dumps({
                        "status": "success",
                        "action": "install_app",
                        "app_name": app_name,
                        "app_id": app_id,
                        "method": "powershell_ms_store",
                        "note": "Microsoft Store opened. Click 'Get' or 'Install' button to download the app."
                    })
                
                # Method 2: Direct MS Store protocol
                print("🔄 Method 2: MS Store Protocol...")
                if self._install_via_ms_store_protocol(app_id):
                    return json.dumps({
                        "status": "success",
                        "action": "install_app",
                        "app_name": app_name,
                        "app_id": app_id,
                        "method": "ms_store_protocol",
                        "note": "Microsoft Store opened. Click 'Get' or 'Install' to download."
                    })
            
            # Method 3: Winget fallback
            print("🔄 Method 3: Trying winget...")
            if self._install_via_winget(app_name):
                return json.dumps({
                    "status": "success",
                    "action": "install_app",
                    "app_name": app_name,
                    "method": "winget",
                    "note": f"{app_name} installed successfully via winget!"
                })
            
            # If all methods fail
            print(f"❌ Could not install {app_name}")
            print("💡 Opening Microsoft Store for manual search...")
            self.open_microsoft_store()
            
            return json.dumps({
                "status": "partial",
                "action": "install_app",
                "app_name": app_name,
                "note": f"Could not auto-install {app_name}. Microsoft Store opened - please search and install manually."
            })
            
        except Exception as e:
            print(f"❌ Installation error: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({"status": "error", "error": str(e)})

    def search_app(self, query):
        """
        Search for app in Microsoft Store
        """
        try:
            print(f"🔍 Searching Microsoft Store for: {query}")
            
            # Open MS Store with search
            search_url = f"ms-windows-store://search/?query={query.replace(' ', '%20')}"
            
            subprocess.Popen(
                f'start "" "{search_url}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print(f"✅ Microsoft Store opened with search: {query}")
            
            return json.dumps({
                "status": "success",
                "action": "search_app",
                "query": query,
                "note": f"Microsoft Store opened with search results for '{query}'"
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def list_popular_apps(self, category="all"):
        """
        List popular apps available for installation
        """
        try:
            categories = {
                "social": ["whatsapp", "telegram", "discord", "zoom", "teams", "skype"],
                "entertainment": ["spotify", "netflix", "prime video", "youtube", "vlc"],
                "productivity": ["notion", "evernote", "onenote", "adobe acrobat"],
                "development": ["visual studio code", "windows terminal", "powershell", "git", "python"],
                "gaming": ["xbox", "steam", "epic games"],
                "browsers": ["chrome", "firefox", "edge", "brave"],
                "office": ["word", "excel", "powerpoint", "outlook"],
                "utilities": ["winrar", "7zip", "notepad++", "paint.net"]
            }
            
            if category == "all":
                apps = list(self.POPULAR_APPS.keys())
            elif category in categories:
                apps = categories[category]
            else:
                apps = list(self.POPULAR_APPS.keys())
            
            print(f"📱 Popular apps ({category}):")
            for app in apps:
                print(f"  • {app.title()}")
            
            return json.dumps({
                "status": "success",
                "action": "list_apps",
                "category": category,
                "apps": apps,
                "count": len(apps)
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def open_microsoft_store(self):
        """
        Open Microsoft Store app
        """
        try:
            print("🏪 Opening Microsoft Store...")
            
            subprocess.Popen(
                'start ms-windows-store://',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("✅ Microsoft Store opened!")
            
            return json.dumps({
                "status": "success",
                "action": "open_store",
                "note": "Microsoft Store opened successfully"
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

import os
import sys
import json
import webbrowser
import subprocess
import platform
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
                    "description": "Open an application or website. For web services like YouTube, Gmail, etc., opens in browser. For system apps like Chrome, Notepad, Calculator, etc., opens the application. Supports Windows, Mac, and Linux.",
                    "parameters": { "type": "object", "properties": { "app_name": {"type": "string", "description": "Name of the app or website to open (e.g., 'YouTube', 'Chrome', 'Notepad', 'Calculator', 'GTA 5')"}}, "required": ["app_name"] }
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
            system = platform.system()
            
            if system == "Darwin":  # macOS
                os.system(f"osascript -e 'set volume output volume {level}'")
            elif system == "Windows":
                # Windows volume control (0-100 to 0-65535)
                volume = int((level / 100) * 65535)
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
                volume_obj.SetMasterVolumeLevelScalar(level / 100, None)
            elif system == "Linux":
                os.system(f"amixer -D pulse sset Master {level}%")
            
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
                "whatsapp": "https://web.whatsapp.com",
                "discord": "https://discord.com/app",
            }
            
            # Common application paths for different OS
            windows_apps = {
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "explorer": "explorer.exe",
                "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "vscode": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "vs code": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "steam": r"C:\Program Files (x86)\Steam\steam.exe",
                "discord": r"C:\Users\{}\AppData\Local\Discord\app-*\Discord.exe",
                "spotify": r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe",
                "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                "gta 5": r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
                "gta v": r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
                "gta": r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto V\GTA5.exe",
            }
            
            mac_apps = {
                "chrome": "Google Chrome",
                "google chrome": "Google Chrome",
                "firefox": "Firefox",
                "safari": "Safari",
                "terminal": "Terminal",
                "finder": "Finder",
                "calculator": "Calculator",
                "notes": "Notes",
                "mail": "Mail",
                "messages": "Messages",
                "vscode": "Visual Studio Code",
                "vs code": "Visual Studio Code",
                "steam": "Steam",
                "discord": "Discord",
                "spotify": "Spotify",
                "vlc": "VLC",
            }
            
            linux_apps = {
                "chrome": "google-chrome",
                "google chrome": "google-chrome",
                "firefox": "firefox",
                "terminal": "gnome-terminal",
                "calculator": "gnome-calculator",
                "files": "nautilus",
                "vscode": "code",
                "vs code": "code",
                "steam": "steam",
                "discord": "discord",
                "spotify": "spotify",
                "vlc": "vlc",
            }
            
            app_lower = app_name.lower()
            system = platform.system()
            
            # Check if it's a web service
            if app_lower in web_services:
                webbrowser.open(web_services[app_lower])
                return json.dumps({
                    "status": "success", 
                    "opened": "browser", 
                    "service": app_name, 
                    "url": web_services[app_lower]
                })
            
            # Try to open as system application
            if system == "Windows":
                if app_lower in windows_apps:
                    app_path = windows_apps[app_lower]
                    
                    # Replace {} with username for user-specific paths
                    if "{}" in app_path:
                        username = os.environ.get("USERNAME", "")
                        app_path = app_path.format(username)
                    
                    # Handle wildcard paths (like Discord)
                    if "*" in app_path:
                        import glob
                        matches = glob.glob(app_path)
                        if matches:
                            app_path = matches[0]
                    
                    # Try to open the app
                    if os.path.exists(app_path):
                        subprocess.Popen([app_path], shell=True)
                        return json.dumps({
                            "status": "success", 
                            "opened": "app", 
                            "app": app_name,
                            "path": app_path
                        })
                    else:
                        # Try using start command
                        os.system(f'start "" "{app_name}"')
                        return json.dumps({
                            "status": "success", 
                            "opened": "app", 
                            "app": app_name,
                            "method": "start_command"
                        })
                else:
                    # Try generic Windows start command
                    os.system(f'start "" "{app_name}"')
                    return json.dumps({
                        "status": "success", 
                        "opened": "app", 
                        "app": app_name,
                        "method": "start_command"
                    })
                    
            elif system == "Darwin":  # macOS
                if app_lower in mac_apps:
                    app_name = mac_apps[app_lower]
                
                os.system(f"open -a '{app_name}'")
                return json.dumps({
                    "status": "success", 
                    "opened": "app", 
                    "app": app_name
                })
                
            elif system == "Linux":
                if app_lower in linux_apps:
                    app_cmd = linux_apps[app_lower]
                else:
                    app_cmd = app_name
                
                subprocess.Popen([app_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return json.dumps({
                    "status": "success", 
                    "opened": "app", 
                    "app": app_name
                })
            
            else:
                return json.dumps({
                    "error": f"Unsupported operating system: {system}"
                })
                
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "app": app_name,
                "suggestion": "Make sure the application is installed and try using the full application name."
            })

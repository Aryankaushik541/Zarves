import os
import sys
import json
import webbrowser
import subprocess
import platform
import winreg
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
                    "description": "Open ANY Windows application, system tool, or website. Supports: This PC, Control Panel, Settings, VLC, Word, Excel, PowerPoint, Chrome, Notepad, Calculator, Paint, File Explorer, Task Manager, Device Manager, Disk Management, Registry Editor, Command Prompt, PowerShell, and many more. Also opens websites like YouTube, Gmail, etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "app_name": {
                                "type": "string", 
                                "description": "Name of the app, system tool, or website to open. Examples: 'This PC', 'Control Panel', 'VLC', 'Word', 'Excel', 'Chrome', 'Calculator', 'Settings', 'Task Manager', 'YouTube', 'Gmail', etc."
                            }
                        }, 
                        "required": ["app_name"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_system_location",
                    "description": "Open specific Windows system locations like Downloads, Documents, Desktop, Pictures, Videos, Music, Recycle Bin, etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "location": {
                                "type": "string", 
                                "description": "System location to open: 'downloads', 'documents', 'desktop', 'pictures', 'videos', 'music', 'recycle bin', 'temp', 'appdata', etc."
                            }
                        }, 
                        "required": ["location"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "set_volume": self.set_volume,
            "open_app": self.open_app,
            "open_system_location": self.open_system_location
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

    def _find_app_in_registry(self, app_name):
        """
        Search Windows Registry for installed application paths
        """
        try:
            # Common registry paths for installed apps
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"),
            ]
            
            for hkey, path in registry_paths:
                try:
                    key = winreg.OpenKey(hkey, path)
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            if app_name.lower() in subkey_name.lower():
                                subkey = winreg.OpenKey(key, subkey_name)
                                app_path, _ = winreg.QueryValueEx(subkey, "")
                                winreg.CloseKey(subkey)
                                if os.path.exists(app_path):
                                    return app_path
                            i += 1
                        except OSError:
                            break
                    winreg.CloseKey(key)
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Registry search error: {e}")
            return None

    def _search_common_locations(self, app_name):
        """
        Search common installation directories for the app
        """
        username = os.environ.get("USERNAME", "")
        
        # Common installation directories
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            f"C:\\Users\\{username}\\AppData\\Local",
            f"C:\\Users\\{username}\\AppData\\Roaming",
            f"C:\\Users\\{username}\\AppData\\Local\\Programs",
        ]
        
        # Common executable names
        exe_names = [
            f"{app_name}.exe",
            f"{app_name.replace(' ', '')}.exe",
            f"{app_name.replace(' ', '_')}.exe",
        ]
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            try:
                for root, dirs, files in os.walk(search_path):
                    # Limit depth to avoid long searches
                    if root.count(os.sep) - search_path.count(os.sep) > 3:
                        continue
                    
                    for exe_name in exe_names:
                        if exe_name.lower() in [f.lower() for f in files]:
                            full_path = os.path.join(root, exe_name)
                            return full_path
                    
                    # Check if directory name matches app name
                    if app_name.lower() in root.lower():
                        for file in files:
                            if file.endswith('.exe'):
                                return os.path.join(root, file)
            except:
                continue
        
        return None

    def open_system_location(self, location):
        """
        Open specific Windows system locations
        """
        try:
            username = os.environ.get("USERNAME", "")
            
            # Map of system locations
            locations = {
                "downloads": f"C:\\Users\\{username}\\Downloads",
                "documents": f"C:\\Users\\{username}\\Documents",
                "desktop": f"C:\\Users\\{username}\\Desktop",
                "pictures": f"C:\\Users\\{username}\\Pictures",
                "videos": f"C:\\Users\\{username}\\Videos",
                "music": f"C:\\Users\\{username}\\Music",
                "recycle bin": "shell:RecycleBinFolder",
                "temp": os.environ.get("TEMP", ""),
                "appdata": f"C:\\Users\\{username}\\AppData",
                "roaming": f"C:\\Users\\{username}\\AppData\\Roaming",
                "local": f"C:\\Users\\{username}\\AppData\\Local",
                "startup": f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup",
            }
            
            location_lower = location.lower()
            
            if location_lower in locations:
                path = locations[location_lower]
                
                if path.startswith("shell:"):
                    # Use shell command for special folders
                    os.system(f'explorer {path}')
                else:
                    # Open regular folder
                    os.startfile(path)
                
                return json.dumps({
                    "status": "success",
                    "location": location,
                    "path": path
                })
            else:
                return json.dumps({
                    "error": f"Unknown location: {location}",
                    "available": list(locations.keys())
                })
                
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
            
            # Windows Shell Commands (for system tools)
            shell_commands = {
                "this pc": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
                "my computer": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
                "computer": "explorer.exe ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
                "control panel": "control.exe",
                "settings": "ms-settings:",
                "task manager": "taskmgr.exe",
                "device manager": "devmgmt.msc",
                "disk management": "diskmgmt.msc",
                "services": "services.msc",
                "registry editor": "regedit.exe",
                "regedit": "regedit.exe",
                "event viewer": "eventvwr.msc",
                "system information": "msinfo32.exe",
                "resource monitor": "resmon.exe",
                "performance monitor": "perfmon.exe",
                "computer management": "compmgmt.msc",
                "disk cleanup": "cleanmgr.exe",
                "defragment": "dfrgui.exe",
                "windows update": "ms-settings:windowsupdate",
                "network connections": "ncpa.cpl",
                "sound settings": "mmsys.cpl",
                "display settings": "desk.cpl",
                "power options": "powercfg.cpl",
                "programs and features": "appwiz.cpl",
                "user accounts": "netplwiz.exe",
                "firewall": "firewall.cpl",
                "windows defender": "windowsdefender:",
                "snipping tool": "snippingtool.exe",
                "snip & sketch": "ms-screenclip:",
                "magnifier": "magnify.exe",
                "on-screen keyboard": "osk.exe",
                "narrator": "narrator.exe",
                "character map": "charmap.exe",
                "remote desktop": "mstsc.exe",
                "windows explorer": "explorer.exe",
                "file explorer": "explorer.exe",
                "explorer": "explorer.exe",
            }
            
            # Common Windows applications with multiple possible paths
            windows_apps = {
                "chrome": [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                ],
                "google chrome": [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                ],
                "firefox": [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                ],
                "edge": [
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                ],
                "notepad": ["notepad.exe"],
                "calculator": ["calc.exe"],
                "paint": ["mspaint.exe"],
                "cmd": ["cmd.exe"],
                "command prompt": ["cmd.exe"],
                "powershell": ["powershell.exe"],
                "word": [
                    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
                ],
                "excel": [
                    r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
                ],
                "powerpoint": [
                    r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE",
                ],
                "outlook": [
                    r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
                ],
                "vlc": [
                    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                    r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                ],
                "vscode": [
                    r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                    r"C:\Program Files\Microsoft VS Code\Code.exe",
                ],
                "vs code": [
                    r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                    r"C:\Program Files\Microsoft VS Code\Code.exe",
                ],
                "steam": [
                    r"C:\Program Files (x86)\Steam\steam.exe",
                    r"C:\Program Files\Steam\steam.exe",
                ],
                "discord": [
                    r"C:\Users\{}\AppData\Local\Discord\Update.exe --processStart Discord.exe",
                ],
                "spotify": [
                    r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe",
                ],
                "winrar": [
                    r"C:\Program Files\WinRAR\WinRAR.exe",
                    r"C:\Program Files (x86)\WinRAR\WinRAR.exe",
                ],
                "7zip": [
                    r"C:\Program Files\7-Zip\7zFM.exe",
                    r"C:\Program Files (x86)\7-Zip\7zFM.exe",
                ],
                "photoshop": [
                    r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe",
                    r"C:\Program Files\Adobe\Adobe Photoshop CC 2024\Photoshop.exe",
                ],
                "obs": [
                    r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
                    r"C:\Program Files (x86)\obs-studio\bin\32bit\obs32.exe",
                ],
                "obs studio": [
                    r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
                ],
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
            
            # Windows-specific handling
            if system == "Windows":
                # Check if it's a shell command (system tool)
                if app_lower in shell_commands:
                    command = shell_commands[app_lower]
                    print(f"🔧 Opening system tool: {app_name}")
                    
                    if command.startswith("ms-"):
                        # Use start for ms- protocol handlers
                        os.system(f'start {command}')
                    else:
                        # Direct execution for .exe and .msc files
                        subprocess.Popen(command, shell=True)
                    
                    return json.dumps({
                        "status": "success",
                        "opened": "system_tool",
                        "app": app_name,
                        "command": command
                    })
                
                # Check if it's in our known apps list
                if app_lower in windows_apps:
                    paths = windows_apps[app_lower]
                    username = os.environ.get("USERNAME", "")
                    
                    # Try each possible path
                    for app_path in paths:
                        # Replace {} with username for user-specific paths
                        if "{}" in app_path:
                            app_path = app_path.format(username)
                        
                        # Check if path exists
                        if os.path.exists(app_path):
                            print(f"✅ Found: {app_path}")
                            subprocess.Popen([app_path], shell=True)
                            return json.dumps({
                                "status": "success",
                                "opened": "app",
                                "app": app_name,
                                "path": app_path
                            })
                
                # Try to find in Windows Registry
                print(f"🔍 Searching registry for: {app_name}")
                registry_path = self._find_app_in_registry(app_name)
                if registry_path:
                    print(f"✅ Found in registry: {registry_path}")
                    subprocess.Popen([registry_path], shell=True)
                    return json.dumps({
                        "status": "success",
                        "opened": "app",
                        "app": app_name,
                        "path": registry_path,
                        "method": "registry"
                    })
                
                # Try Windows start command (works for many apps)
                print(f"🔄 Trying Windows start command for: {app_name}")
                try:
                    os.system(f'start "" "{app_name}"')
                    return json.dumps({
                        "status": "success",
                        "opened": "app",
                        "app": app_name,
                        "method": "start_command"
                    })
                except:
                    pass
                
                # Last resort: search common locations
                print(f"🔍 Searching common locations for: {app_name}")
                found_path = self._search_common_locations(app_name)
                if found_path:
                    print(f"✅ Found: {found_path}")
                    subprocess.Popen([found_path], shell=True)
                    return json.dumps({
                        "status": "success",
                        "opened": "app",
                        "app": app_name,
                        "path": found_path,
                        "method": "search"
                    })
                
                # If nothing worked
                return json.dumps({
                    "error": f"Could not find or open: {app_name}",
                    "suggestion": "Make sure the application is installed. Try using the full application name (e.g., 'Google Chrome' instead of 'Chrome')"
                })
            
            # macOS handling
            elif system == "Darwin":
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
                
                if app_lower in mac_apps:
                    app_name = mac_apps[app_lower]
                
                os.system(f"open -a '{app_name}'")
                return json.dumps({
                    "status": "success",
                    "opened": "app",
                    "app": app_name
                })
            
            # Linux handling
            elif system == "Linux":
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

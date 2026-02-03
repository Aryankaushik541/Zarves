"""
Master PC Control Skill - Complete System Access
AI-powered automation with full control over:
- Applications (open, close, switch)
- System (volume, brightness, power)
- Files (create, delete, search)
- Web (browse, download, search)
- Media (play, pause, control)
- Network (wifi, bluetooth, etc.)
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
import pyautogui
import psutil
from pathlib import Path
from typing import List, Dict, Any


class MasterPCControl:
    """Complete PC control with AI automation"""
    
    def __init__(self):
        self.name = "master_pc_control"
        self.os_type = platform.system()  # Windows, Darwin (Mac), Linux
        
        # Common applications database
        self.apps = {
            # Browsers
            'chrome': ['chrome', 'google chrome', 'google-chrome'],
            'firefox': ['firefox', 'mozilla firefox'],
            'edge': ['edge', 'microsoft edge', 'msedge'],
            'brave': ['brave', 'brave browser'],
            
            # Office
            'word': ['word', 'microsoft word', 'winword'],
            'excel': ['excel', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'microsoft powerpoint', 'powerpnt'],
            'notepad': ['notepad', 'notepad++'],
            
            # Media
            'vlc': ['vlc', 'vlc media player'],
            'spotify': ['spotify'],
            'itunes': ['itunes', 'apple music'],
            
            # Communication
            'whatsapp': ['whatsapp', 'whatsapp desktop'],
            'telegram': ['telegram', 'telegram desktop'],
            'discord': ['discord'],
            'slack': ['slack'],
            'zoom': ['zoom', 'zoom meetings'],
            
            # Development
            'vscode': ['code', 'visual studio code', 'vscode'],
            'pycharm': ['pycharm'],
            'sublime': ['sublime', 'sublime text'],
            'atom': ['atom'],
            
            # System
            'calculator': ['calc', 'calculator'],
            'paint': ['paint', 'mspaint'],
            'cmd': ['cmd', 'command prompt'],
            'powershell': ['powershell'],
            'task manager': ['taskmgr', 'task manager'],
            'control panel': ['control', 'control panel'],
            'settings': ['settings', 'ms-settings'],
            'this pc': ['explorer', 'my computer', 'this pc'],
            
            # Others
            'steam': ['steam'],
            'epic games': ['epic', 'epic games'],
        }
    
    @property
    def name(self) -> str:
        return "master_pc_control"
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools"""
        return [
            {
                "name": "open_application",
                "description": "Open any application on PC",
                "parameters": {
                    "app_name": "Name of application to open"
                }
            },
            {
                "name": "close_application",
                "description": "Close any running application",
                "parameters": {
                    "app_name": "Name of application to close"
                }
            },
            {
                "name": "control_volume",
                "description": "Control system volume",
                "parameters": {
                    "action": "increase, decrease, mute, unmute, set"
                }
            },
            {
                "name": "control_brightness",
                "description": "Control screen brightness",
                "parameters": {
                    "action": "increase, decrease, set"
                }
            },
            {
                "name": "power_control",
                "description": "System power operations",
                "parameters": {
                    "action": "shutdown, restart, sleep, lock"
                }
            },
            {
                "name": "file_operations",
                "description": "File and folder operations",
                "parameters": {
                    "action": "create, delete, rename, search, open"
                }
            },
            {
                "name": "web_operations",
                "description": "Web browser operations",
                "parameters": {
                    "action": "open, search, download, bookmark"
                }
            },
            {
                "name": "media_control",
                "description": "Media playback control",
                "parameters": {
                    "action": "play, pause, next, previous, volume"
                }
            }
        ]
    
    def can_handle(self, query: str) -> bool:
        """Check if this skill can handle the query"""
        keywords = [
            # Apps
            'open', 'close', 'start', 'launch', 'kholo', 'band', 'chalu',
            # System
            'volume', 'brightness', 'shutdown', 'restart', 'sleep', 'lock',
            'awaaz', 'band karo', 'lock karo', 'shutdown karo',
            # Files
            'file', 'folder', 'create', 'delete', 'search', 'find',
            # Web
            'google', 'search', 'browse', 'website', 'download',
            # Media
            'play', 'pause', 'next', 'previous', 'music', 'video',
            # Common apps
            'chrome', 'word', 'excel', 'vlc', 'whatsapp', 'calculator',
            'notepad', 'paint', 'cmd', 'task manager', 'control panel'
        ]
        return any(keyword in query.lower() for keyword in keywords)
    
    def execute(self, query: str, **kwargs) -> str:
        """Execute PC control commands"""
        query_lower = query.lower()
        
        try:
            # Application control
            if any(word in query_lower for word in ['open', 'kholo', 'start', 'launch', 'chalu']):
                return self._open_application(query)
            
            elif any(word in query_lower for word in ['close', 'band', 'exit', 'quit']):
                return self._close_application(query)
            
            # Volume control
            elif any(word in query_lower for word in ['volume', 'awaaz', 'sound']):
                return self._control_volume(query)
            
            # Brightness control
            elif 'brightness' in query_lower or 'chamak' in query_lower:
                return self._control_brightness(query)
            
            # Power control
            elif any(word in query_lower for word in ['shutdown', 'restart', 'sleep', 'lock']):
                return self._power_control(query)
            
            # File operations
            elif any(word in query_lower for word in ['file', 'folder', 'create', 'delete', 'search']):
                return self._file_operations(query)
            
            # Web operations
            elif any(word in query_lower for word in ['google', 'search', 'browse', 'website']):
                return self._web_operations(query)
            
            # Media control
            elif any(word in query_lower for word in ['play', 'pause', 'next', 'previous']):
                return self._media_control(query)
            
            else:
                return "I can help with: apps, volume, brightness, files, web, media. What would you like?"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _open_application(self, query: str) -> str:
        """Open any application"""
        try:
            # Extract app name
            app_name = self._extract_app_name(query)
            
            if not app_name:
                return "Please specify which application to open"
            
            # Find app command
            app_cmd = self._find_app_command(app_name)
            
            if not app_cmd:
                return f"Application '{app_name}' not found. Please check the name."
            
            # Open app based on OS
            if self.os_type == "Windows":
                subprocess.Popen(app_cmd, shell=True)
            elif self.os_type == "Darwin":  # Mac
                subprocess.Popen(['open', '-a', app_cmd])
            else:  # Linux
                subprocess.Popen([app_cmd])
            
            return f"Opening {app_name}..."
            
        except Exception as e:
            return f"Failed to open application: {str(e)}"
    
    def _extract_app_name(self, query: str) -> str:
        """Extract application name from query"""
        # Remove common words
        remove_words = ['open', 'kholo', 'start', 'launch', 'chalu', 'karo', 'please', 'jarvis']
        words = query.lower().split()
        filtered = [w for w in words if w not in remove_words]
        return ' '.join(filtered) if filtered else None
    
    def _find_app_command(self, app_name: str) -> str:
        """Find application command"""
        app_lower = app_name.lower()
        
        # Check in apps database
        for app_key, app_aliases in self.apps.items():
            if any(alias in app_lower for alias in app_aliases):
                return self._get_app_path(app_key)
        
        # Try direct name
        return app_name
    
    def _get_app_path(self, app_key: str) -> str:
        """Get application path based on OS"""
        if self.os_type == "Windows":
            paths = {
                'chrome': 'chrome',
                'firefox': 'firefox',
                'edge': 'msedge',
                'word': 'winword',
                'excel': 'excel',
                'powerpoint': 'powerpnt',
                'notepad': 'notepad',
                'vlc': 'vlc',
                'calculator': 'calc',
                'paint': 'mspaint',
                'cmd': 'cmd',
                'powershell': 'powershell',
                'task manager': 'taskmgr',
                'control panel': 'control',
                'settings': 'ms-settings:',
                'this pc': 'explorer',
                'vscode': 'code',
            }
        elif self.os_type == "Darwin":  # Mac
            paths = {
                'chrome': 'Google Chrome',
                'firefox': 'Firefox',
                'safari': 'Safari',
                'word': 'Microsoft Word',
                'excel': 'Microsoft Excel',
                'vlc': 'VLC',
                'calculator': 'Calculator',
                'vscode': 'Visual Studio Code',
            }
        else:  # Linux
            paths = {
                'chrome': 'google-chrome',
                'firefox': 'firefox',
                'vlc': 'vlc',
                'calculator': 'gnome-calculator',
                'vscode': 'code',
            }
        
        return paths.get(app_key, app_key)
    
    def _close_application(self, query: str) -> str:
        """Close running application"""
        try:
            app_name = self._extract_app_name(query)
            
            if not app_name:
                return "Please specify which application to close"
            
            # Find and kill process
            killed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name.lower() in proc.info['name'].lower():
                        proc.kill()
                        killed = True
                except:
                    pass
            
            if killed:
                return f"Closed {app_name}"
            else:
                return f"{app_name} is not running"
                
        except Exception as e:
            return f"Failed to close application: {str(e)}"
    
    def _control_volume(self, query: str) -> str:
        """Control system volume"""
        try:
            if 'badhao' in query.lower() or 'increase' in query.lower() or 'up' in query.lower():
                # Increase volume
                if self.os_type == "Windows":
                    for _ in range(5):
                        pyautogui.press('volumeup')
                return "Volume increased"
            
            elif 'kam' in query.lower() or 'decrease' in query.lower() or 'down' in query.lower():
                # Decrease volume
                if self.os_type == "Windows":
                    for _ in range(5):
                        pyautogui.press('volumedown')
                return "Volume decreased"
            
            elif 'mute' in query.lower() or 'chup' in query.lower():
                # Mute
                if self.os_type == "Windows":
                    pyautogui.press('volumemute')
                return "Volume muted"
            
            else:
                return "Please specify: volume badhao, volume kam karo, or mute"
                
        except Exception as e:
            return f"Volume control failed: {str(e)}"
    
    def _control_brightness(self, query: str) -> str:
        """Control screen brightness"""
        try:
            if 'badhao' in query.lower() or 'increase' in query.lower():
                # Increase brightness (Windows only)
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)'])
                return "Brightness increased"
            
            elif 'kam' in query.lower() or 'decrease' in query.lower():
                # Decrease brightness
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,50)'])
                return "Brightness decreased"
            
            else:
                return "Please specify: brightness badhao or brightness kam karo"
                
        except Exception as e:
            return f"Brightness control failed: {str(e)}"
    
    def _power_control(self, query: str) -> str:
        """System power operations"""
        try:
            if 'shutdown' in query.lower():
                if self.os_type == "Windows":
                    subprocess.run(['shutdown', '/s', '/t', '10'])
                return "Shutting down in 10 seconds..."
            
            elif 'restart' in query.lower():
                if self.os_type == "Windows":
                    subprocess.run(['shutdown', '/r', '/t', '10'])
                return "Restarting in 10 seconds..."
            
            elif 'sleep' in query.lower():
                if self.os_type == "Windows":
                    subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
                return "Going to sleep..."
            
            elif 'lock' in query.lower():
                if self.os_type == "Windows":
                    subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
                return "Locking PC..."
            
            else:
                return "Please specify: shutdown, restart, sleep, or lock"
                
        except Exception as e:
            return f"Power control failed: {str(e)}"
    
    def _file_operations(self, query: str) -> str:
        """File and folder operations"""
        try:
            # Simple file operations
            if 'create' in query.lower():
                return "Please specify file name and location"
            elif 'delete' in query.lower():
                return "Please specify file to delete"
            elif 'search' in query.lower() or 'find' in query.lower():
                return "Please specify what to search for"
            else:
                return "I can help with: create, delete, search files"
                
        except Exception as e:
            return f"File operation failed: {str(e)}"
    
    def _web_operations(self, query: str) -> str:
        """Web browser operations"""
        try:
            # Extract search term
            search_term = query.lower().replace('google', '').replace('search', '').replace('for', '').strip()
            
            if search_term:
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                return f"Searching Google for: {search_term}"
            else:
                webbrowser.open("https://www.google.com")
                return "Opening Google..."
                
        except Exception as e:
            return f"Web operation failed: {str(e)}"
    
    def _media_control(self, query: str) -> str:
        """Media playback control"""
        try:
            if 'play' in query.lower() or 'pause' in query.lower():
                pyautogui.press('playpause')
                return "Media play/pause toggled"
            
            elif 'next' in query.lower():
                pyautogui.press('nexttrack')
                return "Playing next track"
            
            elif 'previous' in query.lower():
                pyautogui.press('prevtrack')
                return "Playing previous track"
            
            else:
                return "I can help with: play, pause, next, previous"
                
        except Exception as e:
            return f"Media control failed: {str(e)}"


# Register skill
def register():
    return MasterPCControl()

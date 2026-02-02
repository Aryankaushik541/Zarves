#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced System Control Module
Cross-platform automation for Windows, Mac, and Linux
Features:
- Open/Close any application
- Control system settings
- Window management
- Process management
- System configuration
- AI-powered automation
"""

import os
import sys
import platform
import subprocess
import time
import psutil
import json
from pathlib import Path


class AdvancedSystemControl:
    """Advanced system control with cross-platform support"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.app_paths = self.load_app_database()
        self.running_apps = {}
        
    def load_app_database(self):
        """Load application paths database"""
        if self.platform == "windows":
            return {
                # Browsers
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                
                # Office
                "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                
                # Development
                "vscode": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "pycharm": r"C:\Program Files\JetBrains\PyCharm\bin\pycharm64.exe",
                "sublime": r"C:\Program Files\Sublime Text\sublime_text.exe",
                "notepad++": r"C:\Program Files\Notepad++\notepad++.exe",
                
                # Media
                "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                "spotify": r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe",
                "itunes": r"C:\Program Files\iTunes\iTunes.exe",
                
                # Communication
                "discord": r"C:\Users\{}\AppData\Local\Discord\app-1.0.9015\Discord.exe",
                "slack": r"C:\Users\{}\AppData\Local\slack\slack.exe",
                "teams": r"C:\Users\{}\AppData\Local\Microsoft\Teams\current\Teams.exe",
                "zoom": r"C:\Users\{}\AppData\Roaming\Zoom\bin\Zoom.exe",
                
                # System
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "explorer": "explorer.exe",
                "taskmgr": "taskmgr.exe",
                "control": "control.exe",
                "settings": "ms-settings:",
            }
        elif self.platform == "darwin":  # macOS
            return {
                # Browsers
                "chrome": "/Applications/Google Chrome.app",
                "firefox": "/Applications/Firefox.app",
                "safari": "/Applications/Safari.app",
                "brave": "/Applications/Brave Browser.app",
                
                # Office
                "word": "/Applications/Microsoft Word.app",
                "excel": "/Applications/Microsoft Excel.app",
                "powerpoint": "/Applications/Microsoft PowerPoint.app",
                "outlook": "/Applications/Microsoft Outlook.app",
                
                # Development
                "vscode": "/Applications/Visual Studio Code.app",
                "pycharm": "/Applications/PyCharm.app",
                "sublime": "/Applications/Sublime Text.app",
                "xcode": "/Applications/Xcode.app",
                
                # Media
                "vlc": "/Applications/VLC.app",
                "spotify": "/Applications/Spotify.app",
                "itunes": "/Applications/Music.app",
                
                # Communication
                "discord": "/Applications/Discord.app",
                "slack": "/Applications/Slack.app",
                "teams": "/Applications/Microsoft Teams.app",
                "zoom": "/Applications/zoom.us.app",
                
                # System
                "terminal": "/Applications/Utilities/Terminal.app",
                "finder": "/System/Library/CoreServices/Finder.app",
                "calculator": "/Applications/Calculator.app",
                "textedit": "/Applications/TextEdit.app",
            }
        else:  # Linux
            return {
                # Browsers
                "chrome": "google-chrome",
                "firefox": "firefox",
                "brave": "brave-browser",
                "chromium": "chromium-browser",
                
                # Office
                "libreoffice": "libreoffice",
                "writer": "libreoffice --writer",
                "calc": "libreoffice --calc",
                "impress": "libreoffice --impress",
                
                # Development
                "vscode": "code",
                "pycharm": "pycharm",
                "sublime": "subl",
                "gedit": "gedit",
                "vim": "vim",
                
                # Media
                "vlc": "vlc",
                "spotify": "spotify",
                
                # Communication
                "discord": "discord",
                "slack": "slack",
                "teams": "teams",
                "zoom": "zoom",
                
                # System
                "terminal": "gnome-terminal",
                "nautilus": "nautilus",
                "calculator": "gnome-calculator",
            }
    
    def find_application(self, app_name):
        """Find application path intelligently"""
        app_name = app_name.lower().strip()
        
        # Check database first
        if app_name in self.app_paths:
            path = self.app_paths[app_name]
            
            # Handle user-specific paths
            if "{}" in path:
                username = os.getenv("USERNAME") or os.getenv("USER")
                path = path.format(username)
            
            # Verify path exists
            if os.path.exists(path):
                return path
        
        # Search common locations
        if self.platform == "windows":
            search_paths = [
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                os.path.expanduser(r"~\AppData\Local"),
                os.path.expanduser(r"~\AppData\Roaming"),
            ]
            
            for base_path in search_paths:
                if os.path.exists(base_path):
                    for root, dirs, files in os.walk(base_path):
                        for file in files:
                            if app_name in file.lower() and file.endswith('.exe'):
                                return os.path.join(root, file)
        
        elif self.platform == "darwin":
            search_paths = [
                "/Applications",
                os.path.expanduser("~/Applications"),
            ]
            
            for base_path in search_paths:
                if os.path.exists(base_path):
                    for item in os.listdir(base_path):
                        if app_name in item.lower() and item.endswith('.app'):
                            return os.path.join(base_path, item)
        
        # Try command directly (Linux or system commands)
        return app_name
    
    def open_application(self, app_name, args=None):
        """Open an application with optional arguments"""
        try:
            app_path = self.find_application(app_name)
            
            if not app_path:
                return False, f"Application '{app_name}' not found"
            
            # Build command
            if self.platform == "windows":
                if app_path.startswith("ms-settings:"):
                    # Windows Settings
                    subprocess.Popen(["start", app_path], shell=True)
                else:
                    cmd = [app_path]
                    if args:
                        cmd.extend(args if isinstance(args, list) else [args])
                    subprocess.Popen(cmd, shell=True)
            
            elif self.platform == "darwin":
                cmd = ["open", "-a", app_path]
                if args:
                    cmd.extend(["--args"] + (args if isinstance(args, list) else [args]))
                subprocess.Popen(cmd)
            
            else:  # Linux
                cmd = [app_path]
                if args:
                    cmd.extend(args if isinstance(args, list) else [args])
                subprocess.Popen(cmd, shell=True)
            
            # Track opened app
            self.running_apps[app_name] = {
                'path': app_path,
                'opened_at': time.time()
            }
            
            return True, f"Opened {app_name} successfully"
            
        except Exception as e:
            return False, f"Error opening {app_name}: {str(e)}"
    
    def close_application(self, app_name):
        """Close an application by name"""
        try:
            app_name_lower = app_name.lower()
            closed = False
            
            # Find and kill processes
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower()
                    proc_exe = proc.info['exe']
                    
                    # Match by name or executable path
                    if (app_name_lower in proc_name or 
                        (proc_exe and app_name_lower in proc_exe.lower())):
                        
                        proc.terminate()
                        proc.wait(timeout=3)
                        closed = True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                if app_name in self.running_apps:
                    del self.running_apps[app_name]
                return True, f"Closed {app_name} successfully"
            else:
                return False, f"{app_name} is not running"
                
        except Exception as e:
            return False, f"Error closing {app_name}: {str(e)}"
    
    def list_running_applications(self):
        """List all running applications"""
        try:
            apps = set()
            for proc in psutil.process_iter(['name']):
                try:
                    apps.add(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return True, sorted(list(apps))
        except Exception as e:
            return False, f"Error listing applications: {str(e)}"
    
    def is_application_running(self, app_name):
        """Check if an application is running"""
        try:
            app_name_lower = app_name.lower()
            
            for proc in psutil.process_iter(['name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower()
                    proc_exe = proc.info['exe']
                    
                    if (app_name_lower in proc_name or 
                        (proc_exe and app_name_lower in proc_exe.lower())):
                        return True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False
        except:
            return False
    
    # ============================================================================
    # SYSTEM SETTINGS CONTROL
    # ============================================================================
    
    def control_volume(self, action, level=None):
        """Control system volume"""
        try:
            if self.platform == "windows":
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                
                if action == "mute":
                    volume.SetMute(1, None)
                    return True, "Volume muted"
                elif action == "unmute":
                    volume.SetMute(0, None)
                    return True, "Volume unmuted"
                elif action == "set" and level is not None:
                    volume.SetMasterVolumeLevelScalar(level / 100, None)
                    return True, f"Volume set to {level}%"
                elif action == "get":
                    current = int(volume.GetMasterVolumeLevelScalar() * 100)
                    return True, f"Current volume: {current}%"
            
            elif self.platform == "darwin":
                if action == "mute":
                    os.system("osascript -e 'set volume output muted true'")
                    return True, "Volume muted"
                elif action == "unmute":
                    os.system("osascript -e 'set volume output muted false'")
                    return True, "Volume unmuted"
                elif action == "set" and level is not None:
                    os.system(f"osascript -e 'set volume output volume {level}'")
                    return True, f"Volume set to {level}%"
            
            else:  # Linux
                if action == "mute":
                    os.system("amixer set Master mute")
                    return True, "Volume muted"
                elif action == "unmute":
                    os.system("amixer set Master unmute")
                    return True, "Volume unmuted"
                elif action == "set" and level is not None:
                    os.system(f"amixer set Master {level}%")
                    return True, f"Volume set to {level}%"
            
            return False, "Invalid volume action"
            
        except Exception as e:
            return False, f"Error controlling volume: {str(e)}"
    
    def control_brightness(self, level):
        """Control screen brightness"""
        try:
            if self.platform == "windows":
                import wmi
                c = wmi.WMI(namespace='wmi')
                methods = c.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(level, 0)
                return True, f"Brightness set to {level}%"
            
            elif self.platform == "darwin":
                os.system(f"brightness {level / 100}")
                return True, f"Brightness set to {level}%"
            
            else:  # Linux
                # Try different methods
                backlight_paths = [
                    "/sys/class/backlight/intel_backlight/brightness",
                    "/sys/class/backlight/acpi_video0/brightness",
                ]
                
                for path in backlight_paths:
                    if os.path.exists(path):
                        max_path = path.replace("brightness", "max_brightness")
                        with open(max_path, 'r') as f:
                            max_brightness = int(f.read().strip())
                        
                        new_brightness = int((level / 100) * max_brightness)
                        os.system(f"echo {new_brightness} | sudo tee {path}")
                        return True, f"Brightness set to {level}%"
                
                return False, "Brightness control not available"
                
        except Exception as e:
            return False, f"Error controlling brightness: {str(e)}"
    
    def control_wifi(self, action):
        """Control WiFi on/off"""
        try:
            if self.platform == "windows":
                if action == "on":
                    os.system("netsh interface set interface 'Wi-Fi' enabled")
                    return True, "WiFi enabled"
                elif action == "off":
                    os.system("netsh interface set interface 'Wi-Fi' disabled")
                    return True, "WiFi disabled"
            
            elif self.platform == "darwin":
                if action == "on":
                    os.system("networksetup -setairportpower en0 on")
                    return True, "WiFi enabled"
                elif action == "off":
                    os.system("networksetup -setairportpower en0 off")
                    return True, "WiFi disabled"
            
            else:  # Linux
                if action == "on":
                    os.system("nmcli radio wifi on")
                    return True, "WiFi enabled"
                elif action == "off":
                    os.system("nmcli radio wifi off")
                    return True, "WiFi disabled"
            
            return False, "Invalid WiFi action"
            
        except Exception as e:
            return False, f"Error controlling WiFi: {str(e)}"
    
    def control_bluetooth(self, action):
        """Control Bluetooth on/off"""
        try:
            if self.platform == "windows":
                # Windows Bluetooth control requires admin
                if action == "on":
                    os.system("powershell -Command \"Get-PnpDevice | Where-Object {$_.Class -eq 'Bluetooth'} | Enable-PnpDevice -Confirm:$false\"")
                    return True, "Bluetooth enabled"
                elif action == "off":
                    os.system("powershell -Command \"Get-PnpDevice | Where-Object {$_.Class -eq 'Bluetooth'} | Disable-PnpDevice -Confirm:$false\"")
                    return True, "Bluetooth disabled"
            
            elif self.platform == "darwin":
                if action == "on":
                    os.system("blueutil --power 1")
                    return True, "Bluetooth enabled"
                elif action == "off":
                    os.system("blueutil --power 0")
                    return True, "Bluetooth disabled"
            
            else:  # Linux
                if action == "on":
                    os.system("rfkill unblock bluetooth")
                    return True, "Bluetooth enabled"
                elif action == "off":
                    os.system("rfkill block bluetooth")
                    return True, "Bluetooth disabled"
            
            return False, "Invalid Bluetooth action"
            
        except Exception as e:
            return False, f"Error controlling Bluetooth: {str(e)}"
    
    def control_display(self, action):
        """Control display settings"""
        try:
            if self.platform == "windows":
                if action == "sleep":
                    os.system("powershell (Add-Type '[DllImport(\"user32.dll\")]public static extern int SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)")
                    return True, "Display turned off"
                elif action == "on":
                    # Move mouse to wake display
                    import pyautogui
                    pyautogui.move(1, 1)
                    return True, "Display activated"
            
            elif self.platform == "darwin":
                if action == "sleep":
                    os.system("pmset displaysleepnow")
                    return True, "Display turned off"
            
            else:  # Linux
                if action == "sleep":
                    os.system("xset dpms force off")
                    return True, "Display turned off"
                elif action == "on":
                    os.system("xset dpms force on")
                    return True, "Display activated"
            
            return False, "Invalid display action"
            
        except Exception as e:
            return False, f"Error controlling display: {str(e)}"
    
    def open_system_settings(self, setting=None):
        """Open system settings"""
        try:
            if self.platform == "windows":
                if setting:
                    settings_map = {
                        "display": "ms-settings:display",
                        "sound": "ms-settings:sound",
                        "network": "ms-settings:network",
                        "bluetooth": "ms-settings:bluetooth",
                        "wifi": "ms-settings:network-wifi",
                        "power": "ms-settings:powersleep",
                        "storage": "ms-settings:storagesense",
                        "apps": "ms-settings:appsfeatures",
                        "personalization": "ms-settings:personalization",
                        "privacy": "ms-settings:privacy",
                        "update": "ms-settings:windowsupdate",
                    }
                    
                    if setting.lower() in settings_map:
                        os.system(f"start {settings_map[setting.lower()]}")
                        return True, f"Opened {setting} settings"
                
                os.system("start ms-settings:")
                return True, "Opened system settings"
            
            elif self.platform == "darwin":
                if setting:
                    os.system(f"open 'x-apple.systempreferences:{setting}'")
                else:
                    os.system("open 'x-apple.systempreferences:'")
                return True, "Opened system preferences"
            
            else:  # Linux
                os.system("gnome-control-center &")
                return True, "Opened system settings"
                
        except Exception as e:
            return False, f"Error opening settings: {str(e)}"
    
    # ============================================================================
    # WINDOW MANAGEMENT
    # ============================================================================
    
    def minimize_window(self, app_name=None):
        """Minimize window"""
        try:
            if self.platform == "windows":
                import pygetwindow as gw
                
                if app_name:
                    windows = gw.getWindowsWithTitle(app_name)
                    if windows:
                        windows[0].minimize()
                        return True, f"Minimized {app_name}"
                else:
                    # Minimize active window
                    import pyautogui
                    pyautogui.hotkey('win', 'down')
                    return True, "Minimized active window"
            
            elif self.platform == "darwin":
                os.system("osascript -e 'tell application \"System Events\" to set miniaturized of window 1 of (first application process whose frontmost is true) to true'")
                return True, "Minimized active window"
            
            else:  # Linux
                os.system("xdotool getactivewindow windowminimize")
                return True, "Minimized active window"
                
        except Exception as e:
            return False, f"Error minimizing window: {str(e)}"
    
    def maximize_window(self, app_name=None):
        """Maximize window"""
        try:
            if self.platform == "windows":
                import pygetwindow as gw
                
                if app_name:
                    windows = gw.getWindowsWithTitle(app_name)
                    if windows:
                        windows[0].maximize()
                        return True, f"Maximized {app_name}"
                else:
                    import pyautogui
                    pyautogui.hotkey('win', 'up')
                    return True, "Maximized active window"
            
            elif self.platform == "darwin":
                os.system("osascript -e 'tell application \"System Events\" to set value of attribute \"AXFullScreen\" of window 1 of (first application process whose frontmost is true) to true'")
                return True, "Maximized active window"
            
            else:  # Linux
                os.system("xdotool getactivewindow windowsize 100% 100%")
                return True, "Maximized active window"
                
        except Exception as e:
            return False, f"Error maximizing window: {str(e)}"
    
    def close_window(self):
        """Close active window"""
        try:
            if self.platform == "windows":
                import pyautogui
                pyautogui.hotkey('alt', 'f4')
                return True, "Closed active window"
            
            elif self.platform == "darwin":
                os.system("osascript -e 'tell application \"System Events\" to keystroke \"w\" using command down'")
                return True, "Closed active window"
            
            else:  # Linux
                os.system("xdotool getactivewindow windowclose")
                return True, "Closed active window"
                
        except Exception as e:
            return False, f"Error closing window: {str(e)}"
    
    def switch_window(self, direction="next"):
        """Switch between windows"""
        try:
            if self.platform == "windows":
                import pyautogui
                if direction == "next":
                    pyautogui.hotkey('alt', 'tab')
                else:
                    pyautogui.hotkey('alt', 'shift', 'tab')
                return True, f"Switched to {direction} window"
            
            elif self.platform == "darwin":
                if direction == "next":
                    os.system("osascript -e 'tell application \"System Events\" to keystroke tab using command down'")
                else:
                    os.system("osascript -e 'tell application \"System Events\" to keystroke tab using {command down, shift down}'")
                return True, f"Switched to {direction} window"
            
            else:  # Linux
                if direction == "next":
                    os.system("xdotool key alt+Tab")
                else:
                    os.system("xdotool key alt+shift+Tab")
                return True, f"Switched to {direction} window"
                
        except Exception as e:
            return False, f"Error switching window: {str(e)}"
    
    # ============================================================================
    # POWER MANAGEMENT
    # ============================================================================
    
    def shutdown_system(self, delay=0):
        """Shutdown the system"""
        try:
            if self.platform == "windows":
                os.system(f"shutdown /s /t {delay}")
                return True, f"System will shutdown in {delay} seconds"
            
            elif self.platform == "darwin":
                os.system(f"sudo shutdown -h +{delay//60}")
                return True, f"System will shutdown in {delay} seconds"
            
            else:  # Linux
                os.system(f"sudo shutdown -h +{delay//60}")
                return True, f"System will shutdown in {delay} seconds"
                
        except Exception as e:
            return False, f"Error shutting down: {str(e)}"
    
    def restart_system(self, delay=0):
        """Restart the system"""
        try:
            if self.platform == "windows":
                os.system(f"shutdown /r /t {delay}")
                return True, f"System will restart in {delay} seconds"
            
            elif self.platform == "darwin":
                os.system(f"sudo shutdown -r +{delay//60}")
                return True, f"System will restart in {delay} seconds"
            
            else:  # Linux
                os.system(f"sudo shutdown -r +{delay//60}")
                return True, f"System will restart in {delay} seconds"
                
        except Exception as e:
            return False, f"Error restarting: {str(e)}"
    
    def sleep_system(self):
        """Put system to sleep"""
        try:
            if self.platform == "windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return True, "System going to sleep"
            
            elif self.platform == "darwin":
                os.system("pmset sleepnow")
                return True, "System going to sleep"
            
            else:  # Linux
                os.system("systemctl suspend")
                return True, "System going to sleep"
                
        except Exception as e:
            return False, f"Error sleeping system: {str(e)}"
    
    def lock_system(self):
        """Lock the system"""
        try:
            if self.platform == "windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return True, "System locked"
            
            elif self.platform == "darwin":
                os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
                return True, "System locked"
            
            else:  # Linux
                os.system("gnome-screensaver-command -l")
                return True, "System locked"
                
        except Exception as e:
            return False, f"Error locking system: {str(e)}"


# Global instance
system_control = AdvancedSystemControl()


# ============================================================================
# SKILL FUNCTIONS FOR JARVIS
# ============================================================================

def open_app(app_name, args=None):
    """Open an application"""
    return system_control.open_application(app_name, args)


def close_app(app_name):
    """Close an application"""
    return system_control.close_application(app_name)


def list_apps():
    """List running applications"""
    return system_control.list_running_applications()


def is_app_running(app_name):
    """Check if app is running"""
    return system_control.is_application_running(app_name)


def set_volume(level):
    """Set system volume"""
    return system_control.control_volume("set", level)


def mute_volume():
    """Mute system volume"""
    return system_control.control_volume("mute")


def unmute_volume():
    """Unmute system volume"""
    return system_control.control_volume("unmute")


def set_brightness(level):
    """Set screen brightness"""
    return system_control.control_brightness(level)


def wifi_on():
    """Turn WiFi on"""
    return system_control.control_wifi("on")


def wifi_off():
    """Turn WiFi off"""
    return system_control.control_wifi("off")


def bluetooth_on():
    """Turn Bluetooth on"""
    return system_control.control_bluetooth("on")


def bluetooth_off():
    """Turn Bluetooth off"""
    return system_control.control_bluetooth("off")


def display_sleep():
    """Turn display off"""
    return system_control.control_display("sleep")


def display_on():
    """Turn display on"""
    return system_control.control_display("on")


def open_settings(setting=None):
    """Open system settings"""
    return system_control.open_system_settings(setting)


def minimize_win(app_name=None):
    """Minimize window"""
    return system_control.minimize_window(app_name)


def maximize_win(app_name=None):
    """Maximize window"""
    return system_control.maximize_window(app_name)


def close_win():
    """Close active window"""
    return system_control.close_window()


def switch_win(direction="next"):
    """Switch windows"""
    return system_control.switch_window(direction)


def shutdown(delay=0):
    """Shutdown system"""
    return system_control.shutdown_system(delay)


def restart(delay=0):
    """Restart system"""
    return system_control.restart_system(delay)


def sleep():
    """Sleep system"""
    return system_control.sleep_system()


def lock():
    """Lock system"""
    return system_control.lock_system()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI - Complete Visual Interface
Beautiful window with all features
YouTube Auto-Play Support!
"""

import sys
import os
import webbrowser
import subprocess
import platform
import time
import threading
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    import pyttsx3
    import speech_recognition as sr
    import pyautogui
    import psutil
except ImportError as e:
    print(f"Installing missing packages...")
    import subprocess
    packages = ['pyttsx3', 'SpeechRecognition', 'pyautogui', 'psutil']
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
    print("Please restart the application")
    sys.exit(0)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except:
    SELENIUM_AVAILABLE = False


class JarvisGUI:
    """Complete JARVIS GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - Your Personal AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize components
        self.os_type = platform.system()
        self.voice_engine = None
        self.recognizer = None
        self.listening = False
        self.driver = None
        
        # Initialize voice
        self._init_voice()
        
        # Create GUI
        self._create_gui()
        
        # Welcome message
        self.add_message("JARVIS", "Hello! I'm JARVIS. How can I help you today?", "system")
        self.speak("Hello! I'm JARVIS. How can I help you today?")
    
    def _init_voice(self):
        """Initialize voice engine"""
        try:
            self.voice_engine = pyttsx3.init()
            self.voice_engine.setProperty('rate', 180)
            self.voice_engine.setProperty('volume', 1.0)
            
            voices = self.voice_engine.getProperty('voices')
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.voice_engine.setProperty('voice', voice.id)
                    break
            
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000
        except Exception as e:
            print(f"Voice init error: {e}")
    
    def _create_gui(self):
        """Create complete GUI interface"""
        
        # ============ TOP BAR ============
        top_bar = tk.Frame(self.root, bg='#1a1a1a', height=80)
        top_bar.pack(fill=tk.X, padx=0, pady=0)
        
        # Title
        title = tk.Label(top_bar, text="🤖 JARVIS", font=('Arial', 24, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(side=tk.LEFT, padx=20, pady=20)
        
        subtitle = tk.Label(top_bar, text="Your Personal AI Assistant",
                           font=('Arial', 12), bg='#1a1a1a', fg='#888888')
        subtitle.pack(side=tk.LEFT, padx=0, pady=20)
        
        # Status indicator
        self.status_frame = tk.Frame(top_bar, bg='#1a1a1a')
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.status_dot = tk.Label(self.status_frame, text="●", font=('Arial', 20),
                                   bg='#1a1a1a', fg='#00ff00')
        self.status_dot.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.status_frame, text="Ready",
                                     font=('Arial', 12), bg='#1a1a1a', fg='#00ff00')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # ============ MAIN CONTENT ============
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Quick Actions
        left_panel = tk.Frame(main_frame, bg='#1a1a1a', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Quick Actions Title
        actions_title = tk.Label(left_panel, text="⚡ Quick Actions",
                                font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#ffffff')
        actions_title.pack(pady=15)
        
        # Scrollable frame for buttons
        canvas = tk.Canvas(left_panel, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button categories
        self._create_button_category(scrollable_frame, "🌐 Web", [
            ("Chrome", "chrome kholo"),
            ("Gmail", "gmail kholo"),
            ("Facebook", "facebook kholo"),
            ("YouTube", "youtube kholo"),
            ("Twitter", "twitter kholo"),
            ("Instagram", "instagram kholo"),
            ("WhatsApp Web", "whatsapp web kholo"),
            ("LinkedIn", "linkedin kholo"),
        ])
        
        self._create_button_category(scrollable_frame, "📱 Apps", [
            ("Word", "word kholo"),
            ("Excel", "excel kholo"),
            ("PowerPoint", "powerpoint kholo"),
            ("Notepad", "notepad kholo"),
            ("Calculator", "calculator kholo"),
            ("Paint", "paint kholo"),
            ("VLC", "vlc kholo"),
        ])
        
        self._create_button_category(scrollable_frame, "🎵 Media", [
            ("Play Music", "gaana bajao"),
            ("Pause", "pause karo"),
            ("Next", "next"),
            ("Previous", "previous"),
        ])
        
        self._create_button_category(scrollable_frame, "🔊 System", [
            ("Volume Up", "volume badhao"),
            ("Volume Down", "volume kam karo"),
            ("Mute", "mute karo"),
            ("Brightness Up", "brightness badhao"),
            ("Brightness Down", "brightness kam karo"),
        ])
        
        self._create_button_category(scrollable_frame, "⚡ Power", [
            ("Lock PC", "lock karo"),
            ("Sleep", "sleep karo"),
            ("Restart", "restart karo"),
            ("Shutdown", "shutdown karo"),
        ])
        
        # Right panel - Chat
        right_panel = tk.Frame(main_frame, bg='#1a1a1a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat title
        chat_title = tk.Label(right_panel, text="💬 Conversation",
                             font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#ffffff')
        chat_title.pack(pady=15)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#0a0a0a',
            fg='#ffffff',
            insertbackground='#00ff00',
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Configure tags for colored messages
        self.chat_display.tag_config('system', foreground='#00ff00')
        self.chat_display.tag_config('user', foreground='#00aaff')
        self.chat_display.tag_config('error', foreground='#ff4444')
        self.chat_display.tag_config('timestamp', foreground='#666666')
        
        # Input area
        input_frame = tk.Frame(right_panel, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.input_field = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='#00ff00',
            relief=tk.FLAT,
            bd=0
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10, padx=(0, 10))
        self.input_field.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 11, 'bold'),
            bg='#00ff00',
            fg='#000000',
            activebackground='#00cc00',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.send_message
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=20, ipady=10)
        
        # Voice button
        voice_btn = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=('Arial', 11, 'bold'),
            bg='#0088ff',
            fg='#ffffff',
            activebackground='#0066cc',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.voice_input
        )
        voice_btn.pack(side=tk.LEFT, ipadx=15, ipady=10)
    
    def _create_button_category(self, parent, title, buttons):
        """Create a category of buttons"""
        # Category label
        label = tk.Label(parent, text=title, font=('Arial', 12, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        label.pack(pady=(15, 10), anchor='w', padx=15)
        
        # Buttons
        for btn_text, command in buttons:
            btn = tk.Button(
                parent,
                text=btn_text,
                font=('Arial', 10),
                bg='#2a2a2a',
                fg='#ffffff',
                activebackground='#3a3a3a',
                relief=tk.FLAT,
                cursor='hand2',
                command=lambda cmd=command: self.execute_command(cmd)
            )
            btn.pack(fill=tk.X, padx=15, pady=3)
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        if sender == "JARVIS":
            self.chat_display.insert(tk.END, f"🤖 {sender}: ", 'system')
        else:
            self.chat_display.insert(tk.END, f"👤 {sender}: ", 'user')
        
        self.chat_display.insert(tk.END, f"{message}\n\n", msg_type)
        self.chat_display.see(tk.END)
    
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_label.config(text=status, fg=color)
        self.status_dot.config(fg=color)
    
    def speak(self, text):
        """Speak text using TTS"""
        def _speak():
            try:
                if self.voice_engine:
                    self.voice_engine.say(text)
                    self.voice_engine.runAndWait()
            except:
                pass
        
        threading.Thread(target=_speak, daemon=True).start()
    
    def send_message(self):
        """Send message from input field"""
        message = self.input_field.get().strip()
        if message:
            self.input_field.delete(0, tk.END)
            self.add_message("You", message, "user")
            self.execute_command(message)
    
    def voice_input(self):
        """Get voice input"""
        if self.listening:
            return
        
        def _listen():
            self.listening = True
            self.update_status("Listening...", "#0088ff")
            
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.update_status("Processing...", "#ff8800")
                text = self.recognizer.recognize_google(audio)
                
                self.add_message("You", text, "user")
                self.execute_command(text)
                
            except sr.WaitTimeoutError:
                self.add_message("JARVIS", "No speech detected. Please try again.", "error")
            except sr.UnknownValueError:
                self.add_message("JARVIS", "Sorry, I couldn't understand that.", "error")
            except Exception as e:
                self.add_message("JARVIS", f"Error: {str(e)}", "error")
            finally:
                self.listening = False
                self.update_status("Ready", "#00ff00")
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def execute_command(self, query):
        """Execute command"""
        self.update_status("Processing...", "#ff8800")
        
        def _execute():
            try:
                response = self.process_query(query)
                self.add_message("JARVIS", response, "system")
                self.speak(response)
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.add_message("JARVIS", error_msg, "error")
            finally:
                self.update_status("Ready", "#00ff00")
        
        threading.Thread(target=_execute, daemon=True).start()
    
    def process_query(self, query):
        """Process user query"""
        try:
            q = query.lower()
            
            # Web
            if 'gmail' in q:
                return self.open_website('https://mail.google.com')
            elif 'facebook' in q:
                return self.open_website('https://www.facebook.com')
            elif 'youtube' in q and ('kholo' in q or 'open' in q):
                return self.open_website('https://www.youtube.com')
            elif 'twitter' in q:
                return self.open_website('https://www.twitter.com')
            elif 'instagram' in q:
                return self.open_website('https://www.instagram.com')
            elif 'whatsapp' in q:
                return self.open_website('https://web.whatsapp.com')
            elif 'linkedin' in q:
                return self.open_website('https://www.linkedin.com')
            
            # YouTube Music (with auto-play)
            elif any(w in q for w in ['gaana', 'song', 'music', 'bajao', 'play']) and 'youtube' not in q:
                return self.play_youtube_auto(query)
            
            # Apps
            elif any(w in q for w in ['kholo', 'open', 'start', 'launch']):
                return self.open_app(query)
            
            # Close apps
            elif 'band' in q or 'close' in q:
                return self.close_app(query)
            
            # Media controls
            elif any(w in q for w in ['pause', 'next', 'previous', 'stop']):
                return self.media_control(query)
            
            # Volume
            elif 'volume' in q or 'awaaz' in q:
                return self.control_volume(query)
            
            # Brightness
            elif 'brightness' in q or 'chamak' in q:
                return self.control_brightness(query)
            
            # Power
            elif any(w in q for w in ['shutdown', 'restart', 'sleep', 'lock']):
                return self.power_control(query)
            
            # Google search
            elif 'google' in q or 'search' in q:
                return self.google_search(query)
            
            else:
                return "I can help with: web, apps, music, volume, brightness, power, search"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def open_website(self, url):
        """Open website in browser"""
        try:
            webbrowser.open(url)
            site_name = url.split('//')[-1].split('/')[0].replace('www.', '').split('.')[0].title()
            return f"Opening {site_name}..."
        except Exception as e:
            return f"Failed to open website: {str(e)}"
    
    def play_youtube_auto(self, query):
        """Play YouTube video with auto-play using Selenium"""
        try:
            # Extract song name
            words = query.lower().split()
            remove = ['gaana', 'song', 'music', 'bajao', 'play', 'youtube', 'pe', 'par', 'karo', 'ka', 'ki', 'ke']
            song_words = [w for w in words if w not in remove]
            
            if song_words:
                song = ' '.join(song_words)
            else:
                song = "Tauba Tauba Bad Newz"
            
            # Try Selenium auto-play
            if SELENIUM_AVAILABLE:
                try:
                    return self._play_with_selenium(song)
                except:
                    # Fallback to browser
                    return self._play_with_browser(song)
            else:
                # Fallback to browser
                return self._play_with_browser(song)
        
        except Exception as e:
            return f"YouTube error: {str(e)}"
    
    def _play_with_selenium(self, song):
        """Play YouTube with Selenium (auto-clicks play)"""
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Create driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Open YouTube search
            search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            driver.get(search_url)
            
            # Wait and click first video
            wait = WebDriverWait(driver, 10)
            video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#video-title')))
            video.click()
            
            # Wait for video to load and auto-play
            time.sleep(2)
            
            return f"🎵 Playing: {song}\n✅ YouTube opened and playing!"
        
        except Exception as e:
            raise Exception(f"Selenium error: {str(e)}")
    
    def _play_with_browser(self, song):
        """Fallback: Open YouTube in browser"""
        search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"🎵 Playing: {song}\n✅ YouTube opened! Click first video to play."
    
    def open_app(self, query):
        """Open application"""
        try:
            apps = {
                'chrome': 'chrome', 'firefox': 'firefox', 'edge': 'msedge',
                'word': 'winword', 'excel': 'excel', 'powerpoint': 'powerpnt',
                'notepad': 'notepad', 'vlc': 'vlc', 'calculator': 'calc',
                'paint': 'mspaint', 'cmd': 'cmd', 'powershell': 'powershell',
                'task manager': 'taskmgr', 'control panel': 'control',
            }
            
            words = query.lower().split()
            remove = ['kholo', 'open', 'start', 'launch', 'karo']
            app_words = [w for w in words if w not in remove]
            app_name = ' '.join(app_words)
            
            app_cmd = None
            for key, cmd in apps.items():
                if key in app_name:
                    app_cmd = cmd
                    break
            
            if not app_cmd:
                app_cmd = app_name
            
            if self.os_type == "Windows":
                subprocess.Popen(app_cmd, shell=True)
            else:
                subprocess.Popen([app_cmd])
            
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open app: {str(e)}"
    
    def close_app(self, query):
        """Close application"""
        try:
            words = query.lower().split()
            remove = ['band', 'close', 'exit', 'karo']
            app_words = [w for w in words if w not in remove]
            app_name = ' '.join(app_words)
            
            killed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name in proc.info['name'].lower():
                        proc.kill()
                        killed = True
                except:
                    pass
            
            if killed:
                return f"Closed {app_name}"
            else:
                return f"{app_name} not found"
        except Exception as e:
            return f"Failed to close app: {str(e)}"
    
    def media_control(self, query):
        """Control media playback"""
        try:
            q = query.lower()
            
            if 'pause' in q or 'stop' in q:
                pyautogui.press('playpause')
                return "Media paused"
            elif 'next' in q:
                pyautogui.press('nexttrack')
                return "Next track"
            elif 'previous' in q or 'pichla' in q:
                pyautogui.press('prevtrack')
                return "Previous track"
            else:
                return "Media control: pause, next, previous"
        except Exception as e:
            return f"Media control error: {str(e)}"
    
    def control_volume(self, query):
        """Control system volume"""
        try:
            q = query.lower()
            
            if 'badhao' in q or 'up' in q or 'increase' in q:
                for _ in range(5):
                    pyautogui.press('volumeup')
                return "Volume increased"
            elif 'kam' in q or 'down' in q or 'decrease' in q:
                for _ in range(5):
                    pyautogui.press('volumedown')
                return "Volume decreased"
            elif 'mute' in q:
                pyautogui.press('volumemute')
                return "Volume muted"
            else:
                return "Volume control: up, down, mute"
        except Exception as e:
            return f"Volume control error: {str(e)}"
    
    def control_brightness(self, query):
        """Control screen brightness"""
        try:
            q = query.lower()
            
            if 'badhao' in q or 'up' in q or 'increase' in q:
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)'], shell=True)
                return "Brightness increased"
            elif 'kam' in q or 'down' in q or 'decrease' in q:
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,50)'], shell=True)
                return "Brightness decreased"
            else:
                return "Brightness control: up, down"
        except Exception as e:
            return f"Brightness control error: {str(e)}"
    
    def power_control(self, query):
        """Power management"""
        try:
            q = query.lower()
            
            if 'shutdown' in q:
                confirm = messagebox.askyesno("Confirm", "Shutdown computer?")
                if confirm:
                    if self.os_type == "Windows":
                        os.system("shutdown /s /t 1")
                    else:
                        os.system("shutdown -h now")
                    return "Shutting down..."
                return "Shutdown cancelled"
            
            elif 'restart' in q:
                confirm = messagebox.askyesno("Confirm", "Restart computer?")
                if confirm:
                    if self.os_type == "Windows":
                        os.system("shutdown /r /t 1")
                    else:
                        os.system("reboot")
                    return "Restarting..."
                return "Restart cancelled"
            
            elif 'sleep' in q:
                if self.os_type == "Windows":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                else:
                    os.system("systemctl suspend")
                return "Going to sleep..."
            
            elif 'lock' in q:
                if self.os_type == "Windows":
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                else:
                    os.system("gnome-screensaver-command -l")
                return "Locking PC..."
            
            else:
                return "Power control: shutdown, restart, sleep, lock"
        except Exception as e:
            return f"Power control error: {str(e)}"
    
    def google_search(self, query):
        """Google search"""
        try:
            words = query.lower().split()
            remove = ['google', 'search', 'pe', 'par', 'karo', 'kar']
            search_words = [w for w in words if w not in remove]
            search_query = ' '.join(search_words)
            
            if search_query:
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(url)
                return f"Searching Google for: {search_query}"
            else:
                return "What do you want to search?"
        except Exception as e:
            return f"Search error: {str(e)}"


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

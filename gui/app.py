#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI - Complete Visual Interface
Beautiful window with all features
No terminal needed!
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
        
        # Logo and title
        title_frame = tk.Frame(top_bar, bg='#1a1a1a')
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(title_frame, text="🤖 JARVIS", font=("Arial", 24, "bold"), 
                bg='#1a1a1a', fg='#00d4ff').pack(side=tk.LEFT)
        tk.Label(title_frame, text="Your Personal AI Assistant", font=("Arial", 12), 
                bg='#1a1a1a', fg='#888888').pack(side=tk.LEFT, padx=10)
        
        # Status indicator
        self.status_frame = tk.Frame(top_bar, bg='#1a1a1a')
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.status_dot = tk.Label(self.status_frame, text="●", font=("Arial", 20), 
                                   bg='#1a1a1a', fg='#00ff88')
        self.status_dot.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(self.status_frame, text="Ready", font=("Arial", 12), 
                                     bg='#1a1a1a', fg='#00ff88')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # ============ MAIN CONTAINER ============
        main_container = tk.Frame(self.root, bg='#0a0a0a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ============ LEFT PANEL - QUICK ACTIONS ============
        left_panel = tk.Frame(main_container, bg='#1a1a1a', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Quick Actions Title
        tk.Label(left_panel, text="⚡ Quick Actions", font=("Arial", 14, "bold"), 
                bg='#1a1a1a', fg='#00d4ff').pack(pady=15)
        
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
        
        # Quick action buttons
        actions = [
            ("🌐 Web", [
                ("Chrome", lambda: self.execute_command("chrome kholo")),
                ("Gmail", lambda: self.open_website("https://gmail.com")),
                ("Facebook", lambda: self.open_website("https://facebook.com")),
                ("YouTube", lambda: self.open_website("https://youtube.com")),
                ("Twitter", lambda: self.open_website("https://twitter.com")),
                ("Instagram", lambda: self.open_website("https://instagram.com")),
                ("WhatsApp Web", lambda: self.open_website("https://web.whatsapp.com")),
                ("LinkedIn", lambda: self.open_website("https://linkedin.com")),
            ]),
            ("📱 Apps", [
                ("Word", lambda: self.execute_command("word kholo")),
                ("Excel", lambda: self.execute_command("excel kholo")),
                ("PowerPoint", lambda: self.execute_command("powerpoint kholo")),
                ("Notepad", lambda: self.execute_command("notepad kholo")),
                ("Calculator", lambda: self.execute_command("calculator kholo")),
                ("Paint", lambda: self.execute_command("paint kholo")),
                ("VLC", lambda: self.execute_command("vlc kholo")),
            ]),
            ("🎵 Media", [
                ("Play Music", lambda: self.execute_command("gaana bajao")),
                ("Pause", lambda: self.media_control("pause")),
                ("Next", lambda: self.media_control("next")),
                ("Previous", lambda: self.media_control("previous")),
            ]),
            ("🔊 System", [
                ("Volume Up", lambda: self.execute_command("volume badhao")),
                ("Volume Down", lambda: self.execute_command("volume kam karo")),
                ("Mute", lambda: self.execute_command("mute karo")),
                ("Brightness Up", lambda: self.execute_command("brightness badhao")),
                ("Brightness Down", lambda: self.execute_command("brightness kam karo")),
            ]),
            ("⚡ Power", [
                ("Lock PC", lambda: self.execute_command("lock karo")),
                ("Sleep", lambda: self.execute_command("sleep karo")),
                ("Restart", lambda: self.execute_command("restart karo")),
                ("Shutdown", lambda: self.execute_command("shutdown karo")),
            ]),
        ]
        
        for category, items in actions:
            # Category label
            tk.Label(scrollable_frame, text=category, font=("Arial", 11, "bold"), 
                    bg='#1a1a1a', fg='#00d4ff', anchor='w').pack(fill=tk.X, padx=10, pady=(10, 5))
            
            # Category buttons
            for name, command in items:
                btn = tk.Button(scrollable_frame, text=name, font=("Arial", 10), 
                              bg='#2a2a2a', fg='#ffffff', activebackground='#00d4ff',
                              activeforeground='#000000', relief=tk.FLAT, cursor='hand2',
                              command=command)
                btn.pack(fill=tk.X, padx=15, pady=2)
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#3a3a3a'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#2a2a2a'))
        
        # ============ RIGHT PANEL - CHAT & CONTROLS ============
        right_panel = tk.Frame(main_container, bg='#1a1a1a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display
        chat_frame = tk.Frame(right_panel, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(chat_frame, text="💬 Conversation", font=("Arial", 12, "bold"), 
                bg='#1a1a1a', fg='#00d4ff').pack(anchor='w', pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, font=("Consolas", 11),
            bg='#0a0a0a', fg='#ffffff', insertbackground='#00d4ff',
            relief=tk.FLAT, padx=15, pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for colored messages
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("jarvis", foreground="#00ff88", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#ffaa00", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("error", foreground="#ff4444", font=("Consolas", 11, "bold"))
        
        # Input area
        input_frame = tk.Frame(right_panel, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Text input
        self.input_field = tk.Entry(
            input_frame, font=("Arial", 12), bg='#2a2a2a', fg='#ffffff',
            insertbackground='#00d4ff', relief=tk.FLAT
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_btn = tk.Button(
            input_frame, text="📤 Send", font=("Arial", 11, "bold"),
            bg='#00d4ff', fg='#000000', activebackground='#00a8cc',
            relief=tk.FLAT, cursor='hand2', command=self.send_message, width=10
        )
        self.send_btn.pack(side=tk.LEFT, ipady=8)
        
        # Voice button
        self.voice_btn = tk.Button(
            input_frame, text="🎤 Voice", font=("Arial", 11, "bold"),
            bg='#2a2a2a', fg='#ffffff', activebackground='#00ff88',
            relief=tk.FLAT, cursor='hand2', command=self.toggle_voice, width=10
        )
        self.voice_btn.pack(side=tk.LEFT, padx=(10, 0), ipady=8)
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        
        if msg_type == "user":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"👤 You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n")
        elif msg_type == "jarvis":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"🤖 JARVIS: ", "jarvis")
            self.chat_display.insert(tk.END, f"{message}\n")
        elif msg_type == "system":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"ℹ️  {sender}: ", "system")
            self.chat_display.insert(tk.END, f"{message}\n")
        elif msg_type == "error":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"❌ Error: ", "error")
            self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_label.config(text=status, fg=color)
        self.status_dot.config(fg=color)
    
    def speak(self, text):
        """Speak text"""
        try:
            if self.voice_engine:
                self.voice_engine.say(text)
                self.voice_engine.runAndWait()
        except:
            pass
    
    def send_message(self):
        """Send text message"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message("You", message, "user")
        
        # Process command
        threading.Thread(target=self._process_command, args=(message,), daemon=True).start()
    
    def toggle_voice(self):
        """Toggle voice input"""
        if self.listening:
            self.listening = False
            self.voice_btn.config(text="🎤 Voice", bg='#2a2a2a')
            self.update_status("Ready", "#00ff88")
        else:
            self.listening = True
            self.voice_btn.config(text="⏹️ Stop", bg='#ff4444')
            threading.Thread(target=self._voice_loop, daemon=True).start()
    
    def _voice_loop(self):
        """Voice input loop"""
        while self.listening:
            try:
                self.update_status("Listening...", "#00d4ff")
                
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.update_status("Processing...", "#ffaa00")
                text = self.recognizer.recognize_google(audio)
                
                self.add_message("You", text, "user")
                self._process_command(text)
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.add_message("Error", str(e), "error")
                break
        
        self.update_status("Ready", "#00ff88")
    
    def _process_command(self, command):
        """Process user command"""
        self.update_status("Processing...", "#ffaa00")
        
        try:
            response = self.execute_command(command)
            self.add_message("JARVIS", response, "jarvis")
            self.speak(response)
        except Exception as e:
            self.add_message("Error", str(e), "error")
        
        self.update_status("Ready", "#00ff88")
    
    def execute_command(self, query):
        """Execute command"""
        q = query.lower()
        
        try:
            # Web URLs
            if 'gmail' in q:
                return self.open_website("https://gmail.com")
            elif 'facebook' in q:
                return self.open_website("https://facebook.com")
            elif 'youtube' in q and 'bajao' not in q:
                return self.open_website("https://youtube.com")
            elif 'twitter' in q:
                return self.open_website("https://twitter.com")
            elif 'instagram' in q:
                return self.open_website("https://instagram.com")
            elif 'whatsapp' in q and 'web' in q:
                return self.open_website("https://web.whatsapp.com")
            elif 'linkedin' in q:
                return self.open_website("https://linkedin.com")
            
            # YouTube/Music
            elif any(w in q for w in ['gaana', 'song', 'music', 'bajao']):
                return self.play_youtube(query)
            
            # Open app
            elif any(w in q for w in ['kholo', 'open', 'start', 'launch']):
                return self.open_app(query)
            
            # Close app
            elif any(w in q for w in ['band', 'close', 'exit']):
                return self.close_app(query)
            
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
    
    def play_youtube(self, query):
        """Play YouTube video"""
        try:
            words = query.lower().split()
            remove = ['gaana', 'song', 'music', 'bajao', 'play', 'youtube', 'pe', 'par', 'karo']
            song_words = [w for w in words if w not in remove]
            
            if song_words:
                song = ' '.join(song_words)
            else:
                song = "Tauba Tauba Bad Newz"
            
            # Open YouTube search
            search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            return f"Playing: {song}\n✅ YouTube opened!"
        except Exception as e:
            return f"YouTube error: {str(e)}"
    
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
                return f"{app_name} is not running"
        except Exception as e:
            return f"Failed to close app: {str(e)}"
    
    def control_volume(self, query):
        """Control volume"""
        try:
            if 'badhao' in query or 'increase' in query or 'up' in query:
                for _ in range(5):
                    pyautogui.press('volumeup')
                return "Volume increased"
            elif 'kam' in query or 'decrease' in query or 'down' in query:
                for _ in range(5):
                    pyautogui.press('volumedown')
                return "Volume decreased"
            elif 'mute' in query or 'chup' in query:
                pyautogui.press('volumemute')
                return "Volume muted"
        except Exception as e:
            return f"Volume control failed: {str(e)}"
    
    def control_brightness(self, query):
        """Control brightness"""
        try:
            if 'badhao' in query or 'increase' in query:
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)'])
                return "Brightness increased"
            elif 'kam' in query or 'decrease' in query:
                if self.os_type == "Windows":
                    subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,50)'])
                return "Brightness decreased"
        except Exception as e:
            return f"Brightness control failed: {str(e)}"
    
    def power_control(self, query):
        """Power control"""
        try:
            if 'shutdown' in query:
                if messagebox.askyesno("Confirm", "Shutdown PC in 10 seconds?"):
                    if self.os_type == "Windows":
                        subprocess.run(['shutdown', '/s', '/t', '10'])
                    return "Shutting down in 10 seconds..."
            elif 'restart' in query:
                if messagebox.askyesno("Confirm", "Restart PC in 10 seconds?"):
                    if self.os_type == "Windows":
                        subprocess.run(['shutdown', '/r', '/t', '10'])
                    return "Restarting in 10 seconds..."
            elif 'sleep' in query:
                if self.os_type == "Windows":
                    subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
                return "Going to sleep..."
            elif 'lock' in query:
                if self.os_type == "Windows":
                    subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
                return "Locking PC..."
        except Exception as e:
            return f"Power control failed: {str(e)}"
    
    def google_search(self, query):
        """Google search"""
        try:
            words = query.lower().replace('google', '').replace('search', '').replace('pe', '').replace('karo', '').strip()
            
            if words:
                webbrowser.open(f"https://www.google.com/search?q={words}")
                return f"Searching Google for: {words}"
            else:
                webbrowser.open("https://www.google.com")
                return "Opening Google..."
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def media_control(self, action):
        """Media control"""
        try:
            if action == "pause":
                pyautogui.press('playpause')
                return "Media toggled"
            elif action == "next":
                pyautogui.press('nexttrack')
                return "Next track"
            elif action == "previous":
                pyautogui.press('prevtrack')
                return "Previous track"
        except Exception as e:
            return f"Media control failed: {str(e)}"


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI - Complete Visual Interface
✅ YouTube Auto-Play
✅ Browser Auto-Login (Google)
✅ PC Movie Search
✅ VLC Auto-Play
"""

import sys
import os
import webbrowser
import subprocess
import platform
import time
import threading
import json
import glob
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
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
        
        # Config file for credentials
        self.config_file = Path.home() / ".jarvis_config.json"
        self.config = self._load_config()
        
        # Movie search paths
        self.movie_paths = self._get_default_movie_paths()
        
        # Initialize voice
        self._init_voice()
        
        # Create GUI
        self._create_gui()
        
        # Welcome message
        welcome = "Hello! I'm JARVIS. I can auto-login browsers, search movies on PC, and play them in VLC!"
        self.add_message("JARVIS", welcome, "system")
        self.speak("Hello! I'm JARVIS.")
    
    def _load_config(self):
        """Load saved configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'google_email': '',
            'google_password': '',
            'movie_paths': []
        }
    
    def _save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")
    
    def _get_default_movie_paths(self):
        """Get default movie search paths"""
        paths = []
        
        if self.os_type == "Windows":
            # Common Windows paths
            drives = ['C:', 'D:', 'E:', 'F:']
            folders = ['Movies', 'Videos', 'Downloads', 'Desktop']
            
            for drive in drives:
                for folder in folders:
                    path = Path(f"{drive}\\Users\\{os.getlogin()}\\{folder}")
                    if path.exists():
                        paths.append(str(path))
                    
                    # Root folders
                    path = Path(f"{drive}\\{folder}")
                    if path.exists():
                        paths.append(str(path))
        else:
            # Linux/Mac paths
            home = Path.home()
            folders = ['Movies', 'Videos', 'Downloads', 'Desktop']
            for folder in folders:
                path = home / folder
                if path.exists():
                    paths.append(str(path))
        
        # Add custom paths from config
        if self.config.get('movie_paths'):
            paths.extend(self.config['movie_paths'])
        
        return list(set(paths))  # Remove duplicates
    
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
        
        subtitle = tk.Label(top_bar, text="Auto-Login | Movie Search | VLC Play",
                           font=('Arial', 12), bg='#1a1a1a', fg='#888888')
        subtitle.pack(side=tk.LEFT, padx=0, pady=20)
        
        # Settings button
        settings_btn = tk.Button(
            top_bar,
            text="⚙️ Settings",
            font=('Arial', 10, 'bold'),
            bg='#2a2a2a',
            fg='#ffffff',
            activebackground='#3a3a3a',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.open_settings
        )
        settings_btn.pack(side=tk.RIGHT, padx=20, pady=20, ipadx=10, ipady=5)
        
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
        self._create_button_category(scrollable_frame, "🌐 Web (Auto-Login)", [
            ("Gmail (Login)", "gmail login karo"),
            ("Facebook (Login)", "facebook login karo"),
            ("YouTube (Login)", "youtube login karo"),
            ("Twitter (Login)", "twitter login karo"),
        ])
        
        self._create_button_category(scrollable_frame, "🎬 Movies", [
            ("Search Movie", "movie search karo"),
            ("Play in VLC", "movie play karo vlc me"),
        ])
        
        self._create_button_category(scrollable_frame, "📱 Apps", [
            ("Chrome", "chrome kholo"),
            ("Word", "word kholo"),
            ("Excel", "excel kholo"),
            ("VLC", "vlc kholo"),
            ("Notepad", "notepad kholo"),
            ("Calculator", "calculator kholo"),
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
        ])
        
        self._create_button_category(scrollable_frame, "⚡ Power", [
            ("Lock PC", "lock karo"),
            ("Sleep", "sleep karo"),
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
    
    def open_settings(self):
        """Open settings window"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("⚙️ JARVIS Settings")
        settings_win.geometry("600x500")
        settings_win.configure(bg='#1a1a1a')
        
        # Title
        title = tk.Label(settings_win, text="⚙️ Settings", font=('Arial', 18, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=20)
        
        # Google Credentials
        cred_frame = tk.LabelFrame(settings_win, text="Google Auto-Login", font=('Arial', 12, 'bold'),
                                   bg='#1a1a1a', fg='#ffffff', padx=20, pady=20)
        cred_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(cred_frame, text="Email:", bg='#1a1a1a', fg='#ffffff').grid(row=0, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(cred_frame, width=40, bg='#2a2a2a', fg='#ffffff')
        email_entry.grid(row=0, column=1, pady=5, padx=10)
        email_entry.insert(0, self.config.get('google_email', ''))
        
        tk.Label(cred_frame, text="Password:", bg='#1a1a1a', fg='#ffffff').grid(row=1, column=0, sticky='w', pady=5)
        pass_entry = tk.Entry(cred_frame, width=40, show='*', bg='#2a2a2a', fg='#ffffff')
        pass_entry.grid(row=1, column=1, pady=5, padx=10)
        pass_entry.insert(0, self.config.get('google_password', ''))
        
        # Movie Paths
        path_frame = tk.LabelFrame(settings_win, text="Movie Search Paths", font=('Arial', 12, 'bold'),
                                   bg='#1a1a1a', fg='#ffffff', padx=20, pady=20)
        path_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        path_list = tk.Listbox(path_frame, bg='#2a2a2a', fg='#ffffff', height=6)
        path_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for path in self.movie_paths:
            path_list.insert(tk.END, path)
        
        path_btn_frame = tk.Frame(path_frame, bg='#1a1a1a')
        path_btn_frame.pack(fill=tk.X, pady=5)
        
        def add_path():
            path = filedialog.askdirectory(title="Select Movie Folder")
            if path:
                path_list.insert(tk.END, path)
        
        def remove_path():
            selection = path_list.curselection()
            if selection:
                path_list.delete(selection)
        
        tk.Button(path_btn_frame, text="Add Folder", command=add_path,
                 bg='#00ff00', fg='#000000').pack(side=tk.LEFT, padx=5)
        tk.Button(path_btn_frame, text="Remove", command=remove_path,
                 bg='#ff4444', fg='#ffffff').pack(side=tk.LEFT, padx=5)
        
        # Save button
        def save_settings():
            self.config['google_email'] = email_entry.get()
            self.config['google_password'] = pass_entry.get()
            self.config['movie_paths'] = list(path_list.get(0, tk.END))
            self._save_config()
            self.movie_paths = self._get_default_movie_paths()
            messagebox.showinfo("Success", "Settings saved!")
            settings_win.destroy()
        
        save_btn = tk.Button(settings_win, text="💾 Save Settings", font=('Arial', 12, 'bold'),
                            bg='#00ff00', fg='#000000', command=save_settings)
        save_btn.pack(pady=20, ipadx=20, ipady=10)
    
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
            
            # Auto-Login Web
            if 'login' in q:
                if 'gmail' in q:
                    return self.auto_login_website('gmail')
                elif 'facebook' in q:
                    return self.auto_login_website('facebook')
                elif 'youtube' in q:
                    return self.auto_login_website('youtube')
                elif 'twitter' in q:
                    return self.auto_login_website('twitter')
            
            # Movie commands
            elif any(w in q for w in ['movie', 'film', 'video']):
                if 'search' in q or 'dhundo' in q or 'find' in q:
                    # Extract movie name
                    words = q.split()
                    remove = ['movie', 'film', 'video', 'search', 'dhundo', 'find', 'karo', 'kar']
                    movie_words = [w for w in words if w not in remove]
                    movie_name = ' '.join(movie_words) if movie_words else None
                    return self.search_movie(movie_name)
                elif 'play' in q or 'chalao' in q or 'bajao' in q:
                    # Extract movie name and play
                    words = q.split()
                    remove = ['movie', 'film', 'video', 'play', 'chalao', 'bajao', 'karo', 'kar', 'vlc', 'me', 'pe']
                    movie_words = [w for w in words if w not in remove]
                    movie_name = ' '.join(movie_words) if movie_words else None
                    return self.play_movie_vlc(movie_name)
            
            # Web (without login)
            elif 'gmail' in q and 'login' not in q:
                return self.open_website('https://mail.google.com')
            elif 'facebook' in q and 'login' not in q:
                return self.open_website('https://www.facebook.com')
            elif 'youtube' in q and ('kholo' in q or 'open' in q):
                return self.open_website('https://www.youtube.com')
            
            # YouTube Music (with auto-play)
            elif any(w in q for w in ['gaana', 'song', 'music', 'bajao', 'play']) and 'movie' not in q:
                return self.play_youtube_auto(query)
            
            # Apps
            elif any(w in q for w in ['kholo', 'open', 'start', 'launch']) and 'movie' not in q:
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
            
            # Power
            elif any(w in q for w in ['shutdown', 'restart', 'sleep', 'lock']):
                return self.power_control(query)
            
            else:
                return "I can help with: auto-login, movie search, VLC play, web, apps, music, volume, power"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def auto_login_website(self, site):
        """Auto-login to website using Selenium"""
        if not SELENIUM_AVAILABLE:
            return "Selenium not available. Install: pip install selenium webdriver-manager"
        
        email = self.config.get('google_email')
        password = self.config.get('google_password')
        
        if not email or not password:
            return "⚠️ Please set Google credentials in Settings first!"
        
        try:
            # Setup Chrome
            chrome_options = Options()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Site URLs
            urls = {
                'gmail': 'https://mail.google.com',
                'youtube': 'https://www.youtube.com',
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com'
            }
            
            url = urls.get(site, 'https://www.google.com')
            driver.get(url)
            
            # Wait for page load
            time.sleep(2)
            
            # Google login (for Gmail/YouTube)
            if site in ['gmail', 'youtube']:
                try:
                    # Email
                    email_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "identifier"))
                    )
                    email_field.send_keys(email)
                    email_field.send_keys(Keys.RETURN)
                    
                    time.sleep(2)
                    
                    # Password
                    pass_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    pass_field.send_keys(password)
                    pass_field.send_keys(Keys.RETURN)
                    
                    return f"✅ Logged into {site.title()}!\n🌐 Browser opened with auto-login"
                except:
                    return f"⚠️ {site.title()} opened, but auto-login failed. Please login manually."
            
            # Facebook login
            elif site == 'facebook':
                try:
                    email_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "email"))
                    )
                    email_field.send_keys(email)
                    
                    pass_field = driver.find_element(By.ID, "pass")
                    pass_field.send_keys(password)
                    pass_field.send_keys(Keys.RETURN)
                    
                    return f"✅ Logged into Facebook!\n🌐 Browser opened with auto-login"
                except:
                    return "⚠️ Facebook opened, but auto-login failed. Please login manually."
            
            else:
                return f"✅ {site.title()} opened!"
        
        except Exception as e:
            return f"Login error: {str(e)}"
    
    def search_movie(self, movie_name=None):
        """Search for movie in PC storage"""
        if not movie_name:
            return "Please specify movie name. Example: 'search movie Avengers'"
        
        self.update_status("Searching PC...", "#ff8800")
        
        found_movies = []
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        
        # Search in all paths
        for base_path in self.movie_paths:
            try:
                for ext in video_extensions:
                    pattern = f"{base_path}/**/*{movie_name}*{ext}"
                    matches = glob.glob(pattern, recursive=True)
                    found_movies.extend(matches)
            except Exception as e:
                print(f"Search error in {base_path}: {e}")
        
        if found_movies:
            result = f"🎬 Found {len(found_movies)} movie(s):\n\n"
            for i, movie in enumerate(found_movies[:5], 1):  # Show max 5
                movie_file = Path(movie).name
                result += f"{i}. {movie_file}\n"
            
            if len(found_movies) > 5:
                result += f"\n... and {len(found_movies) - 5} more"
            
            # Store for later play
            self.last_search_results = found_movies
            
            return result
        else:
            return f"❌ No movies found with name: {movie_name}\n💡 Try: Settings → Add movie folders"
    
    def play_movie_vlc(self, movie_name=None):
        """Search and play movie in VLC"""
        if not movie_name:
            # Try to play first from last search
            if hasattr(self, 'last_search_results') and self.last_search_results:
                movie_path = self.last_search_results[0]
            else:
                return "Please specify movie name. Example: 'play movie Avengers in VLC'"
        else:
            # Search for movie
            self.update_status("Searching movie...", "#ff8800")
            
            found_movies = []
            video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
            
            for base_path in self.movie_paths:
                try:
                    for ext in video_extensions:
                        pattern = f"{base_path}/**/*{movie_name}*{ext}"
                        matches = glob.glob(pattern, recursive=True)
                        found_movies.extend(matches)
                except:
                    pass
            
            if not found_movies:
                return f"❌ Movie not found: {movie_name}\n💡 Try: Settings → Add movie folders"
            
            movie_path = found_movies[0]
        
        # Play in VLC
        try:
            movie_file = Path(movie_path).name
            
            if self.os_type == "Windows":
                # Try common VLC paths
                vlc_paths = [
                    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                    r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                ]
                
                vlc_exe = None
                for path in vlc_paths:
                    if Path(path).exists():
                        vlc_exe = path
                        break
                
                if vlc_exe:
                    subprocess.Popen([vlc_exe, movie_path])
                else:
                    # Try default
                    os.startfile(movie_path)
            else:
                # Linux/Mac
                subprocess.Popen(['vlc', movie_path])
            
            return f"🎬 Playing in VLC:\n{movie_file}\n✅ Movie started!"
        
        except Exception as e:
            return f"VLC error: {str(e)}\n💡 Make sure VLC is installed"
    
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
                    return self._play_with_browser(song)
            else:
                return self._play_with_browser(song)
        
        except Exception as e:
            return f"YouTube error: {str(e)}"
    
    def _play_with_selenium(self, song):
        """Play YouTube with Selenium (auto-clicks play)"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            driver.get(search_url)
            
            wait = WebDriverWait(driver, 10)
            video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#video-title')))
            video.click()
            
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


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

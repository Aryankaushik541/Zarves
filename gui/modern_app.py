#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS Modern GUI - Enhanced AI Agent Integration
✅ Threaded AI processing (no freezing)
✅ Real-time status updates
✅ Smart intent detection
✅ Conversation memory
✅ Multi-language support (Hindi + English)
✅ Modern dark theme
"""

import sys
import os
import time
import threading
import queue
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
except ImportError:
    print("Installing tkinter...")
    sys.exit(1)

# Import JARVIS core components
try:
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from core.voice import VoiceAssistant
    JARVIS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ JARVIS core not available: {e}")
    JARVIS_AVAILABLE = False


class ModernJarvisGUI:
    """Modern JARVIS GUI with Enhanced AI Agent"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - AI Assistant (Enhanced)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Command queue for threaded processing
        self.command_queue = queue.Queue()
        self.processing = False
        
        # Initialize JARVIS components
        self.registry = None
        self.engine = None
        self.voice = None
        self.listening = False
        
        # Conversation history
        self.conversation_history = []
        
        # Config
        self.config_file = Path.home() / ".jarvis_config.json"
        self.config = self._load_config()
        
        # Stats
        self.stats = {
            'total_skills': 0,
            'total_tools': 0,
            'queries_processed': 0,
            'success_rate': 100.0,
            'session_start': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Create GUI
        self._create_modern_gui()
        
        # Initialize JARVIS in background
        self.update_status("🔄 Initializing JARVIS...", "#ff8800")
        threading.Thread(target=self._init_jarvis, daemon=True).start()
        
        # Start command processor
        threading.Thread(target=self._process_commands, daemon=True).start()
    
    def _load_config(self):
        """Load configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'theme': 'dark',
            'voice_enabled': True,
            'auto_execute': False,
            'language': 'hi-IN'
        }
    
    def _save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")
    
    def _create_modern_gui(self):
        """Create modern GUI interface"""
        
        # ============ HEADER ============
        header = tk.Frame(self.root, bg='#1a1a1a', height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Title with gradient effect
        title_frame = tk.Frame(header, bg='#1a1a1a')
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title = tk.Label(
            title_frame, 
            text="🤖 JARVIS", 
            font=('Arial', 26, 'bold'),
            bg='#1a1a1a', 
            fg='#00ff88'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Enhanced AI Assistant",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        subtitle.pack()
        
        # Status indicator
        status_frame = tk.Frame(header, bg='#1a1a1a')
        status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=('Arial', 20),
            bg='#1a1a1a',
            fg='#ff8800'
        )
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Initializing...",
            font=('Arial', 12, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # ============ MAIN CONTENT ============
        main_container = tk.Frame(self.root, bg='#0a0a0a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Chat
        left_panel = tk.Frame(main_container, bg='#0a0a0a')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Chat header
        chat_header = tk.Frame(left_panel, bg='#1a1a1a', height=40)
        chat_header.pack(fill=tk.X, pady=(0, 5))
        chat_header.pack_propagate(False)
        
        tk.Label(
            chat_header,
            text="💬 Conversation",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # Clear button
        clear_btn = tk.Button(
            chat_header,
            text="🗑️ Clear",
            font=('Arial', 10),
            bg='#2a2a2a',
            fg='#ffffff',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._clear_chat
        )
        clear_btn.pack(side=tk.RIGHT, padx=10)
        
        # Chat display with custom styling
        chat_frame = tk.Frame(left_panel, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg='#1a1a1a',
            fg='#ffffff',
            insertbackground='#00ff88',
            selectbackground='#2a4a3a',
            bd=0,
            padx=15,
            pady=10,
            state='disabled'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config('user', foreground='#00ff88', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('jarvis', foreground='#4488ff', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('system', foreground='#ff8800', font=('Consolas', 10, 'italic'))
        self.chat_display.tag_config('error', foreground='#ff4444', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config('timestamp', foreground='#666666', font=('Consolas', 9))
        
        # Right panel - Stats & Controls
        right_panel = tk.Frame(main_container, bg='#1a1a1a', width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Stats section
        stats_header = tk.Label(
            right_panel,
            text="📊 Statistics",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        stats_header.pack(pady=(15, 10), padx=15, anchor='w')
        
        self.stats_frame = tk.Frame(right_panel, bg='#1a1a1a')
        self.stats_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self._create_stat_item("Skills Loaded", "0", "🎯")
        self._create_stat_item("Tools Available", "0", "🔧")
        self._create_stat_item("Queries Processed", "0", "💬")
        self._create_stat_item("Success Rate", "100%", "✅")
        
        # Separator
        tk.Frame(right_panel, bg='#2a2a2a', height=1).pack(fill=tk.X, padx=15, pady=15)
        
        # Quick Actions
        actions_header = tk.Label(
            right_panel,
            text="⚡ Quick Actions",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        actions_header.pack(pady=(10, 10), padx=15, anchor='w')
        
        actions = [
            ("🎵 YouTube", self._quick_youtube),
            ("🌐 Browser", self._quick_browser),
            ("🎬 Movies", self._quick_movies),
            ("🔍 Search", self._quick_search),
            ("⚙️ Settings", self._open_settings)
        ]
        
        for text, command in actions:
            btn = tk.Button(
                right_panel,
                text=text,
                font=('Arial', 11),
                bg='#2a2a2a',
                fg='#ffffff',
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=command,
                anchor='w'
            )
            btn.pack(fill=tk.X, padx=15, pady=3)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#3a3a3a'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2a2a2a'))
        
        # ============ INPUT AREA ============
        input_container = tk.Frame(self.root, bg='#1a1a1a', height=80)
        input_container.pack(fill=tk.X, padx=10, pady=(0, 10))
        input_container.pack_propagate(False)
        
        # Input frame
        input_frame = tk.Frame(input_container, bg='#1a1a1a')
        input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Text input
        self.input_entry = tk.Entry(
            input_frame,
            font=('Arial', 13),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='#00ff88',
            bd=0,
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), ipady=8)
        self.input_entry.bind('<Return>', lambda e: self._send_command())
        
        # Placeholder text
        self.input_entry.insert(0, "Type your command here...")
        self.input_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.input_entry.bind('<FocusOut>', self._on_entry_focus_out)
        self.input_entry.config(fg='#666666')
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 12, 'bold'),
            bg='#00ff88',
            fg='#000000',
            bd=0,
            padx=25,
            pady=8,
            cursor='hand2',
            command=self._send_command
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Voice button
        self.voice_btn = tk.Button(
            input_frame,
            text="🎤",
            font=('Arial', 18),
            bg='#2a2a2a',
            fg='#ffffff',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._toggle_voice
        )
        self.voice_btn.pack(side=tk.LEFT)
    
    def _create_stat_item(self, label, value, icon):
        """Create a stat display item"""
        frame = tk.Frame(self.stats_frame, bg='#1a1a1a')
        frame.pack(fill=tk.X, pady=5)
        
        icon_label = tk.Label(
            frame,
            text=icon,
            font=('Arial', 14),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        text_frame = tk.Frame(frame, bg='#1a1a1a')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        label_widget = tk.Label(
            text_frame,
            text=label,
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#888888',
            anchor='w'
        )
        label_widget.pack(anchor='w')
        
        value_widget = tk.Label(
            text_frame,
            text=value,
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        )
        value_widget.pack(anchor='w')
        
        # Store reference for updates
        setattr(self, f'stat_{label.lower().replace(" ", "_")}', value_widget)
    
    def _on_entry_focus_in(self, event):
        """Handle input focus in"""
        if self.input_entry.get() == "Type your command here...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg='#ffffff')
    
    def _on_entry_focus_out(self, event):
        """Handle input focus out"""
        if not self.input_entry.get():
            self.input_entry.insert(0, "Type your command here...")
            self.input_entry.config(fg='#666666')
    
    def _init_jarvis(self):
        """Initialize JARVIS engine"""
        try:
            if not JARVIS_AVAILABLE:
                self.add_message("SYSTEM", "⚠️ JARVIS core not available. Running in demo mode.", "error")
                self.update_status("Demo Mode", "#ff8800")
                return
            
            # Initialize registry
            self.add_message("SYSTEM", "📦 Loading skills...", "system")
            self.registry = SkillRegistry()
            
            # Load skills from skill folder
            skills_dir = Path(__file__).parent.parent / "skill"
            if skills_dir.exists():
                self.registry.load_skills(str(skills_dir))
            
            # Get stats
            self.stats['total_skills'] = len(self.registry.list_skills())
            self.stats['total_tools'] = len(self.registry.list_tools())
            
            # Initialize engine
            self.add_message("SYSTEM", "🧠 Initializing AI engine...", "system")
            self.engine = JarvisEngine(self.registry)
            
            # Initialize voice
            try:
                self.voice = VoiceAssistant()
                self.add_message("SYSTEM", "🎤 Voice assistant ready!", "system")
            except:
                self.add_message("SYSTEM", "⚠️ Voice not available", "error")
            
            # Update UI
            self._update_stats_display()
            
            # Welcome message
            welcome = f"✅ JARVIS Enhanced Ready!\n\n📊 Loaded {self.stats['total_skills']} skills with {self.stats['total_tools']} tools\n\n💬 How can I help you today?"
            self.add_message("JARVIS", welcome, "jarvis")
            
            if self.voice:
                threading.Thread(
                    target=lambda: self.voice.speak("JARVIS ready! How can I help you?"),
                    daemon=True
                ).start()
            
            self.update_status("Ready", "#00ff88")
            
        except Exception as e:
            error_msg = f"❌ Initialization failed: {str(e)}\n\n💡 Make sure Ollama is running:\n   ollama serve"
            self.add_message("SYSTEM", error_msg, "error")
            self.update_status("Error", "#ff4444")
    
    def _process_commands(self):
        """Background thread for processing commands"""
        while True:
            try:
                command = self.command_queue.get()
                if command:
                    self._execute_command(command)
            except Exception as e:
                self.add_message("SYSTEM", f"❌ Error: {str(e)}", "error")
            finally:
                self.processing = False
    
    def _execute_command(self, command):
        """Execute a command through JARVIS engine"""
        try:
            self.update_status("Processing...", "#ff8800")
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': command,
                'timestamp': datetime.now().isoformat()
            })
            
            # Display user message
            self.add_message("You", command, "user")
            
            # Get AI response
            if self.engine:
                response = self.engine.process_query(command)
                
                # Display JARVIS response
                self.add_message("JARVIS", response, "jarvis")
                
                # Speak response if voice enabled
                if self.voice and self.config.get('voice_enabled', True):
                    threading.Thread(
                        target=lambda: self.voice.speak(response),
                        daemon=True
                    ).start()
                
                # Update stats
                self.stats['queries_processed'] += 1
                self._update_stats_display()
            else:
                self.add_message("JARVIS", "Engine not initialized yet. Please wait...", "error")
            
            self.update_status("Ready", "#00ff88")
            
        except Exception as e:
            self.add_message("SYSTEM", f"❌ Execution error: {str(e)}", "error")
            self.update_status("Error", "#ff4444")
    
    def _send_command(self):
        """Send command from input"""
        command = self.input_entry.get().strip()
        
        if command and command != "Type your command here..." and not self.processing:
            self.processing = True
            self.input_entry.delete(0, tk.END)
            self.command_queue.put(command)
    
    def _toggle_voice(self):
        """Toggle voice listening"""
        if not self.voice:
            self.add_message("SYSTEM", "⚠️ Voice not available", "error")
            return
        
        if not self.listening:
            self.listening = True
            self.voice_btn.config(bg='#ff4444')
            self.update_status("Listening...", "#ff4444")
            
            # Start listening in background
            threading.Thread(target=self._listen_voice, daemon=True).start()
        else:
            self.listening = False
            self.voice_btn.config(bg='#2a2a2a')
            self.update_status("Ready", "#00ff88")
    
    def _listen_voice(self):
        """Listen for voice command"""
        try:
            command = self.voice.listen()
            
            if command:
                self.command_queue.put(command)
            else:
                self.add_message("SYSTEM", "⚠️ No voice detected", "error")
        except Exception as e:
            self.add_message("SYSTEM", f"❌ Voice error: {str(e)}", "error")
        finally:
            self.listening = False
            self.root.after(0, lambda: self.voice_btn.config(bg='#2a2a2a'))
            self.root.after(0, lambda: self.update_status("Ready", "#00ff88"))
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display"""
        self.chat_display.config(state='normal')
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Sender
        if sender == "You":
            self.chat_display.insert(tk.END, f"👤 {sender}: ", msg_type)
        elif sender == "JARVIS":
            self.chat_display.insert(tk.END, f"🤖 {sender}: ", msg_type)
        else:
            self.chat_display.insert(tk.END, f"⚙️ {sender}: ", msg_type)
        
        # Message
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def update_status(self, text, color):
        """Update status indicator"""
        self.status_label.config(text=text)
        self.status_indicator.config(fg=color)
    
    def _update_stats_display(self):
        """Update statistics display"""
        try:
            self.stat_skills_loaded.config(text=str(self.stats['total_skills']))
            self.stat_tools_available.config(text=str(self.stats['total_tools']))
            self.stat_queries_processed.config(text=str(self.stats['queries_processed']))
            self.stat_success_rate.config(text=f"{self.stats['success_rate']:.1f}%")
        except:
            pass
    
    def _clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        self.conversation_history.clear()
    
    # Quick action methods
    def _quick_youtube(self):
        self.command_queue.put("open youtube")
    
    def _quick_browser(self):
        self.command_queue.put("open browser")
    
    def _quick_movies(self):
        self.command_queue.put("search movies")
    
    def _quick_search(self):
        query = self.input_entry.get().strip()
        if query and query != "Type your command here...":
            self.command_queue.put(f"search {query}")
        else:
            self.add_message("SYSTEM", "⚠️ Enter search query first", "error")
    
    def _open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#1a1a1a')
        
        # Voice toggle
        voice_var = tk.BooleanVar(value=self.config.get('voice_enabled', True))
        voice_check = tk.Checkbutton(
            settings_window,
            text="Enable Voice Responses",
            variable=voice_var,
            font=('Arial', 12),
            bg='#1a1a1a',
            fg='#ffffff',
            selectcolor='#2a2a2a'
        )
        voice_check.pack(pady=20, padx=20, anchor='w')
        
        # Save button
        def save_settings():
            self.config['voice_enabled'] = voice_var.get()
            self._save_config()
            settings_window.destroy()
            self.add_message("SYSTEM", "✅ Settings saved!", "system")
        
        save_btn = tk.Button(
            settings_window,
            text="Save",
            font=('Arial', 12, 'bold'),
            bg='#00ff88',
            fg='#000000',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=save_settings
        )
        save_btn.pack(pady=20)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernJarvisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

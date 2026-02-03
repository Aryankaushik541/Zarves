#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI - Real-Time Integration with Core Engine
✅ Dynamic skill loading from skill folder
✅ Real-time execution through JarvisEngine
✅ Live status updates
✅ Actual tool execution
"""

import sys
import os
import time
import threading
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
except ImportError as e:
    print(f"Installing tkinter...")
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


class JarvisGUI:
    """Real JARVIS GUI with Engine Integration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - AI Assistant (Real-Time)")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize JARVIS components
        self.registry = None
        self.engine = None
        self.voice = None
        self.listening = False
        
        # Config
        self.config_file = Path.home() / ".jarvis_config.json"
        self.config = self._load_config()
        
        # Stats
        self.stats = {
            'total_skills': 0,
            'total_tools': 0,
            'queries_processed': 0,
            'success_rate': 100.0
        }
        
        # Create GUI first
        self._create_gui()
        
        # Initialize JARVIS in background
        self.update_status("Initializing JARVIS...", "#ff8800")
        threading.Thread(target=self._init_jarvis, daemon=True).start()
    
    def _load_config(self):
        """Load configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")
    
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
            self._populate_skills_panel()
            
            # Welcome message
            welcome = f"✅ JARVIS Ready!\n\n📊 Loaded {self.stats['total_skills']} skills with {self.stats['total_tools']} tools\n\n💬 How can I help you today?"
            self.add_message("JARVIS", welcome, "system")
            
            if self.voice:
                self.voice.speak("JARVIS ready! How can I help you?")
            
            self.update_status("Ready", "#00ff00")
            
        except Exception as e:
            error_msg = f"❌ Initialization failed: {str(e)}\n\n💡 Make sure Ollama is running:\n   ollama serve"
            self.add_message("SYSTEM", error_msg, "error")
            self.update_status("Error", "#ff4444")
    
    def _create_gui(self):
        """Create GUI interface"""
        
        # ============ TOP BAR ============
        top_bar = tk.Frame(self.root, bg='#1a1a1a', height=80)
        top_bar.pack(fill=tk.X, padx=0, pady=0)
        
        # Title
        title = tk.Label(top_bar, text="🤖 JARVIS", font=('Arial', 24, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(side=tk.LEFT, padx=20, pady=20)
        
        subtitle = tk.Label(top_bar, text="Real-Time AI Assistant",
                           font=('Arial', 12), bg='#1a1a1a', fg='#888888')
        subtitle.pack(side=tk.LEFT, padx=0, pady=20)
        
        # Stats display
        self.stats_label = tk.Label(
            top_bar,
            text="Skills: 0 | Tools: 0 | Queries: 0",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#666666'
        )
        self.stats_label.pack(side=tk.LEFT, padx=30, pady=20)
        
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
                                   bg='#1a1a1a', fg='#ff8800')
        self.status_dot.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.status_frame, text="Starting...",
                                     font=('Arial', 12), bg='#1a1a1a', fg='#ff8800')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # ============ MAIN CONTENT ============
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Skills & Tools
        left_panel = tk.Frame(main_frame, bg='#1a1a1a', width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Skills title
        skills_title = tk.Label(left_panel, text="🛠️ Available Skills",
                                font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#ffffff')
        skills_title.pack(pady=15)
        
        # Search box
        search_frame = tk.Frame(left_panel, bg='#1a1a1a')
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._filter_skills)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 10),
            bg='#2a2a2a',
            fg='#ffffff',
            insertbackground='#00ff00',
            relief=tk.FLAT
        )
        search_entry.pack(fill=tk.X, ipady=5)
        
        # Skills list with scrollbar
        canvas_frame = tk.Frame(left_panel, bg='#1a1a1a')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.skills_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        self.skills_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.skills_frame, anchor="nw")
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas_width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Middle panel - Chat
        middle_panel = tk.Frame(main_frame, bg='#1a1a1a')
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chat title
        chat_title = tk.Label(middle_panel, text="💬 Conversation",
                             font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#ffffff')
        chat_title.pack(pady=15)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            middle_panel,
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
        
        # Configure tags
        self.chat_display.tag_config('system', foreground='#00ff00')
        self.chat_display.tag_config('user', foreground='#00aaff')
        self.chat_display.tag_config('error', foreground='#ff4444')
        self.chat_display.tag_config('timestamp', foreground='#666666')
        self.chat_display.tag_config('tool', foreground='#ffaa00')
        
        # Input area
        input_frame = tk.Frame(middle_panel, bg='#1a1a1a')
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
        self.voice_btn = tk.Button(
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
        self.voice_btn.pack(side=tk.LEFT, ipadx=15, ipady=10)
        
        # Right panel - System Info
        right_panel = tk.Frame(main_frame, bg='#1a1a1a', width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # System info title
        info_title = tk.Label(right_panel, text="📊 System Info",
                             font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#ffffff')
        info_title.pack(pady=15)
        
        # Info display
        self.info_display = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#0a0a0a',
            fg='#00ff00',
            relief=tk.FLAT,
            padx=10,
            pady=10,
            height=20
        )
        self.info_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Quick actions
        actions_title = tk.Label(right_panel, text="⚡ Quick Actions",
                                font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='#ffffff')
        actions_title.pack(pady=(10, 5))
        
        quick_actions = [
            ("🌐 Open YouTube", "youtube kholo"),
            ("🔍 Google Search", "google search"),
            ("🎵 Play Music", "gaana bajao"),
            ("📧 Open Gmail", "gmail kholo"),
            ("🖥️ System Info", "system info"),
            ("🔄 Reload Skills", self.reload_skills),
        ]
        
        for text, action in quick_actions:
            if callable(action):
                cmd = action
            else:
                cmd = lambda a=action: self.execute_command(a)
            
            btn = tk.Button(
                right_panel,
                text=text,
                font=('Arial', 9),
                bg='#2a2a2a',
                fg='#ffffff',
                activebackground='#3a3a3a',
                relief=tk.FLAT,
                cursor='hand2',
                anchor='w',
                command=cmd
            )
            btn.pack(fill=tk.X, padx=15, pady=2, ipady=6)
    
    def _update_stats_display(self):
        """Update stats in top bar"""
        stats_text = f"Skills: {self.stats['total_skills']} | Tools: {self.stats['total_tools']} | Queries: {self.stats['queries_processed']}"
        self.stats_label.config(text=stats_text)
        
        # Update info panel
        info_text = f"""╔══════════════════════════╗
║   JARVIS SYSTEM STATUS   ║
╚══════════════════════════╝

📦 Total Skills: {self.stats['total_skills']}
🛠️  Total Tools: {self.stats['total_tools']}
📊 Queries Processed: {self.stats['queries_processed']}
✅ Success Rate: {self.stats['success_rate']:.1f}%

╔══════════════════════════╗
║   LOADED SKILLS          ║
╚══════════════════════════╝

"""
        if self.registry:
            for skill_name in self.registry.list_skills():
                info_text += f"✓ {skill_name}\n"
        
        self.info_display.delete('1.0', tk.END)
        self.info_display.insert('1.0', info_text)
    
    def _populate_skills_panel(self):
        """Populate skills panel with actual skills"""
        # Clear existing
        for widget in self.skills_frame.winfo_children():
            widget.destroy()
        
        if not self.registry:
            return
        
        # Group tools by skill
        skills_dict = {}
        for tool_schema in self.registry.get_tools_schema():
            func_info = tool_schema.get('function', {})
            func_name = func_info.get('name', 'unknown')
            func_desc = func_info.get('description', 'No description')
            
            # Extract skill category from function name
            category = func_name.split('_')[0] if '_' in func_name else 'general'
            
            if category not in skills_dict:
                skills_dict[category] = []
            
            skills_dict[category].append({
                'name': func_name,
                'description': func_desc
            })
        
        # Display by category
        for category, tools in sorted(skills_dict.items()):
            self._create_skill_category(category.title(), tools)
    
    def _create_skill_category(self, title, tools):
        """Create a skill category"""
        # Category frame
        category_frame = tk.Frame(self.skills_frame, bg='#1a1a1a')
        category_frame.pack(fill=tk.X, pady=(10, 5))
        
        # Category label
        label = tk.Label(
            category_frame,
            text=f"📁 {title}",
            font=('Arial', 11, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00',
            anchor='w'
        )
        label.pack(fill=tk.X, padx=15, pady=(5, 8))
        
        # Tools
        for tool in tools[:5]:  # Show max 5 per category
            tool_frame = tk.Frame(category_frame, bg='#2a2a2a')
            tool_frame.pack(fill=tk.X, padx=15, pady=2)
            
            tool_btn = tk.Label(
                tool_frame,
                text=f"  • {tool['name']}",
                font=('Arial', 9),
                bg='#2a2a2a',
                fg='#ffffff',
                anchor='w',
                cursor='hand2'
            )
            tool_btn.pack(fill=tk.X, padx=5, pady=4)
            
            # Tooltip
            tool_btn.bind('<Enter>', lambda e, desc=tool['description']: self._show_tooltip(e, desc))
            tool_btn.bind('<Leave>', self._hide_tooltip)
    
    def _show_tooltip(self, event, text):
        """Show tooltip"""
        # Simple status bar update
        self.update_status(text[:50], "#00aaff")
    
    def _hide_tooltip(self, event):
        """Hide tooltip"""
        if self.engine:
            self.update_status("Ready", "#00ff00")
    
    def _filter_skills(self, *args):
        """Filter skills based on search"""
        search_text = self.search_var.get().lower()
        
        for widget in self.skills_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                # Check if any tool matches
                show = False
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label):
                                text = label.cget('text').lower()
                                if search_text in text:
                                    show = True
                                    break
                
                if show or not search_text:
                    widget.pack(fill=tk.X, pady=(10, 5))
                else:
                    widget.pack_forget()
    
    def reload_skills(self):
        """Reload all skills"""
        self.update_status("Reloading skills...", "#ff8800")
        
        def _reload():
            try:
                if self.registry:
                    skills_dir = Path(__file__).parent.parent / "skill"
                    self.registry.load_skills(str(skills_dir))
                    
                    self.stats['total_skills'] = len(self.registry.list_skills())
                    self.stats['total_tools'] = len(self.registry.list_tools())
                    
                    self._update_stats_display()
                    self._populate_skills_panel()
                    
                    self.add_message("SYSTEM", f"✅ Reloaded {self.stats['total_skills']} skills!", "system")
                    self.update_status("Ready", "#00ff00")
            except Exception as e:
                self.add_message("SYSTEM", f"❌ Reload failed: {e}", "error")
                self.update_status("Error", "#ff4444")
        
        threading.Thread(target=_reload, daemon=True).start()
    
    def open_settings(self):
        """Open settings window"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("⚙️ JARVIS Settings")
        settings_win.geometry("600x400")
        settings_win.configure(bg='#1a1a1a')
        
        title = tk.Label(settings_win, text="⚙️ Settings", font=('Arial', 18, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=20)
        
        # Ollama settings
        ollama_frame = tk.LabelFrame(settings_win, text="Ollama Configuration",
                                     font=('Arial', 12, 'bold'),
                                     bg='#1a1a1a', fg='#ffffff', padx=20, pady=20)
        ollama_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(ollama_frame, text="Host:", bg='#1a1a1a', fg='#ffffff').grid(row=0, column=0, sticky='w', pady=5)
        host_entry = tk.Entry(ollama_frame, width=40, bg='#2a2a2a', fg='#ffffff')
        host_entry.grid(row=0, column=1, pady=5, padx=10)
        host_entry.insert(0, os.environ.get('OLLAMA_HOST', 'http://localhost:11434'))
        
        tk.Label(ollama_frame, text="Model:", bg='#1a1a1a', fg='#ffffff').grid(row=1, column=0, sticky='w', pady=5)
        model_entry = tk.Entry(ollama_frame, width=40, bg='#2a2a2a', fg='#ffffff')
        model_entry.grid(row=1, column=1, pady=5, padx=10)
        model_entry.insert(0, os.environ.get('OLLAMA_MODEL', 'llama3.2'))
        
        def save_settings():
            os.environ['OLLAMA_HOST'] = host_entry.get()
            os.environ['OLLAMA_MODEL'] = model_entry.get()
            messagebox.showinfo("Success", "Settings saved! Restart JARVIS to apply.")
            settings_win.destroy()
        
        save_btn = tk.Button(settings_win, text="💾 Save Settings",
                            font=('Arial', 12, 'bold'),
                            bg='#00ff00', fg='#000000',
                            command=save_settings)
        save_btn.pack(pady=20, ipadx=20, ipady=10)
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        if sender == "JARVIS":
            self.chat_display.insert(tk.END, f"🤖 {sender}: ", 'system')
        elif sender == "SYSTEM":
            self.chat_display.insert(tk.END, f"⚙️ {sender}: ", 'tool')
        else:
            self.chat_display.insert(tk.END, f"👤 {sender}: ", 'user')
        
        self.chat_display.insert(tk.END, f"{message}\n\n", msg_type)
        self.chat_display.see(tk.END)
    
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_label.config(text=status, fg=color)
        self.status_dot.config(fg=color)
    
    def send_message(self):
        """Send message"""
        message = self.input_field.get().strip()
        if message:
            self.input_field.delete(0, tk.END)
            self.add_message("You", message, "user")
            self.execute_command(message)
    
    def voice_input(self):
        """Voice input"""
        if self.listening or not self.voice:
            return
        
        def _listen():
            self.listening = True
            self.update_status("Listening...", "#0088ff")
            self.voice_btn.config(bg='#ff4444', text='🔴 Listening...')
            
            try:
                text = self.voice.listen()
                if text:
                    self.add_message("You", text, "user")
                    self.execute_command(text)
                else:
                    self.add_message("SYSTEM", "No speech detected", "error")
            except Exception as e:
                self.add_message("SYSTEM", f"Voice error: {e}", "error")
            finally:
                self.listening = False
                self.update_status("Ready", "#00ff00")
                self.voice_btn.config(bg='#0088ff', text='🎤 Voice')
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def execute_command(self, query):
        """Execute command through JARVIS engine"""
        self.update_status("Processing...", "#ff8800")
        
        def _execute():
            try:
                if not self.engine:
                    response = "⚠️ JARVIS engine not initialized. Please wait..."
                    self.add_message("JARVIS", response, "error")
                    return
                
                # Process through engine
                response = self.engine.process_query(query)
                
                # Update stats
                self.stats['queries_processed'] += 1
                self._update_stats_display()
                
                # Display response
                self.add_message("JARVIS", response, "system")
                
                # Speak response
                if self.voice:
                    self.voice.speak(response[:200])  # Limit speech length
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.add_message("JARVIS", error_msg, "error")
                self.stats['success_rate'] = (self.stats['success_rate'] * 0.9)  # Decrease success rate
            finally:
                self.update_status("Ready", "#00ff00")
        
        threading.Thread(target=_execute, daemon=True).start()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

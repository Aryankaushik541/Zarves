#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS Simple GUI Launcher
Standalone GUI that definitely works
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Try to import JARVIS components
try:
    from core.registry import SkillRegistry
    from core.engine import JarvisEngine
    from core.voice import speak, listen
    JARVIS_AVAILABLE = True
except Exception as e:
    print(f"⚠️  JARVIS core not available: {e}")
    JARVIS_AVAILABLE = False


class SimpleJarvisGUI:
    """Simple JARVIS GUI that definitely works"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - AI Assistant")
        self.root.geometry("900x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize JARVIS
        self.engine = None
        self.registry = None
        self.listening = False
        
        # Create GUI
        self._create_gui()
        
        # Initialize JARVIS in background
        if JARVIS_AVAILABLE:
            threading.Thread(target=self._init_jarvis, daemon=True).start()
        else:
            self.add_message("SYSTEM", "⚠️  JARVIS core not available. Install dependencies first.", "red")
    
    def _create_gui(self):
        """Create simple GUI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2a2a2a', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 JARVIS - Personal AI Assistant",
            font=('Arial', 18, 'bold'),
            bg='#2a2a2a',
            fg='#00ff00'
        )
        title_label.pack(pady=15)
        
        # Chat area
        chat_frame = tk.Frame(self.root, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#0a0a0a',
            fg='#ffffff',
            insertbackground='white',
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = tk.Frame(self.root, bg='#2a2a2a')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_box = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='#3a3a3a',
            fg='white',
            insertbackground='white'
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_box.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 11, 'bold'),
            bg='#00aa00',
            fg='white',
            command=self.send_message,
            width=10
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        voice_btn = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=('Arial', 11, 'bold'),
            bg='#0066cc',
            fg='white',
            command=self.voice_input,
            width=10
        )
        voice_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="● Initializing...",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#ffaa00',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 5))
    
    def _init_jarvis(self):
        """Initialize JARVIS engine"""
        try:
            self.add_message("SYSTEM", "📦 Loading skills...", "#00aaff")
            self.registry = SkillRegistry()
            
            self.add_message("SYSTEM", "🧠 Initializing AI engine...", "#00aaff")
            self.engine = JarvisEngine(self.registry)
            
            self.add_message("SYSTEM", "🎤 Voice assistant ready!", "#00aaff")
            
            # Success message
            skill_count = len(self.registry.skills)
            tool_count = sum(len(s.get('tools', [])) for s in self.registry.skills.values())
            
            self.add_message(
                "JARVIS",
                f"✅ JARVIS Ready!\n\n📊 Loaded {skill_count} skills with {tool_count} tools\n\n💬 How can I help you today?",
                "#00ff00"
            )
            
            self.update_status("● Ready", "#00ff00")
            
        except Exception as e:
            self.add_message("SYSTEM", f"❌ Error initializing JARVIS: {e}", "red")
            self.update_status("● Error", "red")
    
    def add_message(self, sender, message, color="#ffffff"):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        
        # Add message
        if sender == "SYSTEM":
            prefix = f"{timestamp} ⚙️ SYSTEM: "
        elif sender == "JARVIS":
            prefix = f"{timestamp} 🤖 JARVIS: "
        else:
            prefix = f"{timestamp} 👤 You: "
        
        self.chat_display.insert(tk.END, prefix, "prefix")
        self.chat_display.insert(tk.END, message + "\n\n", "message")
        
        # Apply colors
        self.chat_display.tag_config("prefix", foreground=color, font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config("message", foreground=color)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, text, color):
        """Update status bar"""
        self.status_label.config(text=text, fg=color)
    
    def send_message(self):
        """Send text message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, tk.END)
        self.add_message("You", message, "#ffffff")
        
        # Process with JARVIS
        if self.engine:
            self.update_status("● Processing...", "#ffaa00")
            threading.Thread(target=self._process_query, args=(message,), daemon=True).start()
        else:
            self.add_message("JARVIS", "⚠️  JARVIS engine not ready yet. Please wait...", "red")
    
    def voice_input(self):
        """Voice input"""
        if self.listening:
            return
        
        self.listening = True
        self.update_status("● Listening...", "#ff00ff")
        
        def _listen():
            try:
                command = listen()
                if command and command != "none":
                    self.add_message("You", command, "#ffffff")
                    if self.engine:
                        self._process_query(command)
                else:
                    self.add_message("SYSTEM", "No voice detected", "#ffaa00")
            except Exception as e:
                self.add_message("SYSTEM", f"Voice error: {e}", "red")
            finally:
                self.listening = False
                self.update_status("● Ready", "#00ff00")
        
        threading.Thread(target=_listen, daemon=True).start()
    
    def _process_query(self, query):
        """Process query with JARVIS"""
        try:
            response = self.engine.process_query(query)
            self.add_message("JARVIS", response, "#00ff00")
            
            # Speak response (limit length)
            try:
                speak(response[:200])
            except:
                pass
                
        except Exception as e:
            self.add_message("JARVIS", f"Error: {e}", "red")
        finally:
            self.update_status("● Ready", "#00ff00")


def main():
    """Main entry point"""
    print("\n🚀 Launching JARVIS GUI...\n")
    
    root = tk.Tk()
    app = SimpleJarvisGUI(root)
    
    print("✅ GUI window opened!")
    print("💡 If you don't see the window, check your taskbar\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()

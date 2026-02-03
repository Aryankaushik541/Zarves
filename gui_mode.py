#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI Mode - Modern Chat Interface
Beautiful graphical interface with voice controls and visual feedback
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import sys
import os

# Suppress warnings
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'
import warnings
warnings.filterwarnings("ignore")

from core.registry import SkillRegistry
from core.engine import JarvisEngine
from core.voice import speak, listen


class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - Your Personal AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")
        
        # Initialize engine
        self.registry = SkillRegistry()
        self.registry.load_skills("skill")
        self.engine = JarvisEngine(self.registry)
        
        # Voice mode state
        self.voice_mode = False
        self.listening = False
        
        # Create GUI
        self.create_widgets()
        
        # Welcome message
        self.add_message("JARVIS", "Hello! I'm JARVIS, your personal AI assistant. How can I help you today?", "assistant")
        speak("Hello! I'm JARVIS. How can I help you today?")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # ============================================================
        # HEADER
        # ============================================================
        header_frame = tk.Frame(self.root, bg="#2d2d2d", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🤖 JARVIS",
            font=("Segoe UI", 24, "bold"),
            bg="#2d2d2d",
            fg="#00d4ff"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Your Personal AI Assistant",
            font=("Segoe UI", 10),
            bg="#2d2d2d",
            fg="#888888"
        )
        subtitle_label.place(x=120, y=45)
        
        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="● Ready",
            font=("Segoe UI", 10, "bold"),
            bg="#2d2d2d",
            fg="#00ff00"
        )
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # ============================================================
        # CHAT AREA
        # ============================================================
        chat_frame = tk.Frame(self.root, bg="#1e1e1e")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            padx=15,
            pady=15,
            spacing3=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for styling
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#00ff88", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#ffaa00", font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_config("message", foreground="#ffffff", font=("Segoe UI", 11))
        
        # ============================================================
        # INPUT AREA
        # ============================================================
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            bd=0
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        self.input_field.focus()
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg="#00d4ff",
            fg="#1e1e1e",
            activebackground="#00a8cc",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Voice button
        self.voice_button = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3d3d3d",
            activeforeground="#00d4ff",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.toggle_voice_mode
        )
        self.voice_button.pack(side=tk.LEFT)
        
        # ============================================================
        # FOOTER
        # ============================================================
        footer_frame = tk.Frame(self.root, bg="#2d2d2d", height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        # Skills count
        skills_count = len(self.registry.list_skills())
        skills_label = tk.Label(
            footer_frame,
            text=f"📚 {skills_count} Skills Loaded",
            font=("Segoe UI", 9),
            bg="#2d2d2d",
            fg="#888888"
        )
        skills_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Mode indicator
        self.mode_label = tk.Label(
            footer_frame,
            text="⌨️  Text Mode",
            font=("Segoe UI", 9),
            bg="#2d2d2d",
            fg="#888888"
        )
        self.mode_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def add_message(self, sender, message, tag):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add sender
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send a text message"""
        message = self.input_field.get().strip()
        
        if not message:
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Check for exit commands
        if message.lower() in ['quit', 'exit', 'bye', 'goodbye', 'alvida']:
            self.add_message("You", message, "user")
            self.add_message("JARVIS", "Goodbye! Have a great day! 👋", "assistant")
            speak("Goodbye! Have a great day!")
            self.root.after(2000, self.root.destroy)
            return
        
        # Add user message
        self.add_message("You", message, "user")
        
        # Update status
        self.status_label.config(text="● Processing...", fg="#ffaa00")
        
        # Process in background thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process message in background"""
        try:
            # Get response from engine
            response = self.engine.process_query(message)
            
            # Update GUI in main thread
            self.root.after(0, self.add_message, "JARVIS", response, "assistant")
            self.root.after(0, self.status_label.config, {"text": "● Ready", "fg": "#00ff00"})
            
            # Speak response
            speak(response)
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, self.add_message, "JARVIS", error_msg, "assistant")
            self.root.after(0, self.status_label.config, {"text": "● Error", "fg": "#ff0000"})
            speak("Sorry, I encountered an error. Please try again.")
    
    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        if not self.voice_mode:
            # Enable voice mode
            self.voice_mode = True
            self.voice_button.config(bg="#00d4ff", fg="#1e1e1e", text="🎤 Listening...")
            self.mode_label.config(text="🎤 Voice Mode")
            self.input_field.config(state=tk.DISABLED)
            self.send_button.config(state=tk.DISABLED)
            
            # Start listening in background
            threading.Thread(target=self.voice_listen_loop, daemon=True).start()
        else:
            # Disable voice mode
            self.voice_mode = False
            self.voice_button.config(bg="#2d2d2d", fg="#ffffff", text="🎤 Voice")
            self.mode_label.config(text="⌨️  Text Mode")
            self.input_field.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.status_label.config(text="● Ready", fg="#00ff00")
    
    def voice_listen_loop(self):
        """Continuous voice listening loop"""
        self.add_message("JARVIS", "Voice mode activated! Say 'Jarvis' followed by your command. Say 'stop listening' to exit.", "system")
        speak("Voice mode activated. I'm listening.")
        
        while self.voice_mode:
            try:
                # Update status
                self.root.after(0, self.status_label.config, {"text": "● Listening...", "fg": "#00d4ff"})
                
                # Listen for command
                command = listen()
                
                if command == "none":
                    continue
                
                # Check for exit
                if command.lower() in ['stop listening', 'exit voice mode', 'band karo']:
                    self.root.after(0, self.toggle_voice_mode)
                    break
                
                # Add user message
                self.root.after(0, self.add_message, "You", command, "user")
                
                # Update status
                self.root.after(0, self.status_label.config, {"text": "● Processing...", "fg": "#ffaa00"})
                
                # Process command
                response = self.engine.process_query(command)
                
                # Add response
                self.root.after(0, self.add_message, "JARVIS", response, "assistant")
                
                # Speak response
                speak(response)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.root.after(0, self.add_message, "JARVIS", error_msg, "system")
                speak("Sorry, I encountered an error.")
        
        # Reset status
        self.root.after(0, self.status_label.config, {"text": "● Ready", "fg": "#00ff00"})


def main():
    """Main entry point for GUI mode"""
    print("\n" + "="*70)
    print("🤖 JARVIS GUI Mode")
    print("="*70)
    print()
    print("🎨 Launching graphical interface...")
    print()
    
    # Create GUI
    root = tk.Tk()
    app = JarvisGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    print("✅ GUI launched successfully!")
    print()
    print("💡 Features:")
    print("   • Type messages in the input field")
    print("   • Click 'Send' or press Enter")
    print("   • Click '🎤 Voice' for voice mode")
    print("   • JARVIS speaks all responses")
    print()
    print("="*70)
    print()
    
    # Run GUI
    root.mainloop()


if __name__ == "__main__":
    main()

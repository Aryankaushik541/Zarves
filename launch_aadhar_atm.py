#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM GUI Launcher
Voice-first interface for automated Aadhar ATM withdrawal
"""

import importlib.util
import re
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

SKILL_AVAILABLE = False
VOICE_AVAILABLE = False
SR_AVAILABLE = False

if importlib.util.find_spec("skill.aadhar_atm_skill"):
    from skill.aadhar_atm_skill import AadharATMSkill
    SKILL_AVAILABLE = True

if importlib.util.find_spec("core.voice"):
    from core.voice import speak
    VOICE_AVAILABLE = True

if importlib.util.find_spec("speech_recognition"):
    import speech_recognition as sr
    SR_AVAILABLE = True


class AadharATMGUI:
    """Voice-first GUI for Aadhar ATM automation"""

    def __init__(self, root):
        self.root = root
        self.root.title("🏧 Aadhar ATM - Auto Withdrawal")
        self.root.geometry("560x520")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        self.skill = AadharATMSkill() if SKILL_AVAILABLE else None
        self.aadhar_number = None
        self.amount = None
        self.listening = False

        self._create_gui()

    def _create_gui(self):
        header = tk.Frame(self.root, bg="#161b22", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🏧 Aadhar ATM Agent",
            font=("Arial", 20, "bold"),
            bg="#161b22",
            fg="#58a6ff",
        )
        title.pack(pady=25)

        content = tk.Frame(self.root, bg="#0d1117")
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        info = tk.Label(
            content,
            text="AI agent screen dekh ke khud se form fill karega.\n"
                 "Aadhar aur amount voice se bolein.",
            font=("Arial", 10),
            bg="#0d1117",
            fg="#8b949e",
            justify=tk.CENTER,
        )
        info.pack(pady=(0, 15))

        self.aadhar_label = tk.Label(
            content,
            text="Aadhar: —",
            font=("Arial", 14, "bold"),
            bg="#0d1117",
            fg="#c9d1d9",
        )
        self.aadhar_label.pack(pady=5)

        self.amount_label = tk.Label(
            content,
            text="Amount: —",
            font=("Arial", 14, "bold"),
            bg="#0d1117",
            fg="#c9d1d9",
        )
        self.amount_label.pack(pady=5)

        voice_frame = tk.Frame(content, bg="#0d1117")
        voice_frame.pack(fill=tk.X, pady=10)

        self.aadhar_btn = tk.Button(
            voice_frame,
            text="🎤 Aadhar बोलें",
            font=("Arial", 11, "bold"),
            bg="#21262d",
            fg="#c9d1d9",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._listen_aadhar,
        )
        self.aadhar_btn.pack(side=tk.LEFT, padx=5)

        self.amount_btn = tk.Button(
            voice_frame,
            text="🎤 Amount बोलें",
            font=("Arial", 11, "bold"),
            bg="#21262d",
            fg="#c9d1d9",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._listen_amount,
        )
        self.amount_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            content,
            text="Ready.",
            font=("Arial", 10),
            bg="#0d1117",
            fg="#f0883e",
            wraplength=440,
        )
        self.status_label.pack(pady=10)

        self.start_btn = tk.Button(
            content,
            text="🚀 Start Auto Withdrawal",
            font=("Arial", 14, "bold"),
            bg="#238636",
            fg="white",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self._start_withdrawal,
        )
        self.start_btn.pack(pady=10)

        instructions = tk.Label(
            content,
            text="📝 Instructions:\n"
                 "1. ATM screen khol lo\n"
                 "2. Aadhar aur amount voice se bolo\n"
                 "3. Start button dabao\n"
                 "4. AI agent khud se sab kar dega",
            font=("Arial", 9),
            bg="#0d1117",
            fg="#8b949e",
            justify=tk.LEFT,
        )
        instructions.pack(pady=(20, 0))

        if not SKILL_AVAILABLE:
            self._set_status("⚠️ Skill not loaded. Install dependencies first.", "#f85149")
            self.start_btn.config(state="disabled", bg="#6e7681")

    def _set_status(self, text, color="#f0883e"):
        self.status_label.config(text=text, fg=color)

    def _extract_digits(self, text):
        digits = re.findall(r"\d+", text)
        return "".join(digits)

    def _listen_for_numbers(self, prompt, expected_length=None):
        if not SR_AVAILABLE:
            self._set_status("❌ SpeechRecognition missing. Install SpeechRecognition + pyaudio.", "#f85149")
            return None
        if self.listening:
            return None

        self.listening = True
        self._set_status(prompt, "#a371f7")
        if VOICE_AVAILABLE:
            speak(prompt)

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError:
            text = ""

        self.listening = False

        digits = self._extract_digits(text)
        if expected_length and len(digits) != expected_length:
            return None
        return digits if digits else None

    def _listen_aadhar(self):
        def _task():
            aadhar = self._listen_for_numbers("Aadhar number bolo (12 digits)", expected_length=12)
            if aadhar:
                self.aadhar_number = aadhar
                masked = f"{aadhar[:4]}****{aadhar[-4:]}"
                self.aadhar_label.config(text=f"Aadhar: {masked}")
                self._set_status("✅ Aadhar captured.", "#3fb950")
            else:
                self._set_status("⚠️ Aadhar samajh nahi aaya. Dobara bolein.", "#f0883e")
        threading.Thread(target=_task, daemon=True).start()

    def _listen_amount(self):
        def _task():
            amount = self._listen_for_numbers("Kitna paisa chahiye?", expected_length=None)
            if amount:
                self.amount = amount
                self.amount_label.config(text=f"Amount: ₹{amount}")
                self._set_status("✅ Amount captured.", "#3fb950")
            else:
                self._set_status("⚠️ Amount samajh nahi aaya. Dobara bolein.", "#f0883e")
        threading.Thread(target=_task, daemon=True).start()

    def _start_withdrawal(self):
        if not self.aadhar_number:
            self._set_status("❌ Aadhar missing. Voice se bolein.", "#f85149")
            return
        if not self.amount:
            self._set_status("❌ Amount missing. Voice se bolein.", "#f85149")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            f"Aadhar: {self.aadhar_number[:4]}****{self.aadhar_number[-4:]}\n"
            f"Amount: ₹{self.amount}\n\n"
            "AI agent ab screen dekh ke khud se form fill karega.\n"
            "Continue?",
        )
        if not confirm:
            return

        self.start_btn.config(state="disabled", bg="#6e7681")
        self._set_status("🔄 Processing... Screen dekh raha hoon...", "#f0883e")
        self.root.update()

        def _run():
            try:
                result = self.skill.aadhar_withdraw_money(self.aadhar_number, self.amount)
                messagebox.showinfo("Result", result)
                if "✅" in result:
                    self._set_status(f"✅ Success! ₹{self.amount} nikla hai!", "#3fb950")
                else:
                    self._set_status("⚠️ Check result message", "#f0883e")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
                self._set_status(f"❌ Error: {str(e)[:50]}", "#f85149")
            finally:
                self.start_btn.config(state="normal", bg="#238636")

        threading.Thread(target=_run, daemon=True).start()


def main():
    print("\n" + "=" * 60)
    print("🏧 Aadhar ATM - Auto Withdrawal Agent")
    print("=" * 60)
    print()

    if not SKILL_AVAILABLE:
        print("❌ Aadhar skill not available. Install dependencies.")
        return

    root = tk.Tk()
    app = AadharATMGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

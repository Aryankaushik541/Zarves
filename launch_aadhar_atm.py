#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM GUI Launcher
Simple interface for automated Aadhar ATM withdrawal
"""

import sys
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from skill.aadhar_atm_skill import AadharATMSkill
    SKILL_AVAILABLE = True
except ImportError:
    SKILL_AVAILABLE = False


class AadharATMGUI:
    """Simple GUI for Aadhar ATM automation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏧 Aadhar ATM - Auto Withdrawal")
        self.root.geometry("500x400")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)
        
        # Initialize skill
        if SKILL_AVAILABLE:
            self.skill = AadharATMSkill()
        else:
            self.skill = None
        
        self._create_gui()
    
    def _create_gui(self):
        """Create GUI interface"""
        
        # Header
        header = tk.Frame(self.root, bg='#161b22', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🏧 Aadhar ATM Agent",
            font=('Arial', 20, 'bold'),
            bg='#161b22',
            fg='#58a6ff'
        )
        title.pack(pady=25)
        
        # Main content
        content = tk.Frame(self.root, bg='#0d1117')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Info label
        info = tk.Label(
            content,
            text="AI agent jo screen dekh ke khud se form fill karega",
            font=('Arial', 10),
            bg='#0d1117',
            fg='#8b949e'
        )
        info.pack(pady=(0, 20))
        
        # Aadhar number input
        aadhar_frame = tk.Frame(content, bg='#0d1117')
        aadhar_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            aadhar_frame,
            text="Aadhar Number:",
            font=('Arial', 12, 'bold'),
            bg='#0d1117',
            fg='#c9d1d9'
        ).pack(anchor='w', pady=(0, 5))
        
        self.aadhar_entry = tk.Entry(
            aadhar_frame,
            font=('Arial', 14),
            bg='#161b22',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            bd=2,
            relief=tk.FLAT
        )
        self.aadhar_entry.pack(fill=tk.X, ipady=8)
        self.aadhar_entry.insert(0, "")
        
        # Amount input
        amount_frame = tk.Frame(content, bg='#0d1117')
        amount_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            amount_frame,
            text="Kitna paisa chahiye? (₹):",
            font=('Arial', 12, 'bold'),
            bg='#0d1117',
            fg='#c9d1d9'
        ).pack(anchor='w', pady=(0, 5))
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=('Arial', 14),
            bg='#161b22',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            bd=2,
            relief=tk.FLAT
        )
        self.amount_entry.pack(fill=tk.X, ipady=8)
        self.amount_entry.insert(0, "")
        
        # Quick amount buttons
        quick_frame = tk.Frame(content, bg='#0d1117')
        quick_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            quick_frame,
            text="Quick Select:",
            font=('Arial', 10),
            bg='#0d1117',
            fg='#8b949e'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        for amount in ['500', '1000', '2000', '5000']:
            btn = tk.Button(
                quick_frame,
                text=f"₹{amount}",
                font=('Arial', 10),
                bg='#21262d',
                fg='#c9d1d9',
                bd=0,
                padx=15,
                pady=5,
                cursor='hand2',
                command=lambda a=amount: self.amount_entry.delete(0, tk.END) or self.amount_entry.insert(0, a)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Status label
        self.status_label = tk.Label(
            content,
            text="",
            font=('Arial', 10),
            bg='#0d1117',
            fg='#f0883e',
            wraplength=400
        )
        self.status_label.pack(pady=15)
        
        # Start button
        self.start_btn = tk.Button(
            content,
            text="🚀 Start Auto Withdrawal",
            font=('Arial', 14, 'bold'),
            bg='#238636',
            fg='white',
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2',
            command=self._start_withdrawal
        )
        self.start_btn.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            content,
            text="📝 Instructions:\n"
                 "1. ATM screen khol lo\n"
                 "2. Aadhar number aur amount enter karo\n"
                 "3. 'Start' button dabao\n"
                 "4. AI agent khud se sab kar dega!",
            font=('Arial', 9),
            bg='#0d1117',
            fg='#8b949e',
            justify=tk.LEFT
        )
        instructions.pack(pady=(20, 0))
        
        # Check if skill is available
        if not SKILL_AVAILABLE:
            self.status_label.config(
                text="⚠️ Skill not loaded. Install dependencies first.",
                fg='#f85149'
            )
            self.start_btn.config(state='disabled', bg='#6e7681')
    
    def _start_withdrawal(self):
        """Start automated withdrawal"""
        
        # Get inputs
        aadhar = self.aadhar_entry.get().strip().replace(" ", "")
        amount = self.amount_entry.get().strip()
        
        # Validate
        if not aadhar:
            messagebox.showerror("Error", "Aadhar number enter karo!")
            return
        
        if len(aadhar) != 12 or not aadhar.isdigit():
            messagebox.showerror("Error", "Aadhar number 12 digits ka hona chahiye!")
            return
        
        if not amount:
            messagebox.showerror("Error", "Amount enter karo!")
            return
        
        if not amount.isdigit():
            messagebox.showerror("Error", "Amount sirf numbers me hona chahiye!")
            return
        
        # Confirm
        confirm = messagebox.askyesno(
            "Confirm",
            f"Aadhar: {aadhar[:4]}****{aadhar[-4:]}\n"
            f"Amount: ₹{amount}\n\n"
            f"AI agent ab screen dekh ke khud se form fill karega.\n"
            f"Continue?"
        )
        
        if not confirm:
            return
        
        # Disable button
        self.start_btn.config(state='disabled', bg='#6e7681')
        self.status_label.config(
            text="🔄 Processing... Screen dekh raha hoon...",
            fg='#f0883e'
        )
        self.root.update()
        
        # Execute withdrawal
        try:
            if self.skill:
                result = self.skill.aadhar_withdraw_money(aadhar, amount)
                
                # Show result
                messagebox.showinfo("Result", result)
                
                if "✅" in result:
                    self.status_label.config(
                        text=f"✅ Success! ₹{amount} nikla hai!",
                        fg='#3fb950'
                    )
                else:
                    self.status_label.config(
                        text="⚠️ Check result message",
                        fg='#f0883e'
                    )
            else:
                messagebox.showerror("Error", "Skill not available!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.status_label.config(
                text=f"❌ Error: {str(e)[:50]}",
                fg='#f85149'
            )
        
        finally:
            # Re-enable button
            self.start_btn.config(state='normal', bg='#238636')


def main():
    """Main entry point"""
    
    print("\n" + "="*60)
    print("🏧 Aadhar ATM - Auto Withdrawal Agent")
    print("="*60)
    print()
    print("📦 Checking dependencies...")
    
    # Check dependencies
    missing = []
    try:
        import pyautogui
    except ImportError:
        missing.append("pyautogui")
    
    try:
        import pytesseract
    except ImportError:
        missing.append("pytesseract")
    
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    
    try:
        from PIL import Image
    except ImportError:
        missing.append("pillow")
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print()
        print("📥 Install with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        
        if 'pytesseract' in missing:
            print("⚠️  Also install Tesseract OCR:")
            print("   Windows: https://github.com/UB-Mannheim/tesseract/wiki")
            print("   Linux: sudo apt-get install tesseract-ocr")
            print("   Mac: brew install tesseract")
        print()
        
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return
    else:
        print("✅ All dependencies available!")
    
    print()
    print("🚀 Launching GUI...")
    print()
    
    # Launch GUI
    root = tk.Tk()
    app = AadharATMGUI(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

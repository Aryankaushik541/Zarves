#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM Automation Skill for JARVIS
AI Agent that reads screen and fills forms automatically
"""

import sys
import time
import re
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional, Tuple, Iterable

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

pyautogui = None
pytesseract = None
cv2 = None
np = None
ImageGrab = None
ollama = None
requests = None

if importlib.util.find_spec("pyautogui"):
    import pyautogui
if importlib.util.find_spec("pytesseract"):
    import pytesseract
if importlib.util.find_spec("PIL"):
    from PIL import Image, ImageGrab
if importlib.util.find_spec("cv2"):
    import cv2
if importlib.util.find_spec("numpy"):
    import numpy as np
if importlib.util.find_spec("ollama"):
    import ollama
if importlib.util.find_spec("requests"):
    import requests

from core.skill import Skill


class AadharATMSkill(Skill):
    """AI Agent for Aadhar ATM automation with screen reading"""
    
    def __init__(self):
        self.aadhar_number = None
        self.withdrawal_amount = None
        self._ollama_ready = None
        
        # Configure pyautogui
        if pyautogui:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
    
    @property
    def name(self) -> str:
        """The name of the skill."""
        return "Aadhar ATM Agent"
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return the list of tool schemas provided by this skill."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "aadhar_withdraw_money",
                    "description": "Automatically fill Aadhar form and withdraw money by reading screen",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "aadhar_number": {
                                "type": "string",
                                "description": "12-digit Aadhar number (e.g., '123456789012')"
                            },
                            "amount": {
                                "type": "string",
                                "description": "Amount to withdraw (e.g., '500', '1000', '2000')"
                            }
                        },
                        "required": ["aadhar_number", "amount"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_screen_text",
                    "description": "Read and extract text from current screen using OCR",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "Screen region to read: 'full', 'top', 'center', 'bottom'"
                            }
                        }
                    }
                }
            }
        ]
    
    def get_functions(self) -> Dict[str, Callable]:
        """Return a dictionary mapping function names to the actual callables."""
        return {
            "aadhar_withdraw_money": self.aadhar_withdraw_money,
            "read_screen_text": self.read_screen_text
        }

    def _ollama_available(self) -> bool:
        """Check if Ollama server is available for AI screen parsing."""
        if self._ollama_ready is not None:
            return self._ollama_ready
        if not ollama:
            self._ollama_ready = False
            return False
        if not requests:
            self._ollama_ready = False
            return False
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            self._ollama_ready = response.status_code == 200
        except Exception:
            self._ollama_ready = False
        return self._ollama_ready

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize OCR text for matching."""
        return re.sub(r"[^a-z0-9]", "", text.lower())

    def _get_ocr_data(self):
        """Capture screen and return OCR data with bounding boxes."""
        if not pytesseract or not cv2 or not np:
            return None, []
        screenshot = self.capture_screen()
        if not screenshot:
            return None, []
        screenshot_np = np.array(screenshot)
        gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        entries = []
        for i, text in enumerate(data.get("text", [])):
            text = text.strip()
            if not text:
                continue
            entries.append({
                "text": text,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
            })
        return screenshot, entries

    def _ai_pick_label(self, entries: List[Dict[str, Any]], target: str, candidates: Iterable[str]) -> Optional[str]:
        """Use Ollama (if available) to select the best label from OCR text."""
        if not self._ollama_available():
            return None
        try:
            unique_texts = list({entry["text"] for entry in entries})
            prompt = (
                "You are helping an automation agent. "
                "From the OCR words below, pick the BEST label for the target field. "
                "Return only the exact label text.\n\n"
                f"Target: {target}\n"
                f"Candidates: {', '.join(candidates)}\n"
                f"OCR Words: {', '.join(unique_texts)}"
            )
            response = ollama.generate(model="llama3.2", prompt=prompt)
            label = (response.get("response") or "").strip().splitlines()[0]
            return label or None
        except Exception:
            return None

    def _find_text_position(self, search_text: str, entries: Optional[List[Dict[str, Any]]] = None) -> Optional[Tuple[int, int]]:
        """Find text on screen and return its center position."""
        if not entries:
            _, entries = self._get_ocr_data()
        if not entries:
            return None
        search_norm = self._normalize_text(search_text)
        for entry in entries:
            if search_norm in self._normalize_text(entry["text"]):
                x = entry["left"] + entry["width"] // 2
                y = entry["top"] + entry["height"] // 2
                return (x, y)
        return None

    def _find_input_field(self, label_texts: Iterable[str], entries: Optional[List[Dict[str, Any]]] = None):
        """Find input field near any of the label texts."""
        if isinstance(label_texts, str):
            label_texts = [label_texts]
        if not entries:
            _, entries = self._get_ocr_data()
        for label in label_texts:
            label_pos = self._find_text_position(label, entries)
            if label_pos:
                x, y = label_pos
                return (x + 200, y)
        return None

    def _wait_for_screen_text(self, phrases: Iterable[str], timeout: int = 30, poll_interval: float = 2.0) -> Optional[str]:
        """Wait until any phrase appears on screen."""
        end_time = time.time() + timeout
        phrases_norm = [self._normalize_text(p) for p in phrases]
        while time.time() < end_time:
            _, entries = self._get_ocr_data()
            text_blob = " ".join(entry["text"] for entry in entries)
            text_norm = self._normalize_text(text_blob)
            for phrase, phrase_norm in zip(phrases, phrases_norm):
                if phrase_norm in text_norm:
                    return phrase
            time.sleep(poll_interval)
        return None
    
    def capture_screen(self, region=None):
        """Capture screenshot of screen or region"""
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def read_screen_text(self, region="full"):
        """Read text from screen using OCR"""
        if not pytesseract:
            return "❌ OCR not available. Install: pip install pytesseract pillow"
        
        try:
            # Capture screen
            if region == "full":
                screenshot = self.capture_screen()
            else:
                # Define regions
                screen_width, screen_height = pyautogui.size()
                regions = {
                    "top": (0, 0, screen_width, screen_height // 3),
                    "center": (0, screen_height // 3, screen_width, 2 * screen_height // 3),
                    "bottom": (0, 2 * screen_height // 3, screen_width, screen_height)
                }
                screenshot = self.capture_screen(regions.get(region))
            
            if not screenshot:
                return "❌ Failed to capture screen"
            
            # Convert to grayscale for better OCR
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding for better text recognition
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Extract text
            text = pytesseract.image_to_string(thresh)
            
            return f"📖 Screen Text:\n\n{text}"
            
        except Exception as e:
            return f"❌ OCR Error: {str(e)}"
    
    def find_text_on_screen(self, search_text, entries=None):
        """Find text on screen and return its position"""
        try:
            return self._find_text_position(search_text, entries)
        except Exception as e:
            print(f"Text search error: {e}")
            return None
    
    def find_input_field(self, label_text):
        """Find input field near a label"""
        try:
            return self._find_input_field([label_text])
        except Exception as e:
            print(f"Input field search error: {e}")
            return None
    
    def click_button(self, button_text):
        """Find and click a button by text"""
        try:
            button_pos = self.find_text_on_screen(button_text)
            if button_pos:
                pyautogui.click(button_pos[0], button_pos[1])
                return True
            return False
        except Exception as e:
            print(f"Button click error: {e}")
            return False
    
    def type_in_field(self, field_position, text):
        """Click field and type text"""
        try:
            # Click on field
            pyautogui.click(field_position[0], field_position[1])
            time.sleep(0.3)
            
            # Clear existing text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # Type new text
            pyautogui.write(text, interval=0.1)
            time.sleep(0.2)
            
            return True
        except Exception as e:
            print(f"Typing error: {e}")
            return False
    
    def extract_amount_from_screen(self):
        """Extract withdrawal amount from success message"""
        try:
            screenshot = self.capture_screen()
            if not screenshot:
                return None
            
            # Convert and OCR
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            
            # Look for amount patterns
            # Common patterns: "Rs. 500", "₹500", "Amount: 500", etc.
            patterns = [
                r'Rs\.?\s*(\d+)',
                r'₹\s*(\d+)',
                r'Amount:?\s*(\d+)',
                r'Withdrawn:?\s*(\d+)',
                r'(\d+)\s*rupees',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            print(f"Amount extraction error: {e}")
            return None

    def extract_balance_from_screen(self):
        """Extract remaining balance from screen text"""
        try:
            screenshot = self.capture_screen()
            if not screenshot:
                return None
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            patterns = [
                r'Balance:?\s*(\d+)',
                r'Bal(?:ance)?\s*Rs\.?\s*(\d+)',
                r'Remaining:?\s*(\d+)',
                r'Available:?\s*(\d+)',
                r'₹\s*(\d+)\s*balance',
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            print(f"Balance extraction error: {e}")
            return None
    
    def aadhar_withdraw_money(self, aadhar_number: str, amount: str) -> str:
        """
        Automatically fill Aadhar ATM form and withdraw money
        Reads screen, fills form, clicks buttons, and confirms withdrawal
        """
        
        if not pyautogui or not pytesseract or not cv2 or not np:
            return """❌ Required libraries not installed!

Install with:
pip install pyautogui pytesseract pillow opencv-python

Also install Tesseract OCR:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Linux: sudo apt-get install tesseract-ocr
- Mac: brew install tesseract
"""
        
        # Validate inputs
        if not re.match(r'^\d{12}$', aadhar_number):
            return "❌ Invalid Aadhar number! Must be 12 digits."
        
        if not amount.isdigit():
            return "❌ Invalid amount! Must be numeric."
        
        self.aadhar_number = aadhar_number
        self.withdrawal_amount = amount
        
        try:
            steps_log = []
            
            # Step 1: Wait for screen to be ready
            steps_log.append("⏳ Waiting for ATM screen...")
            time.sleep(1)

            _, ocr_entries = self._get_ocr_data()
            aadhar_labels = ["Aadhar", "Aadhaar", "UID", "Aadhaar Number", "Card Number", "Number"]
            amount_labels = ["Amount", "Withdraw", "Enter Amount", "Money", "Rs", "₹"]
            submit_labels = ["Submit", "OK", "Confirm", "Proceed", "Next"]
            print_labels = ["Print", "Receipt", "Print Receipt"]
            fingerprint_phrases = [
                "fingerprint", "finger print", "place finger", "scan finger",
                "biometric", "morpho", "thumb", "finger"
            ]

            aadhar_label = self._ai_pick_label(ocr_entries, "aadhar number", aadhar_labels) or aadhar_labels[0]
            amount_label = self._ai_pick_label(ocr_entries, "withdrawal amount", amount_labels) or amount_labels[0]
            submit_label = self._ai_pick_label(ocr_entries, "submit button", submit_labels) or submit_labels[0]
            print_label = self._ai_pick_label(ocr_entries, "print button", print_labels) or print_labels[0]
            
            # Step 2: Find and fill Aadhar number field
            steps_log.append("🔍 Looking for Aadhar number field...")
            aadhar_field = self._find_input_field([aadhar_label] + aadhar_labels, ocr_entries)
            
            if aadhar_field:
                steps_log.append(f"✅ Found Aadhar field at {aadhar_field}")
                steps_log.append(f"⌨️  Typing Aadhar number: {aadhar_number}")
                self.type_in_field(aadhar_field, aadhar_number)
                time.sleep(0.5)
            else:
                steps_log.append("⚠️  Aadhar field not found, trying manual position...")
                # Fallback: click center-left area where Aadhar field usually is
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width // 2, screen_height // 2 - 50)
                time.sleep(0.3)
                pyautogui.write(aadhar_number, interval=0.1)
            
            # Step 3: Find and fill amount field
            steps_log.append("🔍 Looking for amount field...")
            _, ocr_entries = self._get_ocr_data()
            amount_field = self._find_input_field([amount_label] + amount_labels, ocr_entries)
            
            if amount_field:
                steps_log.append(f"✅ Found amount field at {amount_field}")
                steps_log.append(f"⌨️  Typing amount: ₹{amount}")
                self.type_in_field(amount_field, amount)
                time.sleep(0.5)
            else:
                steps_log.append("⚠️  Amount field not found, trying next field...")
                # Press Tab to go to next field
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.write(amount, interval=0.1)
            
            # Step 4: Click Submit button
            steps_log.append("🔍 Looking for Submit button...")
            time.sleep(0.5)
            
            submit_clicked = False
            for button_text in [submit_label] + submit_labels:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    submit_clicked = True
                    break
            
            if not submit_clicked:
                steps_log.append("⚠️  Submit button not found, pressing Enter...")
                pyautogui.press('enter')
            
            # Wait for processing
            time.sleep(2)

            # Step 5: Wait for fingerprint prompt and user action
            steps_log.append("🧬 Waiting for fingerprint prompt...")
            fingerprint_prompt = self._wait_for_screen_text(fingerprint_phrases, timeout=20)
            if fingerprint_prompt:
                steps_log.append(f"✅ Fingerprint prompt detected ({fingerprint_prompt})")
                try:
                    from core.voice import speak
                    speak("Kripya morpho par ungli lagaiye.")
                except Exception:
                    pass
                self._wait_for_screen_text(["success", "approved", "balance", "transaction", "done"], timeout=30)
            else:
                steps_log.append("⚠️  Fingerprint prompt not detected, continuing...")

            # Step 6: Read screen for confirmation and balance
            time.sleep(1)
            steps_log.append("📖 Reading screen for confirmation...")
            
            extracted_amount = self.extract_amount_from_screen()
            remaining_balance = self.extract_balance_from_screen()

            # Step 7: Click Print button
            steps_log.append("🔍 Looking for Print button...")
            print_clicked = False
            for button_text in [print_label] + print_labels:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    print_clicked = True
                    break
            if not print_clicked:
                steps_log.append("⚠️  Print button not found")

            # Wait for print dialog
            time.sleep(1)

            # Step 8: Click OK on print dialog
            steps_log.append("🔍 Looking for OK button...")
            ok_clicked = False
            for button_text in ["OK", "Ok", "Close", "Done"]:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    ok_clicked = True
                    break
            if not ok_clicked:
                steps_log.append("⚠️  OK button not found, pressing Enter...")
                pyautogui.press('enter')
            
            # Build final response
            response = "🏧 Aadhar ATM Withdrawal Complete!\n\n"
            response += "📋 Steps Executed:\n"
            response += "\n".join(f"   {step}" for step in steps_log)
            response += "\n\n"
            
            if extracted_amount:
                response += f"💰 Withdrawal Confirmed: ₹{extracted_amount}\n"
                response += f"✅ Aapka ₹{extracted_amount} nikla hai!\n"
            else:
                response += f"💰 Requested Amount: ₹{amount}\n"
                response += f"✅ Aapka ₹{amount} nikalne ki request submit ho gayi hai!\n"

            if remaining_balance:
                response += f"\n🏦 Remaining Balance: ₹{remaining_balance}\n"
            
            response += f"\n📝 Aadhar: {aadhar_number[:4]}****{aadhar_number[-4:]}"
            
            # Voice confirmation
            try:
                from core.voice import speak
                if extracted_amount:
                    speak(f"Aapka {extracted_amount} rupaye nikla hai")
                else:
                    speak(f"Aapka {amount} rupaye nikalne ki request submit ho gayi hai")
                if remaining_balance:
                    speak(f"Aapka baki balance {remaining_balance} rupaye hai")
            except:
                pass
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error during withdrawal: {str(e)}\n\n"
            error_msg += "📋 Steps completed:\n"
            error_msg += "\n".join(f"   {step}" for step in steps_log)
            return error_msg


# Create skill instance
skill = AadharATMSkill()

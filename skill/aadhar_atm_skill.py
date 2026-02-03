#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM Automation Skill for JARVIS
AI Agent that reads screen and fills forms automatically
"""

import importlib.util
import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Callable

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

if (
    importlib.util.find_spec("pyautogui")
    and importlib.util.find_spec("pytesseract")
    and importlib.util.find_spec("PIL")
    and importlib.util.find_spec("cv2")
    and importlib.util.find_spec("numpy")
):
    import pyautogui
    import pytesseract
    from PIL import Image, ImageGrab
    import cv2
    import numpy as np
else:
    pyautogui = None
    pytesseract = None

from core.skill import Skill


class AadharATMSkill(Skill):
    """AI Agent for Aadhar ATM automation with screen reading"""
    
    def __init__(self):
        self.aadhar_number = None
        self.withdrawal_amount = None
        
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

    def read_screen_text_raw(self):
        """Read raw screen text without decorations."""
        if not pytesseract:
            return ""
        screenshot = self.capture_screen()
        if not screenshot:
            return ""
        screenshot_np = np.array(screenshot)
        gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    def _ollama_available(self) -> bool:
        if not importlib.util.find_spec("requests"):
            return False
        import requests

        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            return response.status_code == 200
        except Exception:
            return False

    def _ollama_suggest_labels(self, screen_text: str) -> Dict[str, List[str]]:
        """Use Ollama to suggest label keywords from OCR text."""
        if not screen_text or not self._ollama_available():
            return {}
        import json
        import requests

        prompt = (
            "You are analyzing ATM OCR text. Return JSON with keys "
            "aadhar_labels, amount_labels, submit_labels, print_labels. "
            "Each value is an array of short label strings from the text. "
            f"OCR_TEXT:\n{screen_text}"
        )

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2", "prompt": prompt, "stream": False},
                timeout=6,
            )
            if response.status_code != 200:
                return {}
            data = response.json()
            content = data.get("response", "{}")
            parsed = json.loads(content)
            return {
                "aadhar_labels": parsed.get("aadhar_labels", []),
                "amount_labels": parsed.get("amount_labels", []),
                "submit_labels": parsed.get("submit_labels", []),
                "print_labels": parsed.get("print_labels", []),
            }
        except Exception:
            return {}
    
    def find_text_on_screen(self, search_text):
        """Find text on screen and return its position"""
        try:
            screenshot = self.capture_screen()
            if not screenshot:
                return None
            
            # Convert to OpenCV format
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            
            # Get text with bounding boxes
            data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
            
            # Search for text
            for i, text in enumerate(data['text']):
                if search_text.lower() in text.lower():
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    return (x + w // 2, y + h // 2)
            
            return None
            
        except Exception as e:
            print(f"Text search error: {e}")
            return None
    
    def find_input_field(self, label_text):
        """Find input field near a label"""
        try:
            label_pos = self.find_text_on_screen(label_text)
            if label_pos:
                # Input field is usually to the right or below the label
                x, y = label_pos
                # Try right first
                return (x + 200, y)
            return None
        except Exception as e:
            print(f"Input field search error: {e}")
            return None

    def wait_for_keywords(self, keywords, timeout=15):
        """Wait until any keyword appears on screen."""
        start = time.time()
        while time.time() - start < timeout:
            text = self.read_screen_text(region="full")
            if any(keyword.lower() in text.lower() for keyword in keywords):
                return True
            time.sleep(1)
        return False
    
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
        """Extract remaining balance from screen text."""
        try:
            screenshot = self.capture_screen()
            if not screenshot:
                return None

            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)

            patterns = [
                r'Balance:?\s*(\d+)',
                r'Available Balance:?\s*(\d+)',
                r'Remaining:?\s*(\d+)',
                r'Bal\.?:?\s*(\d+)',
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
        
        if not pyautogui or not pytesseract:
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
            screen_text = self.read_screen_text_raw()
            suggested = self._ollama_suggest_labels(screen_text)
            aadhar_labels = ["Aadhar", "Aadhaar", "Card Number", "Number"]
            amount_labels = ["Amount", "Withdraw", "Enter Amount", "Money"]
            submit_labels = ["Submit", "OK", "Confirm", "Proceed", "Next"]
            print_labels = ["Print", "Receipt", "Print Receipt"]

            if suggested:
                aadhar_labels = suggested.get("aadhar_labels", []) + aadhar_labels
                amount_labels = suggested.get("amount_labels", []) + amount_labels
                submit_labels = suggested.get("submit_labels", []) + submit_labels
                print_labels = suggested.get("print_labels", []) + print_labels
            
            # Step 1: Wait for screen to be ready
            steps_log.append("⏳ Waiting for ATM screen...")
            self.wait_for_keywords(["Aadhar", "Aadhaar", "UID", "Aadhaar Number"], timeout=8)
            
            # Step 2: Find and fill Aadhar number field
            steps_log.append("🔍 Looking for Aadhar number field...")
            aadhar_field = None
            for label in aadhar_labels:
                aadhar_field = self.find_input_field(label)
                if aadhar_field:
                    break
            
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
            amount_field = None
            for label in amount_labels:
                amount_field = self.find_input_field(label)
                if amount_field:
                    break
            
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
            for button_text in submit_labels:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    submit_clicked = True
                    break

            if not submit_clicked:
                steps_log.append("⚠️  Submit button not found, pressing Enter...")
                pyautogui.press('enter')

            # Wait for biometric prompt
            steps_log.append("🖐️  Waiting for fingerprint prompt (Morpho)...")
            self.wait_for_keywords(["fingerprint", "biometric", "morpho"], timeout=20)
            time.sleep(3)

            # Step 5: Read screen for confirmation and balance
            steps_log.append("📖 Reading screen for confirmation...")

            extracted_amount = self.extract_amount_from_screen()
            remaining_balance = self.extract_balance_from_screen()

            # Step 6: Click Print button
            steps_log.append("🔍 Looking for Print button...")

            print_clicked = False
            for button_text in print_labels:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    print_clicked = True
                    break

            if not print_clicked:
                steps_log.append("⚠️  Print button not found")

            # Wait for print dialog
            time.sleep(1)

            # Step 7: Click OK on print dialog
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
                response += f"📉 Remaining Balance: ₹{remaining_balance}\n"
            
            response += f"\n📝 Aadhar: {aadhar_number[:4]}****{aadhar_number[-4:]}"
            
            # Voice confirmation
            if importlib.util.find_spec("core.voice"):
                from core.voice import speak
                try:
                    if extracted_amount:
                        speak(f"Aapka {extracted_amount} rupaye nikla hai")
                    else:
                        speak(f"Aapka {amount} rupaye nikalne ki request submit ho gayi hai")
                except Exception:
                    pass
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error during withdrawal: {str(e)}\n\n"
            error_msg += "📋 Steps completed:\n"
            error_msg += "\n".join(f"   {step}" for step in steps_log)
            return error_msg


# Create skill instance
skill = AadharATMSkill()

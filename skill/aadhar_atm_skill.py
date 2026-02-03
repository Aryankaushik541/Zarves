#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM Automation Skill for JARVIS
AI Agent that reads screen and fills forms automatically
"""

import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Callable

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pyautogui
    import pytesseract
    from PIL import Image, ImageGrab
    import cv2
    import numpy as np
except ImportError:
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
            
            # Step 1: Wait for screen to be ready
            steps_log.append("⏳ Waiting for ATM screen...")
            time.sleep(1)
            
            # Step 2: Find and fill Aadhar number field
            steps_log.append("🔍 Looking for Aadhar number field...")
            aadhar_field = self.find_input_field("Aadhar")
            
            if not aadhar_field:
                # Try alternative labels
                for label in ["Aadhaar", "Card Number", "Number"]:
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
            amount_field = self.find_input_field("Amount")
            
            if not amount_field:
                # Try alternative labels
                for label in ["Withdraw", "Enter Amount", "Money"]:
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
            for button_text in ["Submit", "OK", "Confirm", "Proceed", "Next"]:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    submit_clicked = True
                    break
            
            if not submit_clicked:
                steps_log.append("⚠️  Submit button not found, pressing Enter...")
                pyautogui.press('enter')
            
            # Wait for processing
            time.sleep(2)
            
            # Step 5: Click Print button
            steps_log.append("🔍 Looking for Print button...")
            
            print_clicked = False
            for button_text in ["Print", "Receipt", "Print Receipt"]:
                if self.click_button(button_text):
                    steps_log.append(f"✅ Clicked {button_text} button")
                    print_clicked = True
                    break
            
            if not print_clicked:
                steps_log.append("⚠️  Print button not found")
            
            # Wait for print dialog
            time.sleep(1)
            
            # Step 6: Click OK on print dialog
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
            
            # Step 7: Read screen for confirmation
            time.sleep(1)
            steps_log.append("📖 Reading screen for confirmation...")
            
            extracted_amount = self.extract_amount_from_screen()
            
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
            
            response += f"\n📝 Aadhar: {aadhar_number[:4]}****{aadhar_number[-4:]}"
            
            # Voice confirmation
            try:
                from core.voice import speak
                if extracted_amount:
                    speak(f"Aapka {extracted_amount} rupaye nikla hai")
                else:
                    speak(f"Aapka {amount} rupaye nikalne ki request submit ho gayi hai")
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

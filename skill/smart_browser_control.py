#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 Smart Browser Control Skill
Advanced browser automation with AI
"""

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SmartBrowserControl:
    """
    Advanced browser automation
    Can understand natural commands and execute them
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.current_url = None
        
    def initialize_browser(self):
        """Initialize Chrome browser"""
        if self.driver is not None:
            return True
            
        try:
            options = Options()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option("detach", True)
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self.wait = WebDriverWait(self.driver, 10)
            return True
            
        except Exception as e:
            print(f"❌ Browser initialization failed: {e}")
            return False
    
    def open_website(self, url):
        """Open a website"""
        if not self.initialize_browser():
            return False
            
        try:
            # Add https if not present
            if not url.startswith('http'):
                url = 'https://' + url
            
            self.driver.get(url)
            self.current_url = url
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Failed to open {url}: {e}")
            return False
    
    def search_google(self, query):
        """Search on Google"""
        if not self.initialize_browser():
            return False
            
        try:
            self.driver.get('https://www.google.com')
            time.sleep(1)
            
            # Find search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            return False
    
    def search_youtube(self, query):
        """Search on YouTube"""
        if not self.initialize_browser():
            return False
            
        try:
            self.driver.get('https://www.youtube.com')
            time.sleep(2)
            
            # Find search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'search_query'))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ YouTube search failed: {e}")
            return False
    
    def click_first_result(self):
        """Click first search result"""
        try:
            # Wait for results
            time.sleep(2)
            
            # Try different selectors for first result
            selectors = [
                "//h3",
                "//a[@href]",
                ".yuRUbf a",
                "#search a"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    element.click()
                    time.sleep(2)
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    
    def type_text(self, text, selector=None):
        """Type text in active element or specific selector"""
        try:
            if selector:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
            else:
                # Use active element
                element = self.driver.switch_to.active_element
            
            element.clear()
            element.send_keys(text)
            return True
            
        except Exception as e:
            print(f"❌ Type failed: {e}")
            return False
    
    def scroll_down(self, amount=500):
        """Scroll down page"""
        try:
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False
    
    def scroll_up(self, amount=500):
        """Scroll up page"""
        try:
            self.driver.execute_script(f"window.scrollBy(0, -{amount});")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False
    
    def go_back(self):
        """Go back in browser history"""
        try:
            self.driver.back()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Go back failed: {e}")
            return False
    
    def go_forward(self):
        """Go forward in browser history"""
        try:
            self.driver.forward()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Go forward failed: {e}")
            return False
    
    def refresh_page(self):
        """Refresh current page"""
        try:
            self.driver.refresh()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"❌ Refresh failed: {e}")
            return False
    
    def get_page_title(self):
        """Get current page title"""
        try:
            return self.driver.title
        except:
            return None
    
    def get_current_url(self):
        """Get current URL"""
        try:
            return self.driver.current_url
        except:
            return None
    
    def take_screenshot(self, filename='screenshot.png'):
        """Take screenshot of current page"""
        try:
            self.driver.save_screenshot(filename)
            return True
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return False
    
    def close_browser(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
            return True
        except Exception as e:
            print(f"❌ Close failed: {e}")
            return False
    
    def execute_command(self, command):
        """
        Execute natural language command
        Examples:
        - "open google.com"
        - "search for python tutorials"
        - "click first result"
        - "scroll down"
        - "go back"
        """
        command = command.lower().strip()
        
        # Open website
        if command.startswith('open '):
            url = command.replace('open ', '').strip()
            return self.open_website(url)
        
        # Search commands
        elif 'search' in command or 'find' in command:
            query = re.sub(r'(search|find|for|on google|on youtube)', '', command).strip()
            
            if 'youtube' in command:
                return self.search_youtube(query)
            else:
                return self.search_google(query)
        
        # Click commands
        elif 'click' in command:
            if 'first' in command or '1' in command:
                return self.click_first_result()
        
        # Scroll commands
        elif 'scroll down' in command:
            return self.scroll_down()
        elif 'scroll up' in command:
            return self.scroll_up()
        
        # Navigation
        elif 'back' in command or 'go back' in command:
            return self.go_back()
        elif 'forward' in command or 'go forward' in command:
            return self.go_forward()
        elif 'refresh' in command or 'reload' in command:
            return self.refresh_page()
        
        # Close
        elif 'close' in command or 'quit' in command:
            return self.close_browser()
        
        else:
            print(f"❓ Unknown command: {command}")
            return False


# Example usage
if __name__ == "__main__":
    browser = SmartBrowserControl()
    
    # Test commands
    commands = [
        "open google.com",
        "search for Python programming",
        "click first result",
        "scroll down",
        "go back",
        "close browser"
    ]
    
    for cmd in commands:
        print(f"\n🔹 Executing: {cmd}")
        result = browser.execute_command(cmd)
        print(f"✅ Success" if result else "❌ Failed")
        time.sleep(2)

import os
import sys
import subprocess
import traceback
import json
from typing import Dict, Any, Optional
import importlib.util

class SelfHealingSystem:
    """
    Self-healing system that automatically detects and fixes errors.
    Handles missing dependencies, configuration issues, and runtime errors.
    """
    
    def __init__(self):
        self.error_log = []
        self.fix_attempts = {}
        self.max_fix_attempts = 3
        
    def log_error(self, error_type: str, error_msg: str, context: Dict[str, Any] = None):
        """Log errors for analysis"""
        self.error_log.append({
            "type": error_type,
            "message": error_msg,
            "context": context or {},
            "timestamp": self._get_timestamp()
        })
        
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
    
    def check_and_install_package(self, package_name: str, import_name: str = None) -> bool:
        """
        Check if a package is installed, if not, install it automatically.
        
        Args:
            package_name: Name of the package to install (e.g., 'pywhatkit')
            import_name: Name to use for import (if different from package_name)
        
        Returns:
            True if package is available, False otherwise
        """
        if import_name is None:
            import_name = package_name
            
        # Check if already installed
        if importlib.util.find_spec(import_name) is not None:
            return True
        
        # Check if we've tried too many times
        if self.fix_attempts.get(package_name, 0) >= self.max_fix_attempts:
            print(f"❌ {package_name} install करने में बार-बार विफल। कृपया manually install करें।")
            return False
        
        print(f"📦 {package_name} नहीं मिला। Auto-install कर रहा हूँ...")
        
        try:
            # Increment attempt counter
            self.fix_attempts[package_name] = self.fix_attempts.get(package_name, 0) + 1
            
            # Install package
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name, "--quiet"
            ])
            
            print(f"✅ {package_name} successfully install हो गया!")
            self.log_error("dependency_fixed", f"Auto-installed {package_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ {package_name} install नहीं हो सका: {e}")
            self.log_error("dependency_install_failed", str(e), {"package": package_name})
            return False
    
    def fix_import_error(self, error: ImportError) -> bool:
        """
        Automatically fix import errors by installing missing packages.
        
        Args:
            error: The ImportError exception
            
        Returns:
            True if fixed, False otherwise
        """
        error_msg = str(error)
        
        # Common package mappings (import name -> package name)
        package_mappings = {
            "pyttsx3": "pyttsx3",
            "speech_recognition": "SpeechRecognition",
            "sr": "SpeechRecognition",
            "dotenv": "python-dotenv",
            "PyQt5": "PyQt5",
            "pywhatkit": "pywhatkit",
            "pyaudio": "pyaudio",
            "groq": "groq",
        }
        
        # Try to extract package name from error
        for import_name, package_name in package_mappings.items():
            if import_name in error_msg.lower():
                return self.check_and_install_package(package_name, import_name)
        
        # Generic handling
        if "No module named" in error_msg:
            module_name = error_msg.split("'")[1] if "'" in error_msg else None
            if module_name:
                return self.check_and_install_package(module_name)
        
        return False
    
    def fix_microphone_error(self) -> bool:
        """Fix microphone/audio input errors"""
        print("🎤 Microphone issue detect हुआ। Fix कर रहा हूँ...")
        
        try:
            # Check if pyaudio is installed
            if not self.check_and_install_package("pyaudio"):
                print("💡 Tip: pyaudio manually install करें:")
                if sys.platform == "darwin":
                    print("   brew install portaudio")
                    print("   pip install pyaudio")
                elif sys.platform == "win32":
                    print("   pip install pipwin")
                    print("   pipwin install pyaudio")
                return False
            
            return True
            
        except Exception as e:
            self.log_error("microphone_fix_failed", str(e))
            return False
    
    def fix_tts_error(self) -> bool:
        """Fix text-to-speech errors"""
        print("🔊 TTS issue detect हुआ। Fix कर रहा हूँ...")
        
        try:
            # Reinstall pyttsx3
            if not self.check_and_install_package("pyttsx3"):
                return False
            
            # Platform-specific fixes
            if sys.platform == "darwin":
                # macOS - check if pyobjc is installed
                self.check_and_install_package("pyobjc-core")
                self.check_and_install_package("pyobjc-framework-Cocoa")
            elif sys.platform == "win32":
                # Windows - check if pywin32 is installed
                self.check_and_install_package("pywin32")
            
            return True
            
        except Exception as e:
            self.log_error("tts_fix_failed", str(e))
            return False
    
    def fix_api_key_error(self) -> bool:
        """Fix API key configuration errors"""
        print("🔑 API key issue detect हुआ। Fix कर रहा हूँ...")
        
        try:
            # Check if .env file exists
            if not os.path.exists(".env"):
                if os.path.exists(".env.template"):
                    print("📝 .env file बना रहा हूँ .env.template से...")
                    with open(".env.template", "r") as template:
                        with open(".env", "w") as env_file:
                            env_file.write(template.read())
                    print("✅ .env file बन गई। कृपया अपनी API keys add करें।")
                else:
                    print("❌ .env.template नहीं मिला। कृपया manually .env file बनाएं।")
                return False
            
            # Check if GROQ_API_KEY is set
            from dotenv import load_dotenv
            load_dotenv()
            
            if not os.environ.get("GROQ_API_KEY"):
                print("⚠️  GROQ_API_KEY .env file में नहीं मिली।")
                print("💡 कृपया .env file में GROQ_API_KEY add करें।")
                return False
            
            return True
            
        except Exception as e:
            self.log_error("api_key_fix_failed", str(e))
            return False
    
    def auto_fix_error(self, error: Exception, context: str = "") -> bool:
        """
        Main auto-fix function that tries to resolve any error.
        
        Args:
            error: The exception that occurred
            context: Context about where the error occurred
            
        Returns:
            True if error was fixed, False otherwise
        """
        error_type = type(error).__name__
        error_msg = str(error)
        
        print(f"\n⚠️  Error detect हुआ: {error_type}")
        print(f"📍 Context: {context}")
        print(f"💬 Message: {error_msg}")
        print(f"🔧 Auto-fix attempt कर रहा हूँ...\n")
        
        # Log the error
        self.log_error(error_type, error_msg, {"context": context})
        
        # Try different fix strategies based on error type
        if isinstance(error, ImportError) or isinstance(error, ModuleNotFoundError):
            return self.fix_import_error(error)
        
        elif "microphone" in error_msg.lower() or "audio" in error_msg.lower():
            return self.fix_microphone_error()
        
        elif "tts" in error_msg.lower() or "pyttsx3" in error_msg.lower():
            return self.fix_tts_error()
        
        elif "api" in error_msg.lower() and "key" in error_msg.lower():
            return self.fix_api_key_error()
        
        elif "groq" in error_msg.lower():
            return self.fix_api_key_error()
        
        else:
            # Generic error handling
            print(f"❌ इस error को automatically fix नहीं कर सकता: {error_type}")
            print(f"💡 Error details:")
            traceback.print_exc()
            return False
    
    def get_error_report(self) -> str:
        """Generate a report of all errors and fixes"""
        if not self.error_log:
            return "✅ कोई errors नहीं मिले!"
        
        report = f"\n📊 Error Report ({len(self.error_log)} errors logged):\n"
        report += "=" * 60 + "\n"
        
        for i, error in enumerate(self.error_log, 1):
            report += f"\n{i}. {error['type']}\n"
            report += f"   Time: {error['timestamp']}\n"
            report += f"   Message: {error['message']}\n"
            if error['context']:
                report += f"   Context: {error['context']}\n"
        
        return report
    
    def clear_error_log(self):
        """Clear the error log"""
        self.error_log = []
        self.fix_attempts = {}
        print("✅ Error log cleared!")


# Global instance
self_healing = SelfHealingSystem()

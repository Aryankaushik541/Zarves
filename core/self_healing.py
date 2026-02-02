"""
Self-Healing System for JARVIS
Automatically detects and fixes common errors without user intervention
Now with Advanced Self-Coding AI integration
"""

import os
import sys
import subprocess
import traceback
from typing import Optional, Dict, List
from datetime import datetime


class SelfHealing:
    """Autonomous error detection and fixing system with AI code generation"""
    
    def __init__(self):
        self.error_log: List[Dict] = []
        self.fix_attempts: Dict[str, int] = {}
        self.max_fix_attempts = 3
        self.advanced_coder = None
        
        # Try to initialize advanced self-coder
        try:
            from core.advanced_self_coder import advanced_self_coder
            self.advanced_coder = advanced_self_coder
            print("✅ Advanced Self-Coder integrated with Self-Healing")
        except Exception as e:
            print(f"⚠️  Advanced Self-Coder not available: {e}")
        
    def log_error(self, error: Exception, context: str = ""):
        """Log error for analysis"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        self.error_log.append(error_entry)
        
    def auto_fix_error(self, error: Exception, context: str = "", file_path: str = None) -> bool:
        """
        Automatically attempt to fix the error.
        Now with AI-powered code generation!
        
        Args:
            error: The exception that occurred
            context: Context where error happened
            file_path: Path to file with error (for AI fixes)
        
        Returns:
            True if fixed, False if cannot fix.
        """
        self.log_error(error, context)
        error_type = type(error).__name__
        error_msg = str(error)
        
        # Check if we've tried too many times
        fix_key = f"{error_type}:{error_msg}"
        if self.fix_attempts.get(fix_key, 0) >= self.max_fix_attempts:
            print(f"⚠️  Maximum fix attempts reached for: {error_type}")
            return False
        
        self.fix_attempts[fix_key] = self.fix_attempts.get(fix_key, 0) + 1
        
        # Try basic fixes first (fast)
        basic_fix = self._try_basic_fix(error_type, error_msg, context)
        if basic_fix:
            return True
        
        # If basic fix failed and we have advanced coder, try AI fix
        if self.advanced_coder and file_path:
            print(f"\n🤖 Trying AI-powered fix...")
            ai_fix = self.advanced_coder.analyze_error_and_fix(error, context, file_path)
            if ai_fix:
                print(f"✅ AI successfully fixed the error!")
                print(f"💡 Please restart JARVIS to apply changes: python main.py")
                return True
        
        print(f"❌ Could not automatically fix: {error_type}")
        return False
    
    def _try_basic_fix(self, error_type: str, error_msg: str, context: str) -> bool:
        """Try basic/fast fixes first"""
        
        if error_type == "ModuleNotFoundError" or error_type == "ImportError":
            return self._fix_import_error(error_msg)
        
        elif error_type == "AttributeError":
            return self._fix_attribute_error(error_msg, context)
        
        elif error_type == "FileNotFoundError":
            return self._fix_file_not_found(error_msg)
        
        elif error_type == "PermissionError":
            return self._fix_permission_error(error_msg)
        
        elif "API" in error_msg or "key" in error_msg.lower():
            return self._fix_api_error(error_msg)
        
        return False
    
    def _fix_attribute_error(self, error_msg: str, context: str) -> bool:
        """
        Fix AttributeError by analyzing the missing attribute and suggesting fixes.
        """
        print(f"🔧 Attempting to fix AttributeError...")
        
        # Extract object and attribute from error message
        if "has no attribute" in error_msg:
            parts = error_msg.split("'")
            if len(parts) >= 4:
                class_name = parts[1]
                attr_name = parts[3]
                
                print(f"   Missing: {class_name}.{attr_name}")
                
                # Common fixes for known issues
                if class_name == "SkillRegistry":
                    if attr_name == "get_all_tools":
                        print(f"✅ Known issue: SkillRegistry missing get_all_tools()")
                        print(f"   This has been fixed in the latest code.")
                        print(f"   Please restart JARVIS: python main.py")
                        return True
                    
                    elif attr_name in ["get_all_functions", "get_skill", "list_skills"]:
                        print(f"✅ Known issue: SkillRegistry missing helper methods")
                        print(f"   This has been fixed in the latest code.")
                        print(f"   Please restart JARVIS: python main.py")
                        return True
                
                # Generic suggestions
                print(f"💡 Suggestions:")
                print(f"   1. Check if {class_name} class has {attr_name} method")
                print(f"   2. Verify the object type is correct")
                print(f"   3. Check for typos in attribute name")
                
        return False
    
    def _fix_import_error(self, error_msg: str) -> bool:
        """Fix missing module by auto-installing"""
        print(f"🔧 Attempting to fix import error...")
        
        # Extract module name
        module_name = None
        if "No module named" in error_msg:
            module_name = error_msg.split("'")[1].split(".")[0]
        
        if not module_name:
            return False
        
        print(f"📦 {module_name} नहीं मिला। Auto-install कर रहा हूँ...")
        
        try:
            # Try to install the package
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", module_name, "-q"
            ])
            print(f"✅ {module_name} successfully install हो गया!")
            return True
        except subprocess.CalledProcessError:
            # Try common package name mappings
            package_map = {
                'cv2': 'opencv-python',
                'PIL': 'Pillow',
                'sklearn': 'scikit-learn',
                'speech_recognition': 'SpeechRecognition',
                'pywhatkit': 'pywhatkit',
            }
            
            if module_name in package_map:
                actual_package = package_map[module_name]
                print(f"   Trying alternative package: {actual_package}")
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", actual_package, "-q"
                    ])
                    print(f"✅ {actual_package} successfully install हो गया!")
                    return True
                except:
                    pass
            
            print(f"❌ {module_name} install नहीं हो सका")
            return False
    
    def _fix_file_not_found(self, error_msg: str) -> bool:
        """Fix file not found errors"""
        print(f"🔧 Attempting to fix file not found error...")
        
        # Extract filename if possible
        if "[Errno 2]" in error_msg or "No such file" in error_msg:
            # Try to create common directories
            common_dirs = ['logs', 'data', 'temp', 'cache', 'skill']
            for dir_name in common_dirs:
                if dir_name in error_msg.lower():
                    try:
                        os.makedirs(dir_name, exist_ok=True)
                        print(f"✅ Created directory: {dir_name}")
                        return True
                    except:
                        pass
        
        return False
    
    def _fix_permission_error(self, error_msg: str) -> bool:
        """Fix permission errors"""
        print(f"🔧 Attempting to fix permission error...")
        print(f"💡 Suggestion: Run as administrator or check file permissions")
        return False
    
    def _fix_api_error(self, error_msg: str) -> bool:
        """Fix API-related errors"""
        print(f"🔧 Checking API configuration...")
        
        if "GROQ_API_KEY" in error_msg or "API key" in error_msg:
            return self.fix_api_key_error()
        
        return False
    
    def fix_api_key_error(self) -> bool:
        """Fix missing API key"""
        print(f"🔧 Attempting to fix API key error...")
        
        # Check if .env exists
        if not os.path.exists('.env'):
            print(f"📝 Creating .env file...")
            try:
                with open('.env', 'w') as f:
                    f.write("# JARVIS Configuration\n")
                    f.write("GROQ_API_KEY=your_api_key_here\n")
                print(f"✅ .env file created!")
                print(f"💡 Please add your GROQ_API_KEY to .env file")
                return False  # User needs to add key manually
            except Exception as e:
                print(f"❌ Could not create .env file: {e}")
                return False
        
        # Check if key is set but empty
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key or api_key == "your_api_key_here":
            print(f"⚠️  GROQ_API_KEY is not set or invalid")
            print(f"💡 Please set your API key in .env file:")
            print(f"   GROQ_API_KEY=your_actual_key_here")
            return False
        
        return True
    
    def create_skill_with_ai(self, skill_name: str, description: str, functions: List[str]) -> bool:
        """
        Create a new skill using AI code generation
        
        Args:
            skill_name: Name of the skill
            description: What the skill does
            functions: List of function names
        
        Returns:
            True if skill created successfully
        """
        if not self.advanced_coder:
            print("⚠️  Advanced Self-Coder not available")
            return False
        
        return self.advanced_coder.create_new_skill(skill_name, description, functions)
    
    def improve_code_with_ai(self, file_path: str, improvement_type: str = "performance") -> bool:
        """
        Improve existing code using AI
        
        Args:
            file_path: Path to file to improve
            improvement_type: Type of improvement
        
        Returns:
            True if improvement successful
        """
        if not self.advanced_coder:
            print("⚠️  Advanced Self-Coder not available")
            return False
        
        return self.advanced_coder.improve_code(file_path, improvement_type)
    
    def get_error_report(self) -> str:
        """Generate error report"""
        if not self.error_log:
            return "✅ No errors logged"
        
        report = f"\n{'='*60}\n"
        report += f"📊 Error Report ({len(self.error_log)} errors)\n"
        report += f"{'='*60}\n\n"
        
        # Group errors by type
        error_types = {}
        for error in self.error_log:
            error_type = error['type']
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(error)
        
        for error_type, errors in error_types.items():
            report += f"🔴 {error_type} ({len(errors)} occurrences)\n"
            for error in errors[-3:]:  # Show last 3 of each type
                report += f"   • {error['message']}\n"
                if error['context']:
                    report += f"     Context: {error['context']}\n"
            report += "\n"
        
        # Add AI fix history if available
        if self.advanced_coder:
            report += "\n" + self.advanced_coder.get_fix_history()
        
        return report


# Global instance
self_healing = SelfHealing()

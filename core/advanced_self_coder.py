"""
Advanced Self-Coding AI for JARVIS
Automatically writes, fixes, and improves its own code at runtime
Uses LLM to generate code fixes and improvements
"""

import os
import sys
import ast
import json
import traceback
import subprocess
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from ollama import Client

class AdvancedSelfCoder:
    """
    Advanced AI that can write and fix its own code
    - Analyzes errors and generates fixes
    - Writes new skills on demand
    - Improves existing code
    - Tests fixes before applying
    """
    
    def __init__(self):
        self.client = None
        self.model = "llama3.2"  # Fast local model for code generation
        self.fix_history: List[Dict] = []
        self.code_cache: Dict[str, str] = {}
        
        # Initialize Ollama client
        try:
            ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            self.client = Client(host=ollama_host)
            
            # Test connection
            try:
                self.client.list()
                print("✅ Advanced Self-Coder integrated with Self-Healing")
            except:
                print("⚠️  Ollama not running - Self-Coder disabled")
                print("💡 Start Ollama: ollama serve")
                self.client = None
        except Exception as e:
            print(f"⚠️  Self-Coder initialization failed: {e}")
    
    def analyze_error_and_fix(self, error: Exception, context: str, file_path: str = None) -> bool:
        """
        Analyze error and automatically generate + apply fix
        
        Args:
            error: The exception that occurred
            context: Context where error happened
            file_path: Path to file with error (optional)
        
        Returns:
            True if fix was successful, False otherwise
        """
        if not self.client:
            return False
        
        print(f"\n🤖 Advanced Self-Coder analyzing error...")
        
        try:
            # Get error details
            error_type = type(error).__name__
            error_msg = str(error)
            error_trace = traceback.format_exc()
            
            # Read current code if file path provided
            current_code = ""
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    current_code = f.read()
            
            # Generate fix using LLM
            fix_code = self._generate_fix(error_type, error_msg, error_trace, current_code, context)
            
            if not fix_code:
                print("❌ Could not generate fix")
                return False
            
            # Validate fix
            if not self._validate_code(fix_code):
                print("❌ Generated fix has syntax errors")
                return False
            
            # Apply fix
            if file_path:
                return self._apply_fix(file_path, fix_code)
            else:
                print("✅ Fix generated but no file path to apply")
                print(f"📝 Generated fix:\n{fix_code}")
                return True
                
        except Exception as e:
            print(f"❌ Self-Coder error: {e}")
            return False
    
    def _generate_fix(self, error_type: str, error_msg: str, error_trace: str, 
                     current_code: str, context: str) -> Optional[str]:
        """Generate code fix using LLM"""
        
        prompt = f"""You are an expert Python developer fixing code errors.

Error Type: {error_type}
Error Message: {error_msg}
Context: {context}

Current Code:
```python
{current_code[:2000]}  # First 2000 chars
```

Error Traceback:
{error_trace[:1000]}  # First 1000 chars

Generate ONLY the fixed Python code. No explanations, no markdown, just the corrected code.
The code should:
1. Fix the error
2. Maintain existing functionality
3. Be syntactically correct
4. Include proper error handling

Fixed code:"""

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python code fixing expert. Output only valid Python code, no explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            fixed_code = response['message']['content']
            
            # Clean up response (remove markdown if present)
            if "```python" in fixed_code:
                fixed_code = fixed_code.split("```python")[1].split("```")[0]
            elif "```" in fixed_code:
                fixed_code = fixed_code.split("```")[1].split("```")[0]
            
            return fixed_code.strip()
            
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return None
    
    def _validate_code(self, code: str) -> bool:
        """Validate Python code syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"⚠️  Syntax error in generated code: {e}")
            return False
    
    def _apply_fix(self, file_path: str, fixed_code: str) -> bool:
        """Apply fix to file with backup"""
        try:
            # Create backup
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            
            # Apply fix
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            # Log fix
            self.fix_history.append({
                'timestamp': datetime.now().isoformat(),
                'file': file_path,
                'backup': backup_path,
                'success': True
            })
            
            print(f"✅ AI successfully fixed the error!")
            print(f"💾 Backup saved: {backup_path}")
            print(f"💡 Restart JARVIS to apply changes")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to apply fix: {e}")
            return False
    
    def create_new_skill(self, skill_name: str, description: str, functions: List[str]) -> bool:
        """
        Create a new skill file using AI
        
        Args:
            skill_name: Name of the skill
            description: What the skill should do
            functions: List of function names to implement
        
        Returns:
            True if skill was created successfully
        """
        if not self.client:
            print("⚠️  Ollama not available")
            return False
        
        print(f"\n🤖 Creating new skill: {skill_name}")
        print(f"📝 Description: {description}")
        print(f"🔧 Functions: {', '.join(functions)}")
        
        try:
            # Generate skill code
            skill_code = self._generate_skill_code(skill_name, description, functions)
            
            if not skill_code:
                print("❌ Could not generate skill code")
                return False
            
            # Validate code
            if not self._validate_code(skill_code):
                print("❌ Generated skill has syntax errors")
                return False
            
            # Save skill file
            skill_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skill")
            skill_file = os.path.join(skill_dir, f"{skill_name}_ops.py")
            
            if os.path.exists(skill_file):
                print(f"⚠️  Skill file already exists: {skill_file}")
                return False
            
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(skill_code)
            
            print(f"✅ New skill created: {skill_file}")
            print(f"💡 Restart JARVIS to use new skill!")
            
            return True
            
        except Exception as e:
            print(f"❌ Skill creation error: {e}")
            return False
    
    def _generate_skill_code(self, skill_name: str, description: str, functions: List[str]) -> Optional[str]:
        """Generate skill code using LLM"""
        
        prompt = f"""Create a Python skill class for JARVIS AI assistant.

Skill Name: {skill_name}
Description: {description}
Functions to implement: {', '.join(functions)}

Generate a complete Python file with:
1. Imports
2. Skill class inheriting from core.skill.Skill
3. get_tools() method returning tool definitions
4. get_functions() method returning function mappings
5. Implementation of all functions: {', '.join(functions)}

Example structure:
```python
from core.skill import Skill

class MySkill(Skill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    def get_tools(self):
        return [...]
    
    def get_functions(self):
        return {{...}}
    
    def my_function(self, param):
        # Implementation
        pass
```

Generate ONLY the Python code, no explanations:"""

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python code generation expert. Output only valid Python code."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            code = response['message']['content']
            
            # Clean up response
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]
            
            return code.strip()
            
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return None
    
    def improve_code(self, file_path: str, improvement_type: str = "general") -> bool:
        """
        Improve existing code using AI
        
        Args:
            file_path: Path to file to improve
            improvement_type: Type of improvement (performance, readability, etc.)
        
        Returns:
            True if improvement was successful
        """
        if not self.client:
            print("⚠️  Ollama not available")
            return False
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"\n🤖 Improving code: {file_path}")
        print(f"🎯 Improvement: {improvement_type}")
        
        try:
            # Read current code
            with open(file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # Generate improved code
            improved_code = self._generate_improved_code(current_code, improvement_type)
            
            if not improved_code:
                print("❌ Could not generate improvement")
                return False
            
            # Validate code
            if not self._validate_code(improved_code):
                print("❌ Improved code has syntax errors")
                return False
            
            # Apply improvement
            return self._apply_fix(file_path, improved_code)
            
        except Exception as e:
            print(f"❌ Improvement error: {e}")
            return False
    
    def _generate_improved_code(self, current_code: str, improvement_type: str) -> Optional[str]:
        """Generate improved code using LLM"""
        
        prompt = f"""Improve this Python code for {improvement_type}.

Current Code:
```python
{current_code[:3000]}  # First 3000 chars
```

Improvements to make:
- {improvement_type} optimization
- Better error handling
- Code clarity
- Performance improvements
- Best practices

Generate ONLY the improved Python code, no explanations:"""

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python code optimization expert. Output only improved code."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            code = response['message']['content']
            
            # Clean up response
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]
            
            return code.strip()
            
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return None
    
    def get_fix_history(self) -> List[Dict]:
        """Get history of all fixes applied"""
        return self.fix_history


# Global instance
advanced_self_coder = AdvancedSelfCoder()

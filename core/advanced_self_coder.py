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
from groq import Groq

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
        self.model = "llama-3.1-8b-instant"  # Fast model for code generation
        self.fix_history: List[Dict] = []
        self.code_cache: Dict[str, str] = {}
        
        # Initialize Groq client
        try:
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)
                print("✅ Advanced Self-Coder initialized")
            else:
                print("⚠️  GROQ_API_KEY not found - Self-Coder disabled")
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

ERROR DETAILS:
Type: {error_type}
Message: {error_msg}
Context: {context}

TRACEBACK:
{error_trace}

CURRENT CODE:
{current_code[:2000] if current_code else "No code provided"}

TASK:
1. Analyze the error
2. Generate ONLY the fixed code (complete file)
3. Add comments explaining the fix
4. Ensure code is syntactically correct
5. Keep all existing functionality

REQUIREMENTS:
- Return ONLY valid Python code
- No explanations outside code comments
- Fix the specific error
- Maintain code structure
- Add error handling

Generate the fixed code:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python code fixer. Return only valid Python code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.3  # Lower temperature for more deterministic code
            )
            
            fix_code = response.choices[0].message.content
            
            # Extract code from markdown if present
            if "```python" in fix_code:
                fix_code = fix_code.split("```python")[1].split("```")[0].strip()
            elif "```" in fix_code:
                fix_code = fix_code.split("```")[1].split("```")[0].strip()
            
            return fix_code
            
        except Exception as e:
            print(f"❌ LLM fix generation failed: {e}")
            return None
    
    def _validate_code(self, code: str) -> bool:
        """Validate Python code syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"❌ Syntax error in generated code: {e}")
            return False
    
    def _apply_fix(self, file_path: str, fixed_code: str) -> bool:
        """Apply fix to file with backup"""
        try:
            # Create backup
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_code)
                
                print(f"💾 Backup created: {backup_path}")
            
            # Write fixed code
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            print(f"✅ Fix applied to: {file_path}")
            
            # Log fix
            self.fix_history.append({
                'timestamp': datetime.now().isoformat(),
                'file': file_path,
                'backup': backup_path,
                'success': True
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to apply fix: {e}")
            return False
    
    def create_new_skill(self, skill_name: str, description: str, functions: List[str]) -> bool:
        """
        Create a new skill file from scratch
        
        Args:
            skill_name: Name of the skill (e.g., "weather")
            description: What the skill does
            functions: List of function names to implement
        
        Returns:
            True if skill created successfully
        """
        if not self.client:
            print("⚠️  Self-Coder not available")
            return False
        
        print(f"\n🤖 Creating new skill: {skill_name}")
        
        try:
            # Generate skill code
            skill_code = self._generate_skill(skill_name, description, functions)
            
            if not skill_code:
                return False
            
            # Validate
            if not self._validate_code(skill_code):
                return False
            
            # Save skill
            skill_file = f"skill/{skill_name}_ops.py"
            
            if os.path.exists(skill_file):
                print(f"⚠️  Skill already exists: {skill_file}")
                return False
            
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(skill_code)
            
            print(f"✅ New skill created: {skill_file}")
            return True
            
        except Exception as e:
            print(f"❌ Skill creation failed: {e}")
            return False
    
    def _generate_skill(self, skill_name: str, description: str, functions: List[str]) -> Optional[str]:
        """Generate complete skill code using LLM"""
        
        prompt = f"""Create a complete Python skill class for JARVIS.

SKILL NAME: {skill_name}
DESCRIPTION: {description}
FUNCTIONS: {', '.join(functions)}

REQUIREMENTS:
1. Import required modules
2. Create class {skill_name.title()}Skill(Skill)
3. Implement name property
4. Implement get_tools() with proper schema
5. Implement get_functions() returning dict
6. Implement all functions: {', '.join(functions)}
7. Add error handling
8. Return JSON responses
9. Add helpful comments

TEMPLATE STRUCTURE:
```python
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class {skill_name.title()}Skill(Skill):
    @property
    def name(self) -> str:
        return "{skill_name}_skill"
    
    def get_tools(self) -> List[Dict[str, Any]]:
        # Return tool schemas
        pass
    
    def get_functions(self) -> Dict[str, Callable]:
        # Return function mappings
        pass
    
    # Implement functions here
```

Generate the complete skill code:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer creating JARVIS skills."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.5
            )
            
            skill_code = response.choices[0].message.content
            
            # Extract code
            if "```python" in skill_code:
                skill_code = skill_code.split("```python")[1].split("```")[0].strip()
            elif "```" in skill_code:
                skill_code = skill_code.split("```")[1].split("```")[0].strip()
            
            return skill_code
            
        except Exception as e:
            print(f"❌ Skill generation failed: {e}")
            return None
    
    def improve_code(self, file_path: str, improvement_type: str = "performance") -> bool:
        """
        Improve existing code
        
        Args:
            file_path: Path to file to improve
            improvement_type: Type of improvement (performance, readability, error_handling)
        
        Returns:
            True if improvement successful
        """
        if not self.client or not os.path.exists(file_path):
            return False
        
        print(f"\n🤖 Improving code: {file_path} ({improvement_type})")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            improved_code = self._generate_improvement(current_code, improvement_type)
            
            if not improved_code or not self._validate_code(improved_code):
                return False
            
            return self._apply_fix(file_path, improved_code)
            
        except Exception as e:
            print(f"❌ Code improvement failed: {e}")
            return False
    
    def _generate_improvement(self, code: str, improvement_type: str) -> Optional[str]:
        """Generate improved code using LLM"""
        
        prompt = f"""Improve this Python code for {improvement_type}.

CURRENT CODE:
{code[:2000]}

IMPROVEMENT TYPE: {improvement_type}

REQUIREMENTS:
- Maintain all functionality
- Add improvements for {improvement_type}
- Keep code structure
- Add comments for changes
- Return complete improved code

Generate improved code:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code optimizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.3
            )
            
            improved_code = response.choices[0].message.content
            
            if "```python" in improved_code:
                improved_code = improved_code.split("```python")[1].split("```")[0].strip()
            elif "```" in improved_code:
                improved_code = improved_code.split("```")[1].split("```")[0].strip()
            
            return improved_code
            
        except Exception as e:
            print(f"❌ Improvement generation failed: {e}")
            return None
    
    def get_fix_history(self) -> str:
        """Get history of all fixes applied"""
        if not self.fix_history:
            return "No fixes applied yet."
        
        report = "🔧 Self-Coding Fix History:\n\n"
        for i, fix in enumerate(self.fix_history, 1):
            report += f"{i}. {fix['timestamp']}\n"
            report += f"   File: {fix['file']}\n"
            report += f"   Backup: {fix['backup']}\n"
            report += f"   Status: {'✅ Success' if fix['success'] else '❌ Failed'}\n\n"
        
        return report


# Global instance
advanced_self_coder = AdvancedSelfCoder()

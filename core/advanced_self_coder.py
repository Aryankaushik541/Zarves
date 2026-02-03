"""
Advanced Self-Coding AI for JARVIS
Automatically writes, fixes, and improves its own code at runtime
Uses Ollama LLM + Internet search for comprehensive error fixing
"""

import os
import sys
import ast
import json
import traceback
import subprocess
import requests
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from ollama import Client

class AdvancedSelfCoder:
    """
    Advanced AI that can write and fix its own code
    - Analyzes errors using Ollama AI
    - Searches internet for solutions
    - Generates fixes combining AI + web research
    - Tests fixes before applying
    - Fully autonomous error resolution
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
    
    def _search_error_solution(self, error_type: str, error_msg: str) -> str:
        """
        Search internet for error solutions using DuckDuckGo
        """
        try:
            # Create search query
            search_query = f"Python {error_type} {error_msg} solution fix"
            
            # Use DuckDuckGo API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": search_query,
                "format": "json",
                "no_html": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Extract relevant information
            solutions = []
            
            if data.get("Abstract"):
                solutions.append(f"Solution: {data['Abstract']}")
            
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"][:3]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        solutions.append(topic["Text"])
            
            return "\n".join(solutions) if solutions else ""
            
        except Exception as e:
            print(f"⚠️  Internet search failed: {e}")
            return ""
    
    def _search_stackoverflow(self, error_type: str, error_msg: str) -> str:
        """
        Search StackOverflow-like solutions via Google
        """
        try:
            # Search for Python error solutions
            query = f"site:stackoverflow.com python {error_type} {error_msg}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = requests.get(url, headers=headers, timeout=10)
            
            # Extract snippets (basic scraping)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            snippets = []
            for snippet in soup.find_all('div', class_='VwiC3b')[:2]:
                text = snippet.get_text()
                if text and len(text) > 20:
                    snippets.append(text)
            
            return "\n".join(snippets) if snippets else ""
            
        except Exception as e:
            return ""
    
    def analyze_error_and_fix(self, error: Exception, context: str, file_path: str = None) -> bool:
        """
        Analyze error using AI + Internet and automatically generate + apply fix
        
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
            
            # Search internet for solutions
            print(f"🌐 Searching internet for solutions...")
            web_solutions = self._search_error_solution(error_type, error_msg)
            stackoverflow_solutions = self._search_stackoverflow(error_type, error_msg)
            
            # Combine web research
            internet_research = ""
            if web_solutions:
                internet_research += f"\n📚 Web Solutions:\n{web_solutions}\n"
            if stackoverflow_solutions:
                internet_research += f"\n💡 StackOverflow Solutions:\n{stackoverflow_solutions}\n"
            
            if internet_research:
                print(f"✅ Found solutions from internet")
            
            # Read current code if file path provided
            current_code = ""
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    current_code = f.read()
            
            # Generate fix using LLM + Internet research
            fix_code = self._generate_fix(
                error_type, 
                error_msg, 
                error_trace, 
                current_code, 
                context,
                internet_research
            )
            
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
                     current_code: str, context: str, internet_research: str = "") -> Optional[str]:
        """
        Generate code fix using Ollama AI + Internet research
        """
        try:
            # Create comprehensive prompt
            prompt = f"""You are an expert Python developer fixing code errors.

ERROR DETAILS:
- Type: {error_type}
- Message: {error_msg}
- Context: {context}

TRACEBACK:
{error_trace}

{internet_research}

CURRENT CODE:
```python
{current_code}
```

TASK:
1. Analyze the error carefully
2. Consider the internet solutions provided above
3. Generate ONLY the fixed Python code (no explanations)
4. Ensure the fix is complete and syntactically correct
5. Preserve all existing functionality
6. Add comments explaining the fix

OUTPUT FORMAT:
Return ONLY the complete fixed Python code, nothing else.
"""

            # Call Ollama for fix generation
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python code fixer. Return only valid Python code, no markdown, no explanations."
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
                fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
            elif "```" in fixed_code:
                fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
            
            return fixed_code
            
        except Exception as e:
            print(f"❌ Fix generation failed: {e}")
            return None
    
    def _validate_code(self, code: str) -> bool:
        """
        Validate Python code syntax
        """
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            print(f"⚠️  Syntax error in generated code: {e}")
            return False
    
    def _apply_fix(self, file_path: str, fixed_code: str) -> bool:
        """
        Apply the fix to the file
        """
        try:
            # Backup original file
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            
            print(f"💾 Backup created: {backup_path}")
            
            # Write fixed code
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            print(f"✅ Fix applied to: {file_path}")
            
            # Log the fix
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
    
    def write_new_skill(self, skill_name: str, description: str, requirements: List[str]) -> bool:
        """
        Write a completely new skill from scratch using AI
        """
        if not self.client:
            return False
        
        print(f"\n🤖 Writing new skill: {skill_name}...")
        
        try:
            prompt = f"""Create a new Python skill for JARVIS AI assistant.

SKILL NAME: {skill_name}
DESCRIPTION: {description}
REQUIREMENTS: {', '.join(requirements)}

Create a complete Python skill class that:
1. Inherits from core.skill.Skill
2. Implements get_tools() method returning tool definitions
3. Implements get_functions() method returning callable functions
4. Has proper error handling
5. Follows JARVIS skill pattern

Return ONLY the complete Python code, no explanations.
"""

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python developer. Write clean, production-ready code."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            skill_code = response['message']['content']
            
            # Clean up
            if "```python" in skill_code:
                skill_code = skill_code.split("```python")[1].split("```")[0].strip()
            elif "```" in skill_code:
                skill_code = skill_code.split("```")[1].split("```")[0].strip()
            
            # Validate
            if not self._validate_code(skill_code):
                print("❌ Generated skill has syntax errors")
                return False
            
            # Save skill
            skill_file = f"skill/{skill_name}.py"
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(skill_code)
            
            print(f"✅ New skill created: {skill_file}")
            print(f"💡 Restart JARVIS to load the new skill")
            
            return True
            
        except Exception as e:
            print(f"❌ Skill creation failed: {e}")
            return False
    
    def improve_code(self, file_path: str, improvement_goal: str) -> bool:
        """
        Improve existing code based on a goal
        """
        if not self.client:
            return False
        
        print(f"\n🤖 Improving code: {file_path}...")
        
        try:
            # Read current code
            with open(file_path, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            prompt = f"""Improve this Python code based on the goal.

IMPROVEMENT GOAL: {improvement_goal}

CURRENT CODE:
```python
{current_code}
```

Improve the code while:
1. Maintaining all existing functionality
2. Adding better error handling
3. Improving performance
4. Adding helpful comments
5. Following Python best practices

Return ONLY the improved Python code, no explanations.
"""

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python code optimizer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            improved_code = response['message']['content']
            
            # Clean up
            if "```python" in improved_code:
                improved_code = improved_code.split("```python")[1].split("```")[0].strip()
            elif "```" in improved_code:
                improved_code = improved_code.split("```")[1].split("```")[0].strip()
            
            # Validate
            if not self._validate_code(improved_code):
                print("❌ Improved code has syntax errors")
                return False
            
            # Apply improvement
            return self._apply_fix(file_path, improved_code)
            
        except Exception as e:
            print(f"❌ Code improvement failed: {e}")
            return False


# Global instance
advanced_self_coder = AdvancedSelfCoder()

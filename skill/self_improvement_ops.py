import json
import os
from typing import List, Dict, Any, Callable
from core.skill import Skill

class SelfImprovementSkill(Skill):
    """
    Skill that allows JARVIS to improve and modify its own code
    Commands like:
    - "Jarvis improve your code"
    - "Jarvis create a new skill for weather"
    - "Jarvis fix the error in engine.py"
    """
    
    @property
    def name(self) -> str:
        return "self_improvement_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "improve_own_code",
                    "description": "Improve JARVIS's own code for better performance, readability, or error handling",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to improve (e.g., 'core/engine.py', 'skill/web_ops.py')"
                            },
                            "improvement_type": {
                                "type": "string",
                                "description": "Type of improvement: 'performance', 'readability', 'error_handling', 'optimization'",
                                "default": "performance"
                            }
                        }, 
                        "required": ["file_path"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_new_skill",
                    "description": "Create a completely new skill for JARVIS with AI-generated code",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "skill_name": {
                                "type": "string",
                                "description": "Name of the new skill (e.g., 'weather', 'calculator', 'translator')"
                            },
                            "description": {
                                "type": "string",
                                "description": "What the skill should do (e.g., 'Get weather information for any city')"
                            },
                            "functions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of function names to implement (e.g., ['get_weather', 'get_forecast'])"
                            }
                        }, 
                        "required": ["skill_name", "description", "functions"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fix_code_error",
                    "description": "Automatically fix errors in JARVIS's code using AI",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file with error"
                            },
                            "error_description": {
                                "type": "string",
                                "description": "Description of the error to fix"
                            }
                        }, 
                        "required": ["file_path", "error_description"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_code_quality",
                    "description": "Analyze code quality and suggest improvements",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to analyze"
                            }
                        }, 
                        "required": ["file_path"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_improvement_history",
                    "description": "Get history of all code improvements made by JARVIS",
                    "parameters": { 
                        "type": "object", 
                        "properties": {}, 
                        "required": [] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "improve_own_code": self.improve_own_code,
            "create_new_skill": self.create_new_skill,
            "fix_code_error": self.fix_code_error,
            "analyze_code_quality": self.analyze_code_quality,
            "get_improvement_history": self.get_improvement_history
        }

    def improve_own_code(self, file_path: str, improvement_type: str = "performance"):
        """
        Improve JARVIS's own code using AI
        """
        try:
            from core.self_healing import self_healing
            
            print(f"\n🤖 JARVIS is improving its own code...")
            print(f"📁 File: {file_path}")
            print(f"🎯 Improvement: {improvement_type}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                return json.dumps({
                    "status": "error",
                    "error": f"File not found: {file_path}"
                })
            
            # Use AI to improve code
            success = self_healing.improve_code_with_ai(file_path, improvement_type)
            
            if success:
                return json.dumps({
                    "status": "success",
                    "action": "code_improved",
                    "file": file_path,
                    "improvement_type": improvement_type,
                    "message": "Code successfully improved! Restart JARVIS to apply changes."
                })
            else:
                return json.dumps({
                    "status": "error",
                    "error": "Could not improve code. Check if Advanced Self-Coder is available."
                })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def create_new_skill(self, skill_name: str, description: str, functions: List[str]):
        """
        Create a new skill using AI code generation
        """
        try:
            from core.self_healing import self_healing
            
            print(f"\n🤖 JARVIS is creating a new skill...")
            print(f"📝 Skill: {skill_name}")
            print(f"📋 Description: {description}")
            print(f"🔧 Functions: {', '.join(functions)}")
            
            # Use AI to create skill
            success = self_healing.create_skill_with_ai(skill_name, description, functions)
            
            if success:
                return json.dumps({
                    "status": "success",
                    "action": "skill_created",
                    "skill_name": skill_name,
                    "file": f"skill/{skill_name}_ops.py",
                    "message": f"New skill '{skill_name}' created! Restart JARVIS to use it."
                })
            else:
                return json.dumps({
                    "status": "error",
                    "error": "Could not create skill. Check if Advanced Self-Coder is available."
                })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def fix_code_error(self, file_path: str, error_description: str):
        """
        Fix code errors using AI
        """
        try:
            from core.self_healing import self_healing
            
            print(f"\n🤖 JARVIS is fixing code error...")
            print(f"📁 File: {file_path}")
            print(f"🐛 Error: {error_description}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                return json.dumps({
                    "status": "error",
                    "error": f"File not found: {file_path}"
                })
            
            # Create a mock error for AI to fix
            class MockError(Exception):
                pass
            
            error = MockError(error_description)
            
            # Use AI to fix
            if self_healing.advanced_coder:
                success = self_healing.advanced_coder.analyze_error_and_fix(
                    error, 
                    f"User reported error in {file_path}", 
                    file_path
                )
                
                if success:
                    return json.dumps({
                        "status": "success",
                        "action": "error_fixed",
                        "file": file_path,
                        "message": "Error fixed! Restart JARVIS to apply changes."
                    })
            
            return json.dumps({
                "status": "error",
                "error": "Could not fix error. Advanced Self-Coder not available."
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def analyze_code_quality(self, file_path: str):
        """
        Analyze code quality and provide suggestions
        """
        try:
            print(f"\n🤖 JARVIS is analyzing code quality...")
            print(f"📁 File: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                return json.dumps({
                    "status": "error",
                    "error": f"File not found: {file_path}"
                })
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Basic analysis
            lines = code.split('\n')
            total_lines = len(lines)
            code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            comment_lines = len([l for l in lines if l.strip().startswith('#')])
            blank_lines = total_lines - code_lines - comment_lines
            
            # Calculate metrics
            comment_ratio = (comment_lines / code_lines * 100) if code_lines > 0 else 0
            
            suggestions = []
            
            if comment_ratio < 10:
                suggestions.append("Add more comments to improve code readability")
            
            if total_lines > 500:
                suggestions.append("Consider splitting into smaller modules")
            
            # Check for common issues
            if 'except:' in code:
                suggestions.append("Avoid bare except clauses - specify exception types")
            
            if code.count('print(') > 20:
                suggestions.append("Consider using proper logging instead of print statements")
            
            analysis = {
                "status": "success",
                "file": file_path,
                "metrics": {
                    "total_lines": total_lines,
                    "code_lines": code_lines,
                    "comment_lines": comment_lines,
                    "blank_lines": blank_lines,
                    "comment_ratio": f"{comment_ratio:.1f}%"
                },
                "suggestions": suggestions if suggestions else ["Code looks good!"]
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def get_improvement_history(self):
        """
        Get history of all improvements made by JARVIS
        """
        try:
            from core.self_healing import self_healing
            
            if self_healing.advanced_coder:
                history = self_healing.advanced_coder.get_fix_history()
                return json.dumps({
                    "status": "success",
                    "history": history
                })
            else:
                return json.dumps({
                    "status": "info",
                    "message": "No improvement history available. Advanced Self-Coder not initialized."
                })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

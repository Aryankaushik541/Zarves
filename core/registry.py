import os
import importlib.util
import inspect
from typing import Dict, List, Any, Callable
from .skill import Skill

class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.tools_schema: List[Dict[str, Any]] = []
        self.functions: Dict[str, Callable] = {}

    def load_skills(self, skills_dir: str):
        """Dynamically load skills from the specified directory."""
        if not os.path.exists(skills_dir):
            print(f"Skills directory not found: {skills_dir}")
            return

        for filename in os.listdir(skills_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                file_path = os.path.join(skills_dir, filename)
                self._load_skill_from_file(module_name, file_path)

    def _load_skill_from_file(self, module_name: str, file_path: str):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Skill) and obj is not Skill:
                    try:
                        skill_instance = obj()
                        self.register_skill(skill_instance)
                        print(f"Loaded skill: {skill_instance.name}")
                    except Exception as e:
                        print(f"Failed to load skill {name}: {e}")

    def register_skill(self, skill: Skill):
        self.skills[skill.name] = skill
        self.tools_schema.extend(skill.get_tools())
        self.functions.update(skill.get_functions())

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get all tools schema for LLM function calling"""
        return self.tools_schema
    
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get all tools schema (alias for get_tools_schema for compatibility).
        This method is called by JarvisEngine.
        """
        return self.tools_schema

    def get_function(self, name: str) -> Callable:
        """Get a specific function by name"""
        return self.functions.get(name)
    
    def get_all_functions(self) -> Dict[str, Callable]:
        """Get all registered functions"""
        return self.functions
    
    def get_skill(self, name: str) -> Skill:
        """Get a specific skill by name"""
        return self.skills.get(name)
    
    def get_all_skills(self) -> Dict[str, Skill]:
        """Get all registered skills"""
        return self.skills
    
    def list_skills(self) -> List[str]:
        """List all skill names"""
        return list(self.skills.keys())
    
    def list_tools(self) -> List[str]:
        """List all tool names"""
        return [tool.get('function', {}).get('name', 'unknown') for tool in self.tools_schema]
    
    def execute_skill(self, function_name: str, function_args: Dict[str, Any] = None):
        """
        Execute a registered skill function by name with arguments.
        This method is used by the JarvisEngine and self-healing system.
        
        Args:
            function_name: Name of the function to execute (e.g., 'open_website', 'google_search')
            function_args: Dictionary of arguments to pass to the function (e.g., {'url': 'https://youtube.com'})
            
        Returns:
            Result from the executed function
            
        Raises:
            ValueError: If the skill function is not found in registry
        """
        if function_name not in self.functions:
            available_functions = ', '.join(self.functions.keys())
            raise ValueError(
                f"Skill function '{function_name}' not found in registry. "
                f"Available functions: {available_functions}"
            )
        
        try:
            function = self.functions[function_name]
            
            # Handle arguments - if None, use empty dict
            if function_args is None:
                function_args = {}
            
            # Call function with unpacked keyword arguments
            result = function(**function_args)
            return result
        except Exception as e:
            print(f"❌ Error executing skill '{function_name}': {e}")
            raise

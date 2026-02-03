#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autonomous Coding Skill for JARVIS
Integrates autonomous coder with JARVIS voice/text interface
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.autonomous_coder import AutonomousCoder
from core.skill import Skill


class AutonomousCodingSkill(Skill):
    """Autonomous coding skill for full-stack development"""
    
    def __init__(self):
        super().__init__(
            name="Autonomous Coding",
            description="Generate full-stack projects with AI and auto-debugging",
            version="1.0.0"
        )
        
        self.coder = AutonomousCoder()
        
        # Register tools
        self.register_tool(
            name="generate_react_app",
            description="Generate complete React application",
            function=self.generate_react_app
        )
        
        self.register_tool(
            name="generate_django_app",
            description="Generate complete Django application",
            function=self.generate_django_app
        )
        
        self.register_tool(
            name="generate_mern_app",
            description="Generate complete MERN stack application",
            function=self.generate_mern_app
        )
        
        self.register_tool(
            name="generate_android_app",
            description="Generate complete Android application",
            function=self.generate_android_app
        )
        
        self.register_tool(
            name="debug_project",
            description="Auto-debug existing project",
            function=self.debug_project
        )
    
    def generate_react_app(self, project_name: str, requirements: str, output_dir: str = None) -> str:
        """Generate React application"""
        try:
            result = self.coder.generate_fullstack_project(
                project_type='react',
                project_name=project_name,
                requirements=requirements,
                output_dir=output_dir
            )
            
            if result['success']:
                return f"""✅ React App Generated Successfully!

📦 Project: {project_name}
📁 Location: {result['output_dir']}
📄 Files: {result['files_generated']}
🔧 Debug Attempts: {result['debug_result']['attempts']}
✅ Errors Fixed: {len(result['debug_result']['errors_fixed'])}

🚀 To run:
cd {result['output_dir']}
npm start
"""
            else:
                return "❌ Failed to generate React app"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate_django_app(self, project_name: str, requirements: str, output_dir: str = None) -> str:
        """Generate Django application"""
        try:
            result = self.coder.generate_fullstack_project(
                project_type='django',
                project_name=project_name,
                requirements=requirements,
                output_dir=output_dir
            )
            
            if result['success']:
                return f"""✅ Django App Generated Successfully!

📦 Project: {project_name}
📁 Location: {result['output_dir']}
📄 Files: {result['files_generated']}
🔧 Debug Attempts: {result['debug_result']['attempts']}
✅ Errors Fixed: {len(result['debug_result']['errors_fixed'])}

🚀 To run:
cd {result['output_dir']}
python manage.py runserver
"""
            else:
                return "❌ Failed to generate Django app"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate_mern_app(self, project_name: str, requirements: str, output_dir: str = None) -> str:
        """Generate MERN stack application"""
        try:
            result = self.coder.generate_fullstack_project(
                project_type='mern',
                project_name=project_name,
                requirements=requirements,
                output_dir=output_dir
            )
            
            if result['success']:
                return f"""✅ MERN App Generated Successfully!

📦 Project: {project_name}
📁 Location: {result['output_dir']}
📄 Files: {result['files_generated']}
🔧 Debug Attempts: {result['debug_result']['attempts']}
✅ Errors Fixed: {len(result['debug_result']['errors_fixed'])}

🚀 To run:
cd {result['output_dir']}
npm run dev
"""
            else:
                return "❌ Failed to generate MERN app"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate_android_app(self, project_name: str, requirements: str, output_dir: str = None) -> str:
        """Generate Android application"""
        try:
            result = self.coder.generate_fullstack_project(
                project_type='android',
                project_name=project_name,
                requirements=requirements,
                output_dir=output_dir
            )
            
            if result['success']:
                return f"""✅ Android App Generated Successfully!

📦 Project: {project_name}
📁 Location: {result['output_dir']}
📄 Files: {result['files_generated']}
🔧 Debug Attempts: {result['debug_result']['attempts']}
✅ Errors Fixed: {len(result['debug_result']['errors_fixed'])}

🚀 To run:
Open in Android Studio: {result['output_dir']}
"""
            else:
                return "❌ Failed to generate Android app"
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def debug_project(self, project_dir: str, project_type: str) -> str:
        """Auto-debug existing project"""
        try:
            result = self.coder._test_and_debug(project_dir, project_type)
            
            return f"""🔧 Debug Complete!

🧪 Attempts: {result['attempts']}
✅ Errors Fixed: {len(result['errors_fixed'])}
{'✅ Success!' if result['success'] else '⚠️ Some errors remain'}

Fixed Errors:
{chr(10).join(['- ' + e[:100] for e in result['errors_fixed']])}
"""
        
        except Exception as e:
            return f"❌ Debug error: {str(e)}"


# Create skill instance
skill = AutonomousCodingSkill()

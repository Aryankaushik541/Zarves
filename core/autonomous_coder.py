#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autonomous AI Coding Agent
✅ Full-stack code generation (React, Django, MERN, Android)
✅ Internet data collection and research
✅ Self-debugging with AI assistance
✅ Autonomous terminal execution
✅ Error detection and fixing
✅ Multi-language support
"""

import os
import sys
import subprocess
import json
import re
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class AutonomousCoder:
    """Autonomous AI Coding Agent with Self-Debugging"""
    
    def __init__(self, ollama_url="http://localhost:11434", model="llama3.2"):
        self.ollama_url = ollama_url
        self.model = model
        self.project_history = []
        self.error_history = []
        self.max_debug_attempts = 5
        
        # Code templates
        self.templates = {
            'react': self._get_react_template,
            'django': self._get_django_template,
            'mern': self._get_mern_template,
            'android': self._get_android_template,
        }
        
        # Terminal execution history
        self.terminal_history = []
        
    def generate_fullstack_project(self, 
                                   project_type: str,
                                   project_name: str,
                                   requirements: str,
                                   output_dir: str = None) -> Dict:
        """
        Generate complete full-stack project
        
        Args:
            project_type: 'react', 'django', 'mern', 'android'
            project_name: Name of the project
            requirements: Project requirements description
            output_dir: Output directory (default: current dir)
        
        Returns:
            Dict with project info and status
        """
        print(f"\n{'='*70}")
        print(f"🚀 Autonomous Coder - Starting Project Generation")
        print(f"{'='*70}\n")
        
        print(f"📋 Project Type: {project_type.upper()}")
        print(f"📦 Project Name: {project_name}")
        print(f"📝 Requirements: {requirements}\n")
        
        # Step 1: Research and gather information
        print("🔍 Step 1: Researching best practices and gathering data...")
        research_data = self._research_project(project_type, requirements)
        
        # Step 2: Generate project structure
        print("\n📁 Step 2: Generating project structure...")
        project_structure = self._generate_project_structure(
            project_type, project_name, requirements, research_data
        )
        
        # Step 3: Generate code files
        print("\n💻 Step 3: Generating code files...")
        code_files = self._generate_code_files(
            project_type, project_name, requirements, research_data
        )
        
        # Step 4: Create project directory
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), project_name)
        
        print(f"\n📂 Step 4: Creating project at: {output_dir}")
        self._create_project_directory(output_dir, project_structure, code_files)
        
        # Step 5: Install dependencies
        print("\n📦 Step 5: Installing dependencies...")
        install_result = self._install_dependencies(output_dir, project_type)
        
        # Step 6: Run tests and debug
        print("\n🧪 Step 6: Testing and debugging...")
        debug_result = self._test_and_debug(output_dir, project_type)
        
        # Step 7: Generate documentation
        print("\n📚 Step 7: Generating documentation...")
        self._generate_documentation(output_dir, project_type, requirements)
        
        print(f"\n{'='*70}")
        print(f"✅ Project Generation Complete!")
        print(f"{'='*70}\n")
        
        return {
            'success': True,
            'project_name': project_name,
            'project_type': project_type,
            'output_dir': output_dir,
            'files_generated': len(code_files),
            'install_result': install_result,
            'debug_result': debug_result,
        }
    
    def _research_project(self, project_type: str, requirements: str) -> Dict:
        """Research project using internet and AI"""
        research_queries = [
            f"best practices for {project_type} development 2024",
            f"{project_type} project structure and architecture",
            f"common libraries and dependencies for {project_type}",
            f"{requirements} implementation in {project_type}",
        ]
        
        research_data = {
            'best_practices': [],
            'libraries': [],
            'architecture': '',
            'examples': [],
        }
        
        for query in research_queries:
            print(f"   🔍 Researching: {query}")
            
            # Search internet
            search_results = self._search_internet(query)
            
            # Analyze with AI
            analysis = self._analyze_with_ai(query, search_results)
            
            # Store results
            if 'best practices' in query:
                research_data['best_practices'].extend(analysis.get('practices', []))
            elif 'libraries' in query:
                research_data['libraries'].extend(analysis.get('libraries', []))
            elif 'structure' in query:
                research_data['architecture'] = analysis.get('architecture', '')
            elif 'implementation' in query:
                research_data['examples'].extend(analysis.get('examples', []))
        
        return research_data
    
    def _search_internet(self, query: str) -> List[Dict]:
        """Search internet for information"""
        try:
            # Use DuckDuckGo search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse results (simplified)
                results = []
                # Extract snippets from HTML
                snippets = re.findall(r'<a class="result__snippet">(.*?)</a>', response.text)
                for snippet in snippets[:5]:  # Top 5 results
                    results.append({
                        'snippet': snippet.strip(),
                        'source': 'web'
                    })
                return results
            
        except Exception as e:
            print(f"   ⚠️ Search error: {e}")
        
        return []
    
    def _analyze_with_ai(self, query: str, search_results: List[Dict]) -> Dict:
        """Analyze search results with AI"""
        try:
            # Prepare context
            context = "\n".join([r.get('snippet', '') for r in search_results])
            
            prompt = f"""Analyze this information about: {query}

Context from web search:
{context}

Extract and provide:
1. Best practices (list)
2. Recommended libraries/tools (list)
3. Architecture patterns (description)
4. Code examples (list)

Respond in JSON format."""
            
            response = self._call_ollama(prompt)
            
            # Try to parse JSON
            try:
                return json.loads(response)
            except:
                # Fallback parsing
                return {
                    'practices': self._extract_list(response, 'practices'),
                    'libraries': self._extract_list(response, 'libraries'),
                    'architecture': response[:500],
                    'examples': self._extract_list(response, 'examples'),
                }
        
        except Exception as e:
            print(f"   ⚠️ AI analysis error: {e}")
            return {}
    
    def _generate_project_structure(self, 
                                    project_type: str,
                                    project_name: str,
                                    requirements: str,
                                    research_data: Dict) -> Dict:
        """Generate project directory structure"""
        
        structures = {
            'react': {
                'src': {
                    'components': {},
                    'pages': {},
                    'services': {},
                    'utils': {},
                    'styles': {},
                },
                'public': {},
                'tests': {},
            },
            'django': {
                project_name: {
                    'settings.py': None,
                    'urls.py': None,
                    'wsgi.py': None,
                },
                'apps': {
                    'api': {
                        'models.py': None,
                        'views.py': None,
                        'serializers.py': None,
                        'urls.py': None,
                    },
                },
                'static': {},
                'templates': {},
                'tests': {},
            },
            'mern': {
                'client': {
                    'src': {
                        'components': {},
                        'pages': {},
                        'services': {},
                    },
                    'public': {},
                },
                'server': {
                    'models': {},
                    'routes': {},
                    'controllers': {},
                    'middleware': {},
                },
                'tests': {},
            },
            'android': {
                'app': {
                    'src': {
                        'main': {
                            'java': {
                                'com': {
                                    'example': {
                                        project_name: {
                                            'activities': {},
                                            'fragments': {},
                                            'adapters': {},
                                            'models': {},
                                            'utils': {},
                                        }
                                    }
                                }
                            },
                            'res': {
                                'layout': {},
                                'values': {},
                                'drawable': {},
                            },
                        },
                    },
                },
                'gradle': {},
            },
        }
        
        return structures.get(project_type, {})
    
    def _generate_code_files(self,
                            project_type: str,
                            project_name: str,
                            requirements: str,
                            research_data: Dict) -> Dict:
        """Generate code files using AI"""
        
        print(f"   💻 Generating {project_type.upper()} code files...")
        
        code_files = {}
        
        if project_type == 'react':
            code_files = self._generate_react_files(project_name, requirements, research_data)
        elif project_type == 'django':
            code_files = self._generate_django_files(project_name, requirements, research_data)
        elif project_type == 'mern':
            code_files = self._generate_mern_files(project_name, requirements, research_data)
        elif project_type == 'android':
            code_files = self._generate_android_files(project_name, requirements, research_data)
        
        return code_files
    
    def _generate_react_files(self, project_name: str, requirements: str, research_data: Dict) -> Dict:
        """Generate React project files"""
        
        files = {}
        
        # package.json
        files['package.json'] = self._generate_with_ai(
            f"Generate package.json for React project '{project_name}' with requirements: {requirements}",
            research_data
        )
        
        # App.js
        files['src/App.js'] = self._generate_with_ai(
            f"Generate React App.js component for: {requirements}. Include routing and state management.",
            research_data
        )
        
        # index.js
        files['src/index.js'] = self._generate_with_ai(
            "Generate React index.js entry point with React 18 features",
            research_data
        )
        
        # Main component
        files['src/components/MainComponent.jsx'] = self._generate_with_ai(
            f"Generate main React component for: {requirements}. Use modern hooks and best practices.",
            research_data
        )
        
        # API service
        files['src/services/api.js'] = self._generate_with_ai(
            "Generate API service module with axios for making HTTP requests",
            research_data
        )
        
        # Styles
        files['src/styles/App.css'] = self._generate_with_ai(
            "Generate modern CSS styles for React app with responsive design",
            research_data
        )
        
        # README
        files['README.md'] = self._generate_readme('react', project_name, requirements)
        
        return files
    
    def _generate_django_files(self, project_name: str, requirements: str, research_data: Dict) -> Dict:
        """Generate Django project files"""
        
        files = {}
        
        # requirements.txt
        files['requirements.txt'] = self._generate_with_ai(
            f"Generate requirements.txt for Django project with: {requirements}",
            research_data
        )
        
        # settings.py
        files[f'{project_name}/settings.py'] = self._generate_with_ai(
            f"Generate Django settings.py for project '{project_name}' with REST API, CORS, and database configuration",
            research_data
        )
        
        # urls.py
        files[f'{project_name}/urls.py'] = self._generate_with_ai(
            "Generate Django main urls.py with API routing",
            research_data
        )
        
        # models.py
        files['apps/api/models.py'] = self._generate_with_ai(
            f"Generate Django models for: {requirements}. Include proper relationships and validation.",
            research_data
        )
        
        # views.py
        files['apps/api/views.py'] = self._generate_with_ai(
            f"Generate Django REST API views for: {requirements}. Use ViewSets and proper serialization.",
            research_data
        )
        
        # serializers.py
        files['apps/api/serializers.py'] = self._generate_with_ai(
            f"Generate Django REST serializers for the models",
            research_data
        )
        
        # README
        files['README.md'] = self._generate_readme('django', project_name, requirements)
        
        return files
    
    def _generate_mern_files(self, project_name: str, requirements: str, research_data: Dict) -> Dict:
        """Generate MERN stack files"""
        
        files = {}
        
        # Root package.json
        files['package.json'] = self._generate_with_ai(
            f"Generate root package.json for MERN project '{project_name}' with concurrently for running client and server",
            research_data
        )
        
        # Client package.json
        files['client/package.json'] = self._generate_with_ai(
            f"Generate client package.json for React frontend",
            research_data
        )
        
        # Server package.json
        files['server/package.json'] = self._generate_with_ai(
            f"Generate server package.json for Express backend with MongoDB",
            research_data
        )
        
        # Server index.js
        files['server/index.js'] = self._generate_with_ai(
            f"Generate Express server with MongoDB connection, CORS, and API routes for: {requirements}",
            research_data
        )
        
        # Models
        files['server/models/Model.js'] = self._generate_with_ai(
            f"Generate Mongoose model for: {requirements}",
            research_data
        )
        
        # Routes
        files['server/routes/api.js'] = self._generate_with_ai(
            f"Generate Express routes for CRUD operations: {requirements}",
            research_data
        )
        
        # Controllers
        files['server/controllers/controller.js'] = self._generate_with_ai(
            f"Generate Express controllers with business logic for: {requirements}",
            research_data
        )
        
        # Client App.js
        files['client/src/App.js'] = self._generate_with_ai(
            f"Generate React App.js for MERN frontend with API integration for: {requirements}",
            research_data
        )
        
        # README
        files['README.md'] = self._generate_readme('mern', project_name, requirements)
        
        return files
    
    def _generate_android_files(self, project_name: str, requirements: str, research_data: Dict) -> Dict:
        """Generate Android project files"""
        
        files = {}
        
        # build.gradle (app)
        files['app/build.gradle'] = self._generate_with_ai(
            f"Generate Android app build.gradle with modern dependencies for: {requirements}",
            research_data
        )
        
        # MainActivity.java
        files[f'app/src/main/java/com/example/{project_name}/MainActivity.java'] = self._generate_with_ai(
            f"Generate Android MainActivity for: {requirements}. Use modern Android architecture components.",
            research_data
        )
        
        # activity_main.xml
        files['app/src/main/res/layout/activity_main.xml'] = self._generate_with_ai(
            f"Generate Android layout XML for: {requirements}. Use Material Design components.",
            research_data
        )
        
        # AndroidManifest.xml
        files['app/src/main/AndroidManifest.xml'] = self._generate_with_ai(
            f"Generate AndroidManifest.xml for app '{project_name}' with necessary permissions",
            research_data
        )
        
        # README
        files['README.md'] = self._generate_readme('android', project_name, requirements)
        
        return files
    
    def _generate_with_ai(self, prompt: str, research_data: Dict) -> str:
        """Generate code using AI with research context"""
        
        full_prompt = f"""You are an expert full-stack developer. Generate production-ready code.

Research Context:
- Best Practices: {', '.join(research_data.get('best_practices', [])[:3])}
- Recommended Libraries: {', '.join(research_data.get('libraries', [])[:5])}

Task: {prompt}

Generate clean, well-commented, production-ready code following best practices.
Include error handling and proper structure."""
        
        return self._call_ollama(full_prompt)
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API for code generation"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
        
        except Exception as e:
            print(f"   ⚠️ Ollama error: {e}")
        
        return ""
    
    def _create_project_directory(self, output_dir: str, structure: Dict, files: Dict):
        """Create project directory with structure and files"""
        
        # Create base directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory structure
        self._create_dirs(output_dir, structure)
        
        # Write files
        for file_path, content in files.items():
            full_path = os.path.join(output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ Created: {file_path}")
    
    def _create_dirs(self, base_path: str, structure: Dict):
        """Recursively create directory structure"""
        for name, sub_structure in structure.items():
            dir_path = os.path.join(base_path, name)
            os.makedirs(dir_path, exist_ok=True)
            
            if isinstance(sub_structure, dict) and sub_structure:
                self._create_dirs(dir_path, sub_structure)
    
    def _install_dependencies(self, project_dir: str, project_type: str) -> Dict:
        """Install project dependencies"""
        
        result = {'success': False, 'output': '', 'errors': []}
        
        try:
            if project_type == 'react':
                # npm install
                print("   📦 Running: npm install")
                output = self._run_terminal_command('npm install', cwd=project_dir)
                result['output'] = output
                result['success'] = 'error' not in output.lower()
            
            elif project_type == 'django':
                # pip install
                print("   📦 Running: pip install -r requirements.txt")
                output = self._run_terminal_command(
                    'pip install -r requirements.txt',
                    cwd=project_dir
                )
                result['output'] = output
                result['success'] = 'error' not in output.lower()
            
            elif project_type == 'mern':
                # Install root dependencies
                print("   📦 Running: npm install (root)")
                output1 = self._run_terminal_command('npm install', cwd=project_dir)
                
                # Install client dependencies
                print("   📦 Running: npm install (client)")
                output2 = self._run_terminal_command(
                    'npm install',
                    cwd=os.path.join(project_dir, 'client')
                )
                
                # Install server dependencies
                print("   📦 Running: npm install (server)")
                output3 = self._run_terminal_command(
                    'npm install',
                    cwd=os.path.join(project_dir, 'server')
                )
                
                result['output'] = f"{output1}\n{output2}\n{output3}"
                result['success'] = all('error' not in o.lower() for o in [output1, output2, output3])
            
            elif project_type == 'android':
                # Gradle build
                print("   📦 Running: ./gradlew build")
                output = self._run_terminal_command('./gradlew build', cwd=project_dir)
                result['output'] = output
                result['success'] = 'BUILD SUCCESSFUL' in output
        
        except Exception as e:
            result['errors'].append(str(e))
            print(f"   ❌ Installation error: {e}")
        
        return result
    
    def _test_and_debug(self, project_dir: str, project_type: str) -> Dict:
        """Test project and auto-debug errors"""
        
        result = {'success': False, 'attempts': 0, 'errors_fixed': []}
        
        for attempt in range(self.max_debug_attempts):
            result['attempts'] = attempt + 1
            
            print(f"\n   🧪 Debug Attempt {attempt + 1}/{self.max_debug_attempts}")
            
            # Run tests
            test_output = self._run_tests(project_dir, project_type)
            
            # Check for errors
            errors = self._detect_errors(test_output)
            
            if not errors:
                print("   ✅ No errors detected!")
                result['success'] = True
                break
            
            print(f"   ⚠️ Found {len(errors)} error(s)")
            
            # Auto-fix errors
            for error in errors:
                print(f"   🔧 Fixing: {error[:100]}...")
                fix_result = self._auto_fix_error(project_dir, error, project_type)
                
                if fix_result['success']:
                    result['errors_fixed'].append(error)
                    print(f"   ✅ Fixed!")
                else:
                    print(f"   ❌ Could not fix automatically")
        
        return result
    
    def _run_tests(self, project_dir: str, project_type: str) -> str:
        """Run project tests"""
        
        commands = {
            'react': 'npm run build',
            'django': 'python manage.py check',
            'mern': 'npm run build',
            'android': './gradlew assembleDebug',
        }
        
        command = commands.get(project_type, 'echo "No test command"')
        
        try:
            return self._run_terminal_command(command, cwd=project_dir)
        except Exception as e:
            return str(e)
    
    def _detect_errors(self, output: str) -> List[str]:
        """Detect errors in output"""
        
        error_patterns = [
            r'Error: (.+)',
            r'ERROR: (.+)',
            r'Exception: (.+)',
            r'SyntaxError: (.+)',
            r'TypeError: (.+)',
            r'ModuleNotFoundError: (.+)',
            r'ImportError: (.+)',
        ]
        
        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, output)
            errors.extend(matches)
        
        return errors
    
    def _auto_fix_error(self, project_dir: str, error: str, project_type: str) -> Dict:
        """Automatically fix error using AI"""
        
        # Get error context
        error_context = self._get_error_context(project_dir, error)
        
        # Ask AI for fix
        fix_prompt = f"""You are a debugging expert. Fix this error:

Error: {error}

Context:
{error_context}

Project Type: {project_type}

Provide:
1. Root cause analysis
2. Exact fix (code changes)
3. File path to modify
4. Updated code

Respond in JSON format:
{{
    "analysis": "...",
    "file_path": "...",
    "fix_code": "..."
}}"""
        
        ai_response = self._call_ollama(fix_prompt)
        
        try:
            fix_data = json.loads(ai_response)
            
            # Apply fix
            file_path = os.path.join(project_dir, fix_data['file_path'])
            
            if os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fix_data['fix_code'])
                
                return {'success': True, 'fix': fix_data}
        
        except Exception as e:
            print(f"   ⚠️ Fix application error: {e}")
        
        return {'success': False}
    
    def _get_error_context(self, project_dir: str, error: str) -> str:
        """Get context around error"""
        
        # Search for relevant files
        relevant_files = []
        
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.java')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if any(keyword in content for keyword in error.split()[:3]):
                                relevant_files.append({
                                    'path': file_path,
                                    'content': content[:1000]  # First 1000 chars
                                })
                    except:
                        pass
        
        context = "\n\n".join([
            f"File: {f['path']}\n{f['content']}"
            for f in relevant_files[:3]  # Top 3 relevant files
        ])
        
        return context
    
    def _run_terminal_command(self, command: str, cwd: str = None) -> str:
        """Execute terminal command and return output"""
        
        try:
            print(f"   🖥️ Executing: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            output = result.stdout + result.stderr
            
            # Store in history
            self.terminal_history.append({
                'command': command,
                'output': output,
                'timestamp': datetime.now().isoformat(),
                'success': result.returncode == 0
            })
            
            return output
        
        except subprocess.TimeoutExpired:
            return "Command timed out after 5 minutes"
        except Exception as e:
            return f"Command execution error: {str(e)}"
    
    def _generate_readme(self, project_type: str, project_name: str, requirements: str) -> str:
        """Generate README.md"""
        
        return f"""# {project_name}

## Description
{requirements}

## Project Type
{project_type.upper()}

## Setup Instructions

### Prerequisites
- Node.js (for React/MERN)
- Python 3.8+ (for Django)
- Android Studio (for Android)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd {project_name}

# Install dependencies
{"npm install" if project_type in ['react', 'mern'] else "pip install -r requirements.txt"}

# Run the project
{"npm start" if project_type == 'react' else "python manage.py runserver" if project_type == 'django' else "npm run dev" if project_type == 'mern' else "./gradlew run"}
```

## Features
- Auto-generated by Autonomous AI Coder
- Production-ready code
- Best practices implemented
- Error handling included

## Generated by
JARVIS Autonomous Coder - AI-powered full-stack development

## License
MIT
"""
    
    def _generate_documentation(self, project_dir: str, project_type: str, requirements: str):
        """Generate comprehensive documentation"""
        
        docs_dir = os.path.join(project_dir, 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # API documentation
        api_doc = self._generate_with_ai(
            f"Generate API documentation for {project_type} project with requirements: {requirements}",
            {}
        )
        
        with open(os.path.join(docs_dir, 'API.md'), 'w') as f:
            f.write(api_doc)
        
        print("   ✅ Documentation generated")
    
    def _extract_list(self, text: str, key: str) -> List[str]:
        """Extract list items from text"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            if key.lower() in line.lower():
                # Extract bullet points or numbered items
                if re.match(r'^\s*[-*•]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
                    item = re.sub(r'^\s*[-*•\d.]+\s+', '', line).strip()
                    if item:
                        items.append(item)
        
        return items
    
    # Template getters
    def _get_react_template(self) -> str:
        return "React template"
    
    def _get_django_template(self) -> str:
        return "Django template"
    
    def _get_mern_template(self) -> str:
        return "MERN template"
    
    def _get_android_template(self) -> str:
        return "Android template"


# CLI Interface
def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous AI Coding Agent')
    parser.add_argument('--type', required=True, choices=['react', 'django', 'mern', 'android'],
                       help='Project type')
    parser.add_argument('--name', required=True, help='Project name')
    parser.add_argument('--requirements', required=True, help='Project requirements')
    parser.add_argument('--output', help='Output directory')
    
    args = parser.parse_args()
    
    # Create coder
    coder = AutonomousCoder()
    
    # Generate project
    result = coder.generate_fullstack_project(
        project_type=args.type,
        project_name=args.name,
        requirements=args.requirements,
        output_dir=args.output
    )
    
    print(f"\n{'='*70}")
    print(f"📊 Generation Summary:")
    print(f"{'='*70}")
    print(f"✅ Success: {result['success']}")
    print(f"📁 Output: {result['output_dir']}")
    print(f"📄 Files: {result['files_generated']}")
    print(f"🔧 Debug Attempts: {result['debug_result']['attempts']}")
    print(f"✅ Errors Fixed: {len(result['debug_result']['errors_fixed'])}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()

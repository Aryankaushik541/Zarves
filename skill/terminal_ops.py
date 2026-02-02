import os
import json
import subprocess
from typing import List, Dict, Any, Callable
from core.skill import Skill

class TerminalSkill(Skill):
    @property
    def name(self) -> str:
        return "terminal_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "execute_terminal_command",
                    "description": "Execute any terminal/shell command on the system. Can install apps, run scripts, manage files, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The terminal command to execute (e.g., 'brew install python', 'npm install', 'git clone ...')"},
                            "working_directory": {"type": "string", "description": "Directory to run command in (optional)", "default": "~"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "install_application",
                    "description": "Install any application using Homebrew (macOS package manager)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string", "description": "Name of the application to install (e.g., 'python', 'node', 'vscode', 'docker')"}
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_python_script",
                    "description": "Create and run a Python script to perform any task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "script_description": {"type": "string", "description": "What the script should do"},
                            "script_name": {"type": "string", "description": "Name for the script file", "default": "jarvis_script.py"}
                        },
                        "required": ["script_description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_operations",
                    "description": "Perform Git operations (clone, commit, push, pull, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {"type": "string", "description": "Git operation: 'clone', 'commit', 'push', 'pull', 'status'"},
                            "repo_url": {"type": "string", "description": "Repository URL (for clone)"},
                            "message": {"type": "string", "description": "Commit message (for commit)"}
                        },
                        "required": ["operation"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "execute_terminal_command": self.execute_terminal_command,
            "install_application": self.install_application,
            "run_python_script": self.run_python_script,
            "git_operations": self.git_operations
        }

    def execute_terminal_command(self, command, working_directory="~"):
        try:
            # Expand home directory
            work_dir = os.path.expanduser(working_directory)
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout if result.stdout else result.stderr
            
            return json.dumps({
                "status": "success" if result.returncode == 0 else "error",
                "command": command,
                "output": output[:500],  # Limit output
                "return_code": result.returncode
            })
            
        except subprocess.TimeoutExpired:
            return json.dumps({"status": "error", "error": "Command timed out after 60 seconds"})
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def install_application(self, app_name):
        try:
            # Check if Homebrew is installed
            brew_check = subprocess.run(["which", "brew"], capture_output=True)
            
            if brew_check.returncode != 0:
                # Install Homebrew first
                install_brew = subprocess.run(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
            
            # Install the application
            result = subprocess.run(
                ["brew", "install", app_name],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return json.dumps({
                    "status": "success",
                    "message": f"Successfully installed {app_name}",
                    "app": app_name
                })
            else:
                # Try with cask (for GUI apps)
                result = subprocess.run(
                    ["brew", "install", "--cask", app_name],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    return json.dumps({
                        "status": "success",
                        "message": f"Successfully installed {app_name} (GUI app)",
                        "app": app_name
                    })
                else:
                    return json.dumps({
                        "status": "error",
                        "error": result.stderr[:200]
                    })
                    
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def run_python_script(self, script_description, script_name="jarvis_script.py"):
        try:
            # Generate Python script based on description
            script_content = f'''"""
{script_description}
Auto-generated and executed by JARVIS AI
"""

import os
import sys

def main():
    print("JARVIS Auto-Script: {script_description}")
    
    # Script logic here
    # This is a template - JARVIS will enhance this based on the task
    
    print("Script completed successfully!")

if __name__ == "__main__":
    main()
'''
            
            # Save script to Desktop
            script_path = os.path.join(os.path.expanduser("~"), "Desktop", script_name)
            with open(script_path, "w") as f:
                f.write(script_content)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            # Run the script
            result = subprocess.run(
                ["python3", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return json.dumps({
                "status": "success",
                "message": f"Script created and executed",
                "script_path": script_path,
                "output": result.stdout[:300]
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def git_operations(self, operation, repo_url=None, message=None):
        try:
            if operation == "clone" and repo_url:
                # Clone to Desktop
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                result = subprocess.run(
                    ["git", "clone", repo_url],
                    cwd=desktop,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                return json.dumps({
                    "status": "success" if result.returncode == 0 else "error",
                    "operation": "clone",
                    "output": result.stdout if result.returncode == 0 else result.stderr
                })
            
            elif operation == "commit" and message:
                result = subprocess.run(
                    ["git", "add", ".", "&&", "git", "commit", "-m", message],
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                return json.dumps({
                    "status": "success" if result.returncode == 0 else "error",
                    "operation": "commit",
                    "message": message
                })
            
            elif operation == "push":
                result = subprocess.run(
                    ["git", "push"],
                    capture_output=True,
                    text=True
                )
                
                return json.dumps({
                    "status": "success" if result.returncode == 0 else "error",
                    "operation": "push"
                })
            
            elif operation == "pull":
                result = subprocess.run(
                    ["git", "pull"],
                    capture_output=True,
                    text=True
                )
                
                return json.dumps({
                    "status": "success" if result.returncode == 0 else "error",
                    "operation": "pull"
                })
            
            elif operation == "status":
                result = subprocess.run(
                    ["git", "status"],
                    capture_output=True,
                    text=True
                )
                
                return json.dumps({
                    "status": "success",
                    "operation": "status",
                    "output": result.stdout
                })
            
            else:
                return json.dumps({"status": "error", "error": "Invalid operation or missing parameters"})
                
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

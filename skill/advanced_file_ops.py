import os
import json
import shutil
from typing import List, Dict, Any, Callable
from core.skill import Skill

class AdvancedFileSkill(Skill):
    @property
    def name(self) -> str:
        return "advanced_file_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_project_structure",
                    "description": "Create a complete project folder structure with multiple files and directories",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project_name": {"type": "string", "description": "Name of the project"},
                            "project_type": {"type": "string", "description": "Type: 'web', 'python', 'mobile', 'data-science', 'game'"}
                        },
                        "required": ["project_name", "project_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "batch_file_operations",
                    "description": "Perform batch operations on multiple files (rename, move, copy, delete)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {"type": "string", "description": "'rename', 'move', 'copy', 'delete'"},
                            "pattern": {"type": "string", "description": "File pattern to match (e.g., '*.txt', '*.jpg')"},
                            "source_dir": {"type": "string", "description": "Source directory"},
                            "destination_dir": {"type": "string", "description": "Destination directory (for move/copy)"}
                        },
                        "required": ["operation", "pattern", "source_dir"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "organize_downloads",
                    "description": "Automatically organize Downloads folder by file type",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "create_folders": {"type": "boolean", "description": "Create category folders", "default": True}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file_with_content",
                    "description": "Create any file with specific content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string", "description": "Full path where file should be created"},
                            "content": {"type": "string", "description": "Content to write to the file"}
                        },
                        "required": ["filepath", "content"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "create_project_structure": self.create_project_structure,
            "batch_file_operations": self.batch_file_operations,
            "organize_downloads": self.organize_downloads,
            "create_file_with_content": self.create_file_with_content
        }

    def create_project_structure(self, project_name, project_type):
        try:
            base_path = os.path.join(os.path.expanduser("~"), "Desktop", project_name)
            os.makedirs(base_path, exist_ok=True)
            
            structures = {
                "web": {
                    "folders": ["src", "src/css", "src/js", "src/images", "public", "tests"],
                    "files": {
                        "src/index.html": "<!DOCTYPE html>\n<html>\n<head>\n    <title>{}</title>\n    <link rel='stylesheet' href='css/style.css'>\n</head>\n<body>\n    <h1>Welcome to {}</h1>\n    <script src='js/app.js'></script>\n</body>\n</html>".format(project_name, project_name),
                        "src/css/style.css": "/* Styles for {} */\nbody {{ font-family: Arial, sans-serif; }}".format(project_name),
                        "src/js/app.js": "// JavaScript for {}\nconsole.log('App initialized');".format(project_name),
                        "README.md": "# {}\n\nAuto-generated web project by JARVIS AI".format(project_name)
                    }
                },
                "python": {
                    "folders": ["src", "tests", "docs", "data"],
                    "files": {
                        "src/__init__.py": "",
                        "src/main.py": "#!/usr/bin/env python3\n\"\"\"{}\"\"\"\n\ndef main():\n    print('Hello from {}')\n\nif __name__ == '__main__':\n    main()".format(project_name, project_name),
                        "tests/__init__.py": "",
                        "requirements.txt": "# Dependencies for {}\n".format(project_name),
                        "README.md": "# {}\n\nAuto-generated Python project by JARVIS AI".format(project_name),
                        ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/"
                    }
                },
                "data-science": {
                    "folders": ["data", "notebooks", "src", "models", "reports"],
                    "files": {
                        "notebooks/analysis.ipynb": "{}",
                        "src/__init__.py": "",
                        "requirements.txt": "pandas\nnumpy\nmatplotlib\nseaborn\nscikit-learn\njupyter",
                        "README.md": "# {} - Data Science Project\n\nAuto-generated by JARVIS AI".format(project_name)
                    }
                }
            }
            
            structure = structures.get(project_type, structures["python"])
            
            # Create folders
            for folder in structure["folders"]:
                os.makedirs(os.path.join(base_path, folder), exist_ok=True)
            
            # Create files
            for filepath, content in structure["files"].items():
                full_path = os.path.join(base_path, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
            
            # Open in Finder
            os.system(f"open '{base_path}'")
            
            return json.dumps({
                "status": "success",
                "message": f"{project_type.title()} project '{project_name}' created successfully!",
                "path": base_path,
                "folders": len(structure["folders"]),
                "files": len(structure["files"])
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def batch_file_operations(self, operation, pattern, source_dir, destination_dir=None):
        try:
            import glob
            
            source_path = os.path.expanduser(source_dir)
            files = glob.glob(os.path.join(source_path, pattern))
            
            count = 0
            for file in files:
                if operation == "delete":
                    os.remove(file)
                    count += 1
                elif operation == "move" and destination_dir:
                    dest_path = os.path.expanduser(destination_dir)
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.move(file, os.path.join(dest_path, os.path.basename(file)))
                    count += 1
                elif operation == "copy" and destination_dir:
                    dest_path = os.path.expanduser(destination_dir)
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.copy2(file, os.path.join(dest_path, os.path.basename(file)))
                    count += 1
            
            return json.dumps({
                "status": "success",
                "operation": operation,
                "files_processed": count,
                "pattern": pattern
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def organize_downloads(self, create_folders=True):
        try:
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            
            categories = {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
                "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
                "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
                "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
                "Spreadsheets": [".xlsx", ".xls", ".csv"],
                "Presentations": [".ppt", ".pptx"]
            }
            
            moved_files = {}
            
            for filename in os.listdir(downloads_path):
                filepath = os.path.join(downloads_path, filename)
                
                if os.path.isfile(filepath):
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    for category, extensions in categories.items():
                        if file_ext in extensions:
                            category_path = os.path.join(downloads_path, category)
                            
                            if create_folders:
                                os.makedirs(category_path, exist_ok=True)
                                shutil.move(filepath, os.path.join(category_path, filename))
                                
                                if category not in moved_files:
                                    moved_files[category] = 0
                                moved_files[category] += 1
                            break
            
            return json.dumps({
                "status": "success",
                "message": "Downloads folder organized!",
                "categories": moved_files,
                "total_files": sum(moved_files.values())
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

    def create_file_with_content(self, filepath, content):
        try:
            full_path = os.path.expanduser(filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w") as f:
                f.write(content)
            
            # Open the file
            os.system(f"open '{full_path}'")
            
            return json.dumps({
                "status": "success",
                "message": f"File created: {os.path.basename(filepath)}",
                "path": full_path
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})

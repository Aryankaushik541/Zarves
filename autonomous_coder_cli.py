#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autonomous AI Coder - CLI Interface
Generate full-stack projects with AI assistance
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.autonomous_coder import AutonomousCoder


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🤖 JARVIS Autonomous AI Coder")
    print("="*70)
    print("Generate full-stack projects with AI and auto-debugging")
    print("="*70 + "\n")


def print_menu():
    """Print main menu"""
    print("\n📋 Select Project Type:")
    print("1. React Application")
    print("2. Django Application")
    print("3. MERN Stack Application")
    print("4. Android Application")
    print("5. Exit")
    print()


def get_project_details():
    """Get project details from user"""
    print("\n📝 Project Details:")
    print("-" * 70)
    
    project_name = input("Project Name: ").strip()
    if not project_name:
        print("❌ Project name cannot be empty!")
        return None
    
    requirements = input("Requirements (describe what you want): ").strip()
    if not requirements:
        print("❌ Requirements cannot be empty!")
        return None
    
    output_dir = input("Output Directory (press Enter for current dir): ").strip()
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), project_name)
    
    return {
        'project_name': project_name,
        'requirements': requirements,
        'output_dir': output_dir
    }


def main():
    """Main CLI interface"""
    print_banner()
    
    # Check Ollama
    print("🔍 Checking Ollama...")
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            print("✅ Ollama is running!\n")
        else:
            print("⚠️ Ollama not responding. Make sure it's running: ollama serve\n")
    except:
        print("❌ Ollama not found! Please start Ollama: ollama serve\n")
        sys.exit(1)
    
    # Create coder instance
    coder = AutonomousCoder()
    
    while True:
        print_menu()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '5':
            print("\n👋 Goodbye!\n")
            break
        
        project_types = {
            '1': 'react',
            '2': 'django',
            '3': 'mern',
            '4': 'android'
        }
        
        if choice not in project_types:
            print("❌ Invalid choice! Please select 1-5.")
            continue
        
        project_type = project_types[choice]
        
        # Get project details
        details = get_project_details()
        if not details:
            continue
        
        # Confirm
        print("\n" + "="*70)
        print("📊 Project Summary:")
        print("="*70)
        print(f"Type: {project_type.upper()}")
        print(f"Name: {details['project_name']}")
        print(f"Requirements: {details['requirements']}")
        print(f"Output: {details['output_dir']}")
        print("="*70)
        
        confirm = input("\n🚀 Generate project? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Cancelled!")
            continue
        
        # Generate project
        try:
            result = coder.generate_fullstack_project(
                project_type=project_type,
                project_name=details['project_name'],
                requirements=details['requirements'],
                output_dir=details['output_dir']
            )
            
            if result['success']:
                print("\n" + "="*70)
                print("🎉 SUCCESS!")
                print("="*70)
                print(f"✅ Project generated: {result['output_dir']}")
                print(f"📄 Files created: {result['files_generated']}")
                print(f"🔧 Debug attempts: {result['debug_result']['attempts']}")
                print(f"✅ Errors fixed: {len(result['debug_result']['errors_fixed'])}")
                print("="*70)
                
                # Show next steps
                print("\n📚 Next Steps:")
                print("-" * 70)
                print(f"1. cd {result['output_dir']}")
                
                if project_type == 'react':
                    print("2. npm start")
                elif project_type == 'django':
                    print("2. python manage.py runserver")
                elif project_type == 'mern':
                    print("2. npm run dev")
                elif project_type == 'android':
                    print("2. Open in Android Studio")
                
                print("-" * 70 + "\n")
            else:
                print("\n❌ Project generation failed!")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
        sys.exit(0)

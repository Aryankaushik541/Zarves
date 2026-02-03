#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autonomous AI Coder - CLI Interface V2
Generate full-stack projects with AI assistance
✅ Improved timeout handling
✅ Fallback templates
✅ Faster generation
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.autonomous_coder_v2 import AutonomousCoderV2


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🤖 JARVIS Autonomous AI Coder V2")
    print("="*70)
    print("Generate full-stack projects with AI and fallback templates")
    print("✅ Faster generation | ✅ Better timeout handling | ✅ More reliable")
    print("="*70 + "\n")


def print_menu():
    """Print main menu"""
    print("\n📋 Select Project Type:")
    print("1. React Application (2-3 min)")
    print("2. Django Application (3-4 min)")
    print("3. MERN Stack Application (4-5 min)")
    print("4. Android Application (5-6 min)")
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
            print("✅ Ollama is running!")
            print("ℹ️  Note: If Ollama is slow, fallback templates will be used\n")
        else:
            print("⚠️ Ollama not responding. Using fallback templates only.\n")
    except:
        print("⚠️ Ollama not found. Using fallback templates only.")
        print("ℹ️  Projects will still be generated successfully!\n")
    
    # Create coder instance
    coder = AutonomousCoderV2()
    
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
                print("="*70)
                
                # Show next steps
                print("\n📚 Next Steps:")
                print("-" * 70)
                print(f"1. cd {result['output_dir']}")
                
                if project_type == 'react':
                    print("2. npm install")
                    print("3. npm start")
                    print("\n🌐 App will open at: http://localhost:3000")
                elif project_type == 'django':
                    print("2. pip install -r requirements.txt")
                    print("3. python manage.py migrate")
                    print("4. python manage.py createsuperuser")
                    print("5. python manage.py runserver")
                    print("\n🌐 API will run at: http://localhost:8000")
                elif project_type == 'mern':
                    print("2. npm install")
                    print("3. cd client && npm install")
                    print("4. cd ../server && npm install")
                    print("5. cd .. && npm run dev")
                    print("\n🌐 Client: http://localhost:3000")
                    print("🌐 Server: http://localhost:5000")
                elif project_type == 'android':
                    print("2. Open in Android Studio")
                    print("3. Sync Gradle")
                    print("4. Run on emulator or device")
                
                print("-" * 70 + "\n")
            else:
                print("\n❌ Project generation failed!")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("\nℹ️  Tip: Make sure Ollama is running or fallback templates will be used")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
        sys.exit(0)

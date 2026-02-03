#!/usr/bin/env python3
"""
Script to remove all GROQ references from main.py
Run this to update your local main.py file
"""

import re

def fix_main_py():
    """Remove all GROQ references from main.py"""
    
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all GROQ_API_KEY references
    replacements = [
        # In auto_create_env_file function
        (r'print\("⚠️  Please add your GROQ_API_KEY to .env file"\)', 
         'print("⚠️  Please configure Ollama settings in .env file (optional)")'),
        (r'print\("   Get free key from: https://console\.groq\.com/keys"\)',
         'print("   See OLLAMA_SETUP.md for configuration")'),
        
        # In run_startup_tests function - Test 7
        (r'groq_key = os\.environ\.get\("GROQ_API_KEY"\)',
         'ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")'),
        (r'if groq_key:',
         'if ollama_host:'),
        (r'print\(f"✅ GROQ_API_KEY found \(length: \{len\(groq_key\)\}\)"\)',
         'print(f"✅ Ollama host configured: {ollama_host}")'),
        (r'print\("❌ GROQ_API_KEY not found"\)',
         'print("ℹ️  Using default Ollama host: http://localhost:11434")'),
        (r'print\("⚠️  IMPORTANT: Add your GROQ_API_KEY to \.env file"\)',
         'print("💡 Optional: Configure OLLAMA_HOST in .env file")'),
        (r'print\("   Get free key from: https://console\.groq\.com/keys"\)',
         'print("   Default: http://localhost:11434")'),
        (r'print\("⚠️  \.env file exists but GROQ_API_KEY is missing"\)',
         'print("ℹ️  .env file exists - Ollama will use default settings")'),
        (r'print\("   Add: GROQ_API_KEY=your_key_here"\)',
         'print("   Optional: Add OLLAMA_HOST=http://localhost:11434")'),
        (r'if not groq_key:',
         'if False:  # Ollama doesn\'t require API key'),
        (r'print\("   • GROQ_API_KEY missing - Please add to \.env file"\)',
         ''),
        
        # In main function
        (r'if not os\.environ\.get\("GROQ_API_KEY"\):',
         'if False:  # Ollama check disabled - no API key needed'),
        (r'print\("⚠️  CRITICAL: GROQ_API_KEY is required to run JARVIS"\)',
         'print("⚠️  CRITICAL: Ollama is required to run JARVIS")'),
        (r'print\("   1\. Get free key from: https://console\.groq\.com/keys"\)',
         'print("   1. Install Ollama: https://ollama.com/download")'),
        (r'print\("   2\. Add to \.env file: GROQ_API_KEY=your_key_here"\)',
         'print("   2. Start Ollama: ollama serve")'),
        (r'print\("   3\. Restart: python main\.py"\)',
         'print("   3. Pull model: ollama pull llama3.2")'),
        
        # After imports section
        (r'# Check API key\nif not os\.environ\.get\("GROQ_API_KEY"\):\n    print\("⚠️  GROQ_API_KEY not found\."\)\n    if not os\.path\.exists\(\'\.env\'\):\n        auto_create_env_file\(\)\n    print\("⚠️  Please add GROQ_API_KEY to \.env file and restart"\)\n    print\("   Get free key from: https://console\.groq\.com/keys"\)',
         '# Ollama is used - no API key needed\n# Configuration is optional via OLLAMA_HOST environment variable'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Write back
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Successfully removed all GROQ references from main.py")
    print("💡 Now run: python main.py")

if __name__ == "__main__":
    try:
        fix_main_py()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please run this script from the Project_JARVIS directory")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aadhar ATM Demo Script
Quick test of screen reading and automation capabilities
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all dependencies are installed"""
    print("📦 Checking dependencies...\n")
    
    deps = {
        'pyautogui': 'PyAutoGUI',
        'pytesseract': 'Pytesseract',
        'PIL': 'Pillow',
        'cv2': 'OpenCV'
    }
    
    missing = []
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - NOT INSTALLED")
            missing.append(name.lower())
    
    print()
    
    if missing:
        print("⚠️  Missing dependencies!")
        print(f"\n📥 Install with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        return False
    
    print("✅ All dependencies installed!\n")
    return True


def test_screen_reading():
    """Test screen reading capability"""
    print("="*60)
    print("🧪 Test 1: Screen Reading")
    print("="*60)
    print()
    
    try:
        from skill.aadhar_atm_skill import AadharATMSkill
        
        skill = AadharATMSkill()
        
        print("📸 Capturing screen...")
        print("💡 Make sure some text is visible on screen\n")
        
        import time
        time.sleep(2)  # Give user time to prepare
        
        result = skill.read_screen_text(region="center")
        
        print(result)
        print()
        print("✅ Screen reading test complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_text_detection():
    """Test text detection on screen"""
    print("\n" + "="*60)
    print("🧪 Test 2: Text Detection")
    print("="*60)
    print()
    
    try:
        from skill.aadhar_atm_skill import AadharATMSkill
        
        skill = AadharATMSkill()
        
        search_text = input("Enter text to search on screen: ").strip()
        
        if not search_text:
            print("⚠️  No text entered, skipping test")
            return False
        
        print(f"\n🔍 Searching for: '{search_text}'")
        print("💡 Make sure the text is visible on screen\n")
        
        import time
        time.sleep(2)
        
        position = skill.find_text_on_screen(search_text)
        
        if position:
            print(f"✅ Found at position: {position}")
            print(f"   X: {position[0]}, Y: {position[1]}")
        else:
            print("❌ Text not found on screen")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def demo_withdrawal():
    """Demo withdrawal process (dry run)"""
    print("\n" + "="*60)
    print("🧪 Test 3: Withdrawal Demo (Dry Run)")
    print("="*60)
    print()
    
    print("⚠️  This is a DRY RUN - no actual clicks will happen")
    print("💡 It will show what the agent would do\n")
    
    try:
        from skill.aadhar_atm_skill import AadharATMSkill
        
        # Get inputs
        aadhar = input("Enter Aadhar number (12 digits): ").strip()
        amount = input("Enter amount: ").strip()
        
        if len(aadhar) != 12 or not aadhar.isdigit():
            print("❌ Invalid Aadhar number!")
            return False
        
        if not amount.isdigit():
            print("❌ Invalid amount!")
            return False
        
        print("\n📋 Withdrawal Plan:")
        print(f"   Aadhar: {aadhar[:4]}****{aadhar[-4:]}")
        print(f"   Amount: ₹{amount}")
        print()
        
        print("🤖 Agent would perform these steps:")
        print("   1. ⏳ Wait for ATM screen")
        print("   2. 🔍 Find Aadhar number field")
        print(f"   3. ⌨️  Type: {aadhar}")
        print("   4. 🔍 Find amount field")
        print(f"   5. ⌨️  Type: {amount}")
        print("   6. 🖱️  Click Submit button")
        print("   7. 🖱️  Click Print button")
        print("   8. 🖱️  Click OK button")
        print("   9. 📖 Read success message")
        print("   10. 🔊 Voice confirmation")
        print()
        
        proceed = input("Run actual automation? (yes/no): ").lower()
        
        if proceed == 'yes':
            print("\n⚠️  STARTING ACTUAL AUTOMATION IN 3 SECONDS...")
            print("💡 Move mouse to corner to stop (failsafe)")
            
            import time
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(1)
            
            print("\n🚀 Starting automation...\n")
            
            skill = AadharATMSkill()
            result = skill.aadhar_withdraw_money(aadhar, amount)
            
            print("\n" + "="*60)
            print(result)
            print("="*60)
        else:
            print("\n✅ Dry run complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main demo function"""
    
    print("\n" + "="*60)
    print("🏧 Aadhar ATM Automation - Demo & Testing")
    print("="*60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️  Please install missing dependencies first!")
        return
    
    # Menu
    while True:
        print("\n" + "="*60)
        print("📋 Demo Menu")
        print("="*60)
        print()
        print("1. Test Screen Reading")
        print("2. Test Text Detection")
        print("3. Demo Withdrawal (with dry run option)")
        print("4. Launch Full GUI")
        print("5. Exit")
        print()
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            test_screen_reading()
        elif choice == '2':
            test_text_detection()
        elif choice == '3':
            demo_withdrawal()
        elif choice == '4':
            print("\n🚀 Launching GUI...\n")
            import subprocess
            subprocess.run([sys.executable, "launch_aadhar_atm.py"])
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice!")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()

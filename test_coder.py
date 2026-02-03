#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Test Script for Autonomous Coder V2
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.autonomous_coder_v2 import AutonomousCoderV2


def test_react():
    """Test React project generation"""
    print("\n" + "="*70)
    print("Testing React Project Generation")
    print("="*70)
    
    coder = AutonomousCoderV2()
    
    result = coder.generate_fullstack_project(
        project_type='react',
        project_name='test-react-app',
        requirements='Simple React app for testing',
        output_dir='./test-output/test-react-app'
    )
    
    print(f"\n✅ React Test: {'PASSED' if result['success'] else 'FAILED'}")
    return result['success']


def test_django():
    """Test Django project generation"""
    print("\n" + "="*70)
    print("Testing Django Project Generation")
    print("="*70)
    
    coder = AutonomousCoderV2()
    
    result = coder.generate_fullstack_project(
        project_type='django',
        project_name='test-django-api',
        requirements='Simple Django API for testing',
        output_dir='./test-output/test-django-api'
    )
    
    print(f"\n✅ Django Test: {'PASSED' if result['success'] else 'FAILED'}")
    return result['success']


def test_mern():
    """Test MERN project generation"""
    print("\n" + "="*70)
    print("Testing MERN Project Generation")
    print("="*70)
    
    coder = AutonomousCoderV2()
    
    result = coder.generate_fullstack_project(
        project_type='mern',
        project_name='test-mern-app',
        requirements='Simple MERN app for testing',
        output_dir='./test-output/test-mern-app'
    )
    
    print(f"\n✅ MERN Test: {'PASSED' if result['success'] else 'FAILED'}")
    return result['success']


def test_android():
    """Test Android project generation"""
    print("\n" + "="*70)
    print("Testing Android Project Generation")
    print("="*70)
    
    coder = AutonomousCoderV2()
    
    result = coder.generate_fullstack_project(
        project_type='android',
        project_name='TestAndroidApp',
        requirements='Simple Android app for testing',
        output_dir='./test-output/TestAndroidApp'
    )
    
    print(f"\n✅ Android Test: {'PASSED' if result['success'] else 'FAILED'}")
    return result['success']


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 JARVIS Autonomous Coder V2 - Test Suite")
    print("="*70)
    
    tests = {
        'React': test_react,
        'Django': test_django,
        'MERN': test_mern,
        'Android': test_android,
    }
    
    results = {}
    
    for name, test_func in tests.items():
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} Test FAILED with error: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 Test Summary")
    print("="*70)
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:15} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("="*70)
    print(f"Total: {passed}/{total} tests passed ({passed*100//total}%)")
    print("="*70 + "\n")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check output above.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user.\n")
        sys.exit(0)

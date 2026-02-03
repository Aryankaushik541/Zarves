#!/usr/bin/env python3
"""
Test YouTube Auto-Play Skill
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.registry import SkillRegistry

def test_youtube_skill():
    print("\n" + "="*60)
    print("🧪 Testing YouTube Auto-Play Skill")
    print("="*60)
    
    # Load skills
    registry = SkillRegistry()
    registry.load_skills("skill")
    
    # List all skills
    print("\n📋 Loaded Skills:")
    for skill_name in registry.list_skills():
        print(f"  ✅ {skill_name}")
    
    # List all tools
    print("\n🔧 Available Tools:")
    for tool_name in registry.list_tools():
        print(f"  ✅ {tool_name}")
    
    # Check if YouTube skill is loaded
    print("\n🔍 Checking YouTube Player Skill...")
    
    if "youtube_player_skill" in registry.list_skills():
        print("  ✅ YouTube Player Skill is loaded!")
        
        # Get skill
        youtube_skill = registry.get_skill("youtube_player_skill")
        print(f"  ✅ Skill instance: {youtube_skill}")
        
        # Get tools
        tools = youtube_skill.get_tools()
        print(f"\n  📋 YouTube Skill Tools ({len(tools)}):")
        for tool in tools:
            tool_name = tool.get('function', {}).get('name', 'unknown')
            tool_desc = tool.get('function', {}).get('description', 'No description')
            print(f"    ▶️  {tool_name}")
            print(f"       {tool_desc[:80]}...")
        
        # Test play_youtube_video function
        print("\n🎵 Testing play_youtube_video function...")
        try:
            result = registry.execute_skill(
                "play_youtube_video",
                {"query": "Kesariya", "autoplay": True}
            )
            print(f"  ✅ Result: {result}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("  ❌ YouTube Player Skill NOT loaded!")
        print("\n  Available skills:")
        for skill_name in registry.list_skills():
            print(f"    - {skill_name}")

if __name__ == "__main__":
    test_youtube_skill()

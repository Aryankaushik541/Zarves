#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI-Powered System Controller
Natural language understanding for system control
Supports Hinglish and English commands
"""

import re
from skill.advanced_system_control import system_control


class AISystemController:
    """AI-powered system controller with NLU"""
    
    def __init__(self):
        self.system = system_control
        self.command_patterns = self.build_command_patterns()
    
    def build_command_patterns(self):
        """Build command patterns for NLU"""
        return {
            # Application control
            'open_app': [
                r'(?:open|start|launch|chalu|kholo|run)\s+(.+)',
                r'(.+)\s+(?:kholo|chalu karo|open karo|start karo)',
                r'mujhe\s+(.+)\s+chahiye',
            ],
            'close_app': [
                r'(?:close|quit|exit|band|stop)\s+(.+)',
                r'(.+)\s+(?:band karo|close karo|quit karo)',
                r'(.+)\s+ko\s+(?:band|close)\s+karo',
            ],
            
            # Volume control
            'volume_up': [
                r'(?:volume|awaz)\s+(?:up|badha|increase|zyada)',
                r'(?:increase|badha)\s+(?:volume|awaz)',
                r'awaz\s+(?:badha|zyada)\s+karo',
            ],
            'volume_down': [
                r'(?:volume|awaz)\s+(?:down|kam|decrease|low)',
                r'(?:decrease|kam)\s+(?:volume|awaz)',
                r'awaz\s+(?:kam|low)\s+karo',
            ],
            'volume_set': [
                r'(?:volume|awaz)\s+(?:set|rakh)\s+(?:to|pe|at)?\s*(\d+)',
                r'(?:set|rakh)\s+(?:volume|awaz)\s+(?:to|pe|at)?\s*(\d+)',
                r'awaz\s+(\d+)\s+(?:pe|par)\s+karo',
            ],
            'mute': [
                r'(?:mute|silent|chup)',
                r'awaz\s+(?:band|off)\s+karo',
                r'volume\s+(?:off|mute)\s+karo',
            ],
            'unmute': [
                r'(?:unmute|sound on)',
                r'awaz\s+(?:chalu|on)\s+karo',
                r'volume\s+(?:on|unmute)\s+karo',
            ],
            
            # Brightness control
            'brightness_set': [
                r'(?:brightness|chamak)\s+(?:set|rakh)\s+(?:to|pe|at)?\s*(\d+)',
                r'(?:set|rakh)\s+(?:brightness|chamak)\s+(?:to|pe|at)?\s*(\d+)',
                r'screen\s+(?:brightness|chamak)\s+(\d+)',
            ],
            'brightness_up': [
                r'(?:brightness|chamak)\s+(?:up|badha|increase)',
                r'screen\s+(?:bright|chamakdar)\s+karo',
            ],
            'brightness_down': [
                r'(?:brightness|chamak)\s+(?:down|kam|decrease)',
                r'screen\s+(?:dim|halka)\s+karo',
            ],
            
            # WiFi control
            'wifi_on': [
                r'(?:wifi|wi-fi)\s+(?:on|chalu|enable)',
                r'(?:turn on|chalu karo)\s+(?:wifi|wi-fi)',
                r'wifi\s+chalu\s+karo',
            ],
            'wifi_off': [
                r'(?:wifi|wi-fi)\s+(?:off|band|disable)',
                r'(?:turn off|band karo)\s+(?:wifi|wi-fi)',
                r'wifi\s+band\s+karo',
            ],
            
            # Bluetooth control
            'bluetooth_on': [
                r'bluetooth\s+(?:on|chalu|enable)',
                r'(?:turn on|chalu karo)\s+bluetooth',
                r'bluetooth\s+chalu\s+karo',
            ],
            'bluetooth_off': [
                r'bluetooth\s+(?:off|band|disable)',
                r'(?:turn off|band karo)\s+bluetooth',
                r'bluetooth\s+band\s+karo',
            ],
            
            # Display control
            'display_off': [
                r'(?:display|screen|monitor)\s+(?:off|band)',
                r'(?:turn off|band karo)\s+(?:display|screen)',
                r'screen\s+band\s+karo',
            ],
            'display_on': [
                r'(?:display|screen|monitor)\s+(?:on|chalu)',
                r'(?:turn on|chalu karo)\s+(?:display|screen)',
                r'screen\s+chalu\s+karo',
            ],
            
            # Window management
            'minimize': [
                r'(?:minimize|chhota karo)\s+(?:window|this)?',
                r'window\s+(?:minimize|chhota)\s+karo',
            ],
            'maximize': [
                r'(?:maximize|bada karo)\s+(?:window|this)?',
                r'window\s+(?:maximize|bada)\s+karo',
                r'full\s+screen\s+karo',
            ],
            'close_window': [
                r'(?:close|band karo)\s+(?:window|this)',
                r'window\s+(?:close|band)\s+karo',
            ],
            'switch_window': [
                r'(?:switch|change|badlo)\s+(?:window|app)',
                r'(?:next|agle)\s+window',
                r'window\s+(?:switch|badlo)',
            ],
            
            # System settings
            'open_settings': [
                r'(?:open|kholo)\s+(?:settings|preferences)',
                r'settings\s+(?:open|kholo)',
                r'system\s+settings',
            ],
            
            # Power management
            'shutdown': [
                r'(?:shutdown|band karo|turn off)\s+(?:computer|system|pc)?',
                r'computer\s+(?:shutdown|band)\s+karo',
                r'system\s+(?:off|shutdown)',
            ],
            'restart': [
                r'(?:restart|reboot|dubara chalu)\s+(?:computer|system|pc)?',
                r'computer\s+(?:restart|reboot)\s+karo',
                r'system\s+restart',
            ],
            'sleep': [
                r'(?:sleep|suspend)\s+(?:computer|system|pc)?',
                r'computer\s+(?:sleep|so jao)',
                r'system\s+sleep',
            ],
            'lock': [
                r'(?:lock|tala lagao)\s+(?:computer|system|pc)?',
                r'computer\s+(?:lock|tala)\s+lagao',
                r'system\s+lock',
            ],
        }
    
    def understand_command(self, command):
        """Understand natural language command"""
        command = command.lower().strip()
        
        # Try to match patterns
        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    # Extract parameters if any
                    params = match.groups() if match.groups() else None
                    return action, params
        
        return None, None
    
    def execute_command(self, command):
        """Execute system command from natural language"""
        action, params = self.understand_command(command)
        
        if not action:
            return False, "Sorry, I didn't understand that command"
        
        try:
            # Application control
            if action == 'open_app':
                app_name = params[0] if params else None
                if app_name:
                    return self.system.open_application(app_name)
                return False, "Please specify an application name"
            
            elif action == 'close_app':
                app_name = params[0] if params else None
                if app_name:
                    return self.system.close_application(app_name)
                return False, "Please specify an application name"
            
            # Volume control
            elif action == 'volume_up':
                current = self.system.control_volume("get")
                if current[0]:
                    level = int(current[1].split(":")[1].strip().replace("%", ""))
                    new_level = min(100, level + 10)
                    return self.system.control_volume("set", new_level)
                return False, "Could not get current volume"
            
            elif action == 'volume_down':
                current = self.system.control_volume("get")
                if current[0]:
                    level = int(current[1].split(":")[1].strip().replace("%", ""))
                    new_level = max(0, level - 10)
                    return self.system.control_volume("set", new_level)
                return False, "Could not get current volume"
            
            elif action == 'volume_set':
                level = int(params[0]) if params else 50
                return self.system.control_volume("set", level)
            
            elif action == 'mute':
                return self.system.control_volume("mute")
            
            elif action == 'unmute':
                return self.system.control_volume("unmute")
            
            # Brightness control
            elif action == 'brightness_set':
                level = int(params[0]) if params else 50
                return self.system.control_brightness(level)
            
            elif action == 'brightness_up':
                return self.system.control_brightness(80)
            
            elif action == 'brightness_down':
                return self.system.control_brightness(30)
            
            # WiFi control
            elif action == 'wifi_on':
                return self.system.control_wifi("on")
            
            elif action == 'wifi_off':
                return self.system.control_wifi("off")
            
            # Bluetooth control
            elif action == 'bluetooth_on':
                return self.system.control_bluetooth("on")
            
            elif action == 'bluetooth_off':
                return self.system.control_bluetooth("off")
            
            # Display control
            elif action == 'display_off':
                return self.system.control_display("sleep")
            
            elif action == 'display_on':
                return self.system.control_display("on")
            
            # Window management
            elif action == 'minimize':
                return self.system.minimize_window()
            
            elif action == 'maximize':
                return self.system.maximize_window()
            
            elif action == 'close_window':
                return self.system.close_window()
            
            elif action == 'switch_window':
                return self.system.switch_window()
            
            # System settings
            elif action == 'open_settings':
                return self.system.open_system_settings()
            
            # Power management
            elif action == 'shutdown':
                return self.system.shutdown_system(10)
            
            elif action == 'restart':
                return self.system.restart_system(10)
            
            elif action == 'sleep':
                return self.system.sleep_system()
            
            elif action == 'lock':
                return self.system.lock_system()
            
            else:
                return False, f"Action '{action}' not implemented"
                
        except Exception as e:
            return False, f"Error executing command: {str(e)}"
    
    def get_help(self):
        """Get help text for available commands"""
        help_text = """
🤖 JARVIS System Control Commands:

📱 APPLICATION CONTROL:
  • "Open Chrome" / "Chrome kholo"
  • "Close Firefox" / "Firefox band karo"
  • "Start VS Code" / "VS Code chalu karo"

🔊 VOLUME CONTROL:
  • "Volume up" / "Awaz badha"
  • "Volume down" / "Awaz kam karo"
  • "Set volume to 50" / "Awaz 50 pe karo"
  • "Mute" / "Awaz band karo"
  • "Unmute" / "Awaz chalu karo"

💡 BRIGHTNESS CONTROL:
  • "Set brightness to 70" / "Chamak 70 pe karo"
  • "Brightness up" / "Chamak badha"
  • "Brightness down" / "Chamak kam karo"

📡 CONNECTIVITY:
  • "WiFi on" / "WiFi chalu karo"
  • "WiFi off" / "WiFi band karo"
  • "Bluetooth on" / "Bluetooth chalu karo"
  • "Bluetooth off" / "Bluetooth band karo"

🖥️ DISPLAY CONTROL:
  • "Display off" / "Screen band karo"
  • "Display on" / "Screen chalu karo"

🪟 WINDOW MANAGEMENT:
  • "Minimize window" / "Window chhota karo"
  • "Maximize window" / "Window bada karo"
  • "Close window" / "Window band karo"
  • "Switch window" / "Window badlo"

⚙️ SYSTEM SETTINGS:
  • "Open settings" / "Settings kholo"

🔌 POWER MANAGEMENT:
  • "Shutdown" / "Computer band karo"
  • "Restart" / "Computer restart karo"
  • "Sleep" / "Computer so jao"
  • "Lock" / "Computer lock karo"

💡 TIP: You can use both English and Hinglish commands!
"""
        return help_text


# Global instance
ai_controller = AISystemController()


# ============================================================================
# MAIN SKILL FUNCTION FOR JARVIS
# ============================================================================

def process_system_command(command):
    """
    Main function to process system control commands
    This is called by JARVIS engine
    """
    return ai_controller.execute_command(command)


def get_system_help():
    """Get help for system commands"""
    return ai_controller.get_help()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("🤖 AI System Controller Test")
    print("=" * 60)
    
    # Test commands
    test_commands = [
        "Open Chrome",
        "Chrome kholo",
        "Volume badha",
        "Set volume to 50",
        "Brightness 70 pe karo",
        "WiFi chalu karo",
        "Window maximize karo",
        "Settings kholo",
    ]
    
    for cmd in test_commands:
        print(f"\n📝 Command: {cmd}")
        success, message = process_system_command(cmd)
        print(f"{'✅' if success else '❌'} {message}")
    
    print("\n" + "=" * 60)
    print(get_system_help())

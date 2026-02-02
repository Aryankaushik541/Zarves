"""
AI Game Player - Autonomous Gaming Agent
Plays games like GTA 5, Minecraft, etc. using computer vision and AI
"""

import os
import sys
import json
import time
import numpy as np
import cv2
import pyautogui
import keyboard
import mouse
from typing import List, Dict, Any, Callable, Tuple
from core.skill import Skill
from PIL import ImageGrab
import threading

class AIGamePlayer(Skill):
    """
    AI agent that can play games autonomously using:
    - Computer vision for screen analysis
    - AI decision making
    - Keyboard/mouse control
    - Object detection
    - Path planning
    """
    
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.game_thread = None
        self.current_game = None
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Game-specific configurations
        self.game_configs = {
            "gta5": {
                "name": "Grand Theft Auto V",
                "controls": {
                    "forward": "w",
                    "backward": "s",
                    "left": "a",
                    "right": "d",
                    "jump": "space",
                    "sprint": "shift",
                    "crouch": "ctrl",
                    "shoot": "left_click",
                    "aim": "right_click",
                    "enter_vehicle": "f",
                    "exit_vehicle": "f",
                    "handbrake": "space",
                    "horn": "e",
                    "change_camera": "v",
                    "pause": "esc",
                },
                "objectives": [
                    "drive_safely",
                    "avoid_police",
                    "complete_missions",
                    "explore_map",
                ]
            },
            "minecraft": {
                "name": "Minecraft",
                "controls": {
                    "forward": "w",
                    "backward": "s",
                    "left": "a",
                    "right": "d",
                    "jump": "space",
                    "sprint": "ctrl",
                    "crouch": "shift",
                    "attack": "left_click",
                    "use": "right_click",
                    "inventory": "e",
                    "drop": "q",
                },
                "objectives": [
                    "gather_resources",
                    "build_shelter",
                    "craft_tools",
                    "survive",
                ]
            },
            "csgo": {
                "name": "Counter-Strike: Global Offensive",
                "controls": {
                    "forward": "w",
                    "backward": "s",
                    "left": "a",
                    "right": "d",
                    "jump": "space",
                    "crouch": "ctrl",
                    "shoot": "left_click",
                    "aim": "right_click",
                    "reload": "r",
                    "switch_weapon": "q",
                },
                "objectives": [
                    "aim_at_enemies",
                    "control_recoil",
                    "use_cover",
                    "plant_bomb",
                ]
            }
        }
    
    @property
    def name(self) -> str:
        return "ai_game_player"
    
    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "start_playing_game",
                    "description": "Start AI autonomous game playing. AI will analyze screen, make decisions, and control the game. Supports GTA 5, Minecraft, CS:GO, and more.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_name": {
                                "type": "string",
                                "description": "Name of the game to play (e.g., 'gta5', 'minecraft', 'csgo')"
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["explore", "mission", "survival", "combat"],
                                "description": "Game mode - explore (roam around), mission (complete objectives), survival (stay alive), combat (fight enemies)"
                            },
                            "duration": {
                                "type": "integer",
                                "description": "How long to play in seconds (default: 300 = 5 minutes)"
                            }
                        },
                        "required": ["game_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "stop_playing_game",
                    "description": "Stop AI game playing and return control to user",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_game_screen",
                    "description": "Analyze current game screen and provide AI insights about what's happening",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_name": {
                                "type": "string",
                                "description": "Name of the game"
                            }
                        },
                        "required": ["game_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "perform_game_action",
                    "description": "Perform a specific action in the game (move, shoot, jump, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_name": {
                                "type": "string",
                                "description": "Name of the game"
                            },
                            "action": {
                                "type": "string",
                                "description": "Action to perform (e.g., 'forward', 'shoot', 'jump', 'drive')"
                            },
                            "duration": {
                                "type": "number",
                                "description": "How long to perform action in seconds (default: 1)"
                            }
                        },
                        "required": ["game_name", "action"]
                    }
                }
            }
        ]
    
    def get_functions(self) -> Dict[str, Callable]:
        return {
            "start_playing_game": self.start_playing_game,
            "stop_playing_game": self.stop_playing_game,
            "analyze_game_screen": self.analyze_game_screen,
            "perform_game_action": self.perform_game_action,
        }
    
    def capture_screen(self) -> np.ndarray:
        """Capture current screen as numpy array"""
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
    
    def detect_objects(self, frame: np.ndarray, game_name: str) -> List[Dict]:
        """
        Detect game objects using computer vision
        Returns list of detected objects with positions
        """
        objects = []
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if game_name == "gta5":
            # Detect cars (look for rectangular shapes)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filter small objects
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        "type": "vehicle",
                        "position": (x, y),
                        "size": (w, h),
                        "confidence": 0.7
                    })
            
            # Detect roads (look for gray/black areas)
            lower_road = np.array([0, 0, 50])
            upper_road = np.array([180, 50, 150])
            road_mask = cv2.inRange(hsv, lower_road, upper_road)
            
            # Detect police (look for blue/red flashing lights)
            lower_police = np.array([100, 100, 100])
            upper_police = np.array([130, 255, 255])
            police_mask = cv2.inRange(hsv, lower_police, upper_police)
            
            if cv2.countNonZero(police_mask) > 1000:
                objects.append({
                    "type": "police",
                    "position": "nearby",
                    "confidence": 0.8
                })
        
        elif game_name == "minecraft":
            # Detect blocks, trees, animals
            # Look for specific colors
            pass
        
        return objects
    
    def make_decision(self, frame: np.ndarray, objects: List[Dict], game_name: str, mode: str) -> str:
        """
        AI decision making based on screen analysis
        Returns action to perform
        """
        if game_name == "gta5":
            # Check for police
            has_police = any(obj["type"] == "police" for obj in objects)
            
            if has_police and mode != "combat":
                return "evade_police"
            
            if mode == "explore":
                # Random exploration
                import random
                actions = ["forward", "left", "right", "forward"]
                return random.choice(actions)
            
            elif mode == "mission":
                # Follow waypoint
                return "follow_waypoint"
            
            elif mode == "combat":
                # Engage enemies
                return "aim_and_shoot"
        
        return "forward"
    
    def execute_action(self, action: str, game_name: str, duration: float = 1.0):
        """Execute game action using keyboard/mouse"""
        config = self.game_configs.get(game_name, {})
        controls = config.get("controls", {})
        
        if action == "forward":
            keyboard.press(controls.get("forward", "w"))
            time.sleep(duration)
            keyboard.release(controls.get("forward", "w"))
        
        elif action == "backward":
            keyboard.press(controls.get("backward", "s"))
            time.sleep(duration)
            keyboard.release(controls.get("backward", "s"))
        
        elif action == "left":
            keyboard.press(controls.get("left", "a"))
            time.sleep(duration)
            keyboard.release(controls.get("left", "a"))
        
        elif action == "right":
            keyboard.press(controls.get("right", "d"))
            time.sleep(duration)
            keyboard.release(controls.get("right", "d"))
        
        elif action == "jump":
            keyboard.press(controls.get("jump", "space"))
            time.sleep(0.1)
            keyboard.release(controls.get("jump", "space"))
        
        elif action == "shoot":
            mouse.click("left")
        
        elif action == "aim_and_shoot":
            mouse.press("right")
            time.sleep(0.5)
            mouse.click("left")
            time.sleep(0.1)
            mouse.release("right")
        
        elif action == "evade_police":
            # Quick evasive maneuvers
            keyboard.press(controls.get("sprint", "shift"))
            keyboard.press(controls.get("forward", "w"))
            time.sleep(2)
            keyboard.press(controls.get("left", "a"))
            time.sleep(1)
            keyboard.release(controls.get("left", "a"))
            keyboard.release(controls.get("forward", "w"))
            keyboard.release(controls.get("sprint", "shift"))
        
        elif action == "drive":
            keyboard.press(controls.get("forward", "w"))
            time.sleep(duration)
            keyboard.release(controls.get("forward", "w"))
    
    def game_loop(self, game_name: str, mode: str, duration: int):
        """Main game playing loop"""
        start_time = time.time()
        frame_count = 0
        
        print(f"\n🎮 AI Game Player Started!")
        print(f"   Game: {self.game_configs.get(game_name, {}).get('name', game_name)}")
        print(f"   Mode: {mode}")
        print(f"   Duration: {duration}s")
        print(f"\n🤖 AI is now playing... Press 'q' to stop\n")
        
        while self.is_playing and (time.time() - start_time) < duration:
            try:
                # Capture screen
                frame = self.capture_screen()
                frame_count += 1
                
                # Analyze every 5th frame (performance optimization)
                if frame_count % 5 == 0:
                    # Detect objects
                    objects = self.detect_objects(frame, game_name)
                    
                    # Make decision
                    action = self.make_decision(frame, objects, game_name, mode)
                    
                    # Execute action
                    self.execute_action(action, game_name, duration=0.5)
                    
                    # Log progress
                    elapsed = int(time.time() - start_time)
                    print(f"⏱️  {elapsed}s | Action: {action} | Objects: {len(objects)}", end="\r")
                
                # Check for stop key
                if keyboard.is_pressed('q'):
                    print("\n\n⏹️  Stopped by user")
                    break
                
                time.sleep(0.1)  # Small delay
                
            except Exception as e:
                print(f"\n❌ Error in game loop: {e}")
                break
        
        self.is_playing = False
        elapsed = int(time.time() - start_time)
        print(f"\n\n✅ Game session completed!")
        print(f"   Duration: {elapsed}s")
        print(f"   Frames processed: {frame_count}")
    
    def start_playing_game(self, game_name: str, mode: str = "explore", duration: int = 300):
        """Start autonomous game playing"""
        try:
            game_name = game_name.lower()
            
            if game_name not in self.game_configs:
                return json.dumps({
                    "error": f"Game '{game_name}' not supported yet",
                    "supported_games": list(self.game_configs.keys())
                })
            
            if self.is_playing:
                return json.dumps({
                    "error": "Already playing a game. Stop current session first."
                })
            
            self.is_playing = True
            self.current_game = game_name
            
            # Start game loop in separate thread
            self.game_thread = threading.Thread(
                target=self.game_loop,
                args=(game_name, mode, duration)
            )
            self.game_thread.start()
            
            return json.dumps({
                "status": "success",
                "message": f"AI started playing {self.game_configs[game_name]['name']}",
                "game": game_name,
                "mode": mode,
                "duration": duration,
                "controls": "Press 'q' to stop"
            })
            
        except Exception as e:
            self.is_playing = False
            return json.dumps({"error": str(e)})
    
    def stop_playing_game(self):
        """Stop game playing"""
        try:
            if not self.is_playing:
                return json.dumps({
                    "status": "info",
                    "message": "No game is currently being played"
                })
            
            self.is_playing = False
            
            if self.game_thread:
                self.game_thread.join(timeout=5)
            
            return json.dumps({
                "status": "success",
                "message": "Game playing stopped",
                "game": self.current_game
            })
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def analyze_game_screen(self, game_name: str):
        """Analyze current game screen"""
        try:
            frame = self.capture_screen()
            objects = self.detect_objects(frame, game_name)
            
            # Get screen statistics
            height, width = frame.shape[:2]
            avg_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            
            return json.dumps({
                "status": "success",
                "game": game_name,
                "screen": {
                    "width": width,
                    "height": height,
                    "brightness": float(avg_brightness)
                },
                "objects_detected": len(objects),
                "objects": objects[:5],  # Top 5 objects
                "analysis": f"Detected {len(objects)} objects on screen"
            })
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def perform_game_action(self, game_name: str, action: str, duration: float = 1.0):
        """Perform specific game action"""
        try:
            self.execute_action(action, game_name, duration)
            
            return json.dumps({
                "status": "success",
                "action": action,
                "duration": duration,
                "game": game_name
            })
            
        except Exception as e:
            return json.dumps({"error": str(e)})

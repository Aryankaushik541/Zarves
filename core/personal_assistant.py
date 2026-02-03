#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Personal Assistant Core - Makes JARVIS behave like a real human assistant
- Natural conversation with context memory
- Emotion detection and appropriate responses
- Proactive suggestions based on user behavior
- Multi-step task handling
- Personality and empathy
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PersonalAssistant:
    """
    Intelligent personal assistant that makes JARVIS feel human
    """
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.context = {}
        self.last_task = None
        self.user_mood = "neutral"
        self.memory_file = "assistant_memory.json"
        
        # Load previous memory
        self.load_memory()
    
    def load_memory(self):
        """Load assistant's memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_preferences = data.get('preferences', {})
                    self.context = data.get('context', {})
        except Exception as e:
            print(f"⚠️  Could not load memory: {e}")
    
    def save_memory(self):
        """Save assistant's memory to file"""
        try:
            data = {
                'preferences': self.user_preferences,
                'context': self.context,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Could not save memory: {e}")
    
    def detect_emotion(self, text: str) -> str:
        """
        Detect user's emotion from text
        Returns: happy, sad, angry, frustrated, excited, neutral
        """
        text_lower = text.lower()
        
        # Happy indicators
        happy_words = ['thanks', 'great', 'awesome', 'love', 'perfect', 'excellent', 
                       'shukriya', 'badhiya', 'mast', 'zabardast', '😊', '😄', '🎉']
        if any(word in text_lower for word in happy_words):
            return "happy"
        
        # Frustrated/Angry indicators
        angry_words = ['stupid', 'useless', 'wrong', 'bad', 'hate', 'kharab', 
                       'bekaar', 'galat', '😠', '😡', 'wtf', 'damn']
        if any(word in text_lower for word in angry_words):
            return "frustrated"
        
        # Sad indicators
        sad_words = ['sad', 'sorry', 'unfortunately', 'problem', 'issue', 
                     'dukh', 'pareshan', '😢', '😞']
        if any(word in text_lower for word in sad_words):
            return "sad"
        
        # Excited indicators
        excited_words = ['wow', 'amazing', 'incredible', 'omg', 'yes!', 
                        'kamaal', 'shandar', '🔥', '✨', '!']
        if any(word in text_lower for word in excited_words):
            return "excited"
        
        return "neutral"
    
    def get_empathetic_response(self, emotion: str) -> str:
        """
        Generate empathetic response based on emotion
        """
        responses = {
            "happy": [
                "I'm glad I could help! 😊",
                "Happy to assist you!",
                "Khushi hui madad karke!",
                "Great! Anything else I can do?"
            ],
            "frustrated": [
                "I understand your frustration. Let me try to fix this.",
                "Sorry about that. I'll do better.",
                "Maaf kijiye, main theek kar deta hoon.",
                "Let me help you properly this time."
            ],
            "sad": [
                "I'm here to help. Let's solve this together.",
                "Don't worry, we'll figure it out.",
                "Koi baat nahi, main hoon na.",
                "I'll do my best to help you."
            ],
            "excited": [
                "That's awesome! 🎉",
                "I'm excited too!",
                "Zabardast! Aur kya chahiye?",
                "Let's keep the momentum going!"
            ],
            "neutral": [
                "Sure, I'm on it.",
                "Got it!",
                "Theek hai, kar deta hoon.",
                "Consider it done."
            ]
        }
        
        import random
        return random.choice(responses.get(emotion, responses["neutral"]))
    
    def understand_context(self, user_input: str) -> Dict:
        """
        Understand context from user input
        Returns: {
            'intent': 'play_music' | 'download_movie' | 'search' | 'system_control' | 'chat',
            'entities': {...},
            'is_followup': bool,
            'emotion': str
        }
        """
        text_lower = user_input.lower()
        
        context = {
            'intent': 'chat',
            'entities': {},
            'is_followup': False,
            'emotion': self.detect_emotion(user_input),
            'original_text': user_input
        }
        
        # Detect follow-up (references to previous conversation)
        followup_indicators = ['usko', 'woh', 'that', 'it', 'same', 'bhi', 'aur', 'also']
        if any(word in text_lower for word in followup_indicators) and self.last_task:
            context['is_followup'] = True
            context['previous_task'] = self.last_task
        
        # Music/YouTube intent
        music_keywords = ['play', 'bajao', 'song', 'gaana', 'music', 'youtube', 'video']
        if any(word in text_lower for word in music_keywords):
            context['intent'] = 'play_music'
            # Extract song name
            for keyword in ['play', 'bajao', 'song', 'gaana']:
                if keyword in text_lower:
                    parts = text_lower.split(keyword)
                    if len(parts) > 1:
                        context['entities']['song_name'] = parts[1].strip()
        
        # Movie download intent
        movie_keywords = ['download', 'movie', 'film', 'vegamovies']
        if any(word in text_lower for word in movie_keywords):
            context['intent'] = 'download_movie'
            # Extract movie name
            if 'download' in text_lower:
                parts = text_lower.split('download')
                if len(parts) > 1:
                    context['entities']['movie_name'] = parts[1].strip()
        
        # Search intent
        search_keywords = ['search', 'google', 'find', 'dhundo', 'khojo']
        if any(word in text_lower for word in search_keywords):
            context['intent'] = 'search'
            for keyword in search_keywords:
                if keyword in text_lower:
                    parts = text_lower.split(keyword)
                    if len(parts) > 1:
                        context['entities']['query'] = parts[1].strip()
        
        # System control intent
        system_keywords = ['volume', 'brightness', 'screenshot', 'open', 'close', 'kholo', 'band']
        if any(word in text_lower for word in system_keywords):
            context['intent'] = 'system_control'
            context['entities']['action'] = user_input
        
        # Web browsing intent
        web_keywords = ['website', 'open', 'kholo', '.com', '.in', 'http']
        if any(word in text_lower for word in web_keywords):
            context['intent'] = 'web_browse'
            context['entities']['url'] = user_input
        
        return context
    
    def generate_natural_response(self, context: Dict, result: str = None) -> str:
        """
        Generate natural, human-like response
        """
        intent = context['intent']
        emotion = context['emotion']
        
        # Start with empathetic acknowledgment
        response = self.get_empathetic_response(emotion)
        
        # Add task-specific response
        if intent == 'play_music':
            song = context['entities'].get('song_name', 'trending song')
            response = f"🎵 Playing {song} for you!"
        
        elif intent == 'download_movie':
            movie = context['entities'].get('movie_name', 'movie')
            response = f"🎬 Downloading {movie}. I'll let you know when it's ready!"
        
        elif intent == 'search':
            query = context['entities'].get('query', 'that')
            response = f"🔍 Searching for {query}..."
        
        elif intent == 'system_control':
            response = "✅ Done!"
        
        elif intent == 'web_browse':
            response = "🌐 Opening that for you..."
        
        elif intent == 'chat':
            # Natural conversation
            if emotion == "happy":
                response = "I'm glad you're happy! How else can I help?"
            elif emotion == "frustrated":
                response = "I understand. Let me know what's wrong and I'll fix it."
            else:
                response = "I'm here to help. What would you like me to do?"
        
        # Add result if provided
        if result:
            response += f"\n{result}"
        
        return response
    
    def learn_preference(self, key: str, value: any):
        """Learn user preference"""
        self.user_preferences[key] = value
        self.save_memory()
    
    def get_preference(self, key: str, default=None):
        """Get user preference"""
        return self.user_preferences.get(key, default)
    
    def add_to_history(self, user_input: str, response: str):
        """Add conversation to history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'assistant': response
        })
        
        # Keep only last 50 conversations in memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def get_proactive_suggestion(self) -> Optional[str]:
        """
        Generate proactive suggestions based on context and history
        """
        current_hour = datetime.now().hour
        
        # Morning suggestions
        if 6 <= current_hour < 12:
            return "Good morning! Would you like me to play some energetic music?"
        
        # Afternoon suggestions
        elif 12 <= current_hour < 17:
            return "Need any help with work? I can search for information or play focus music."
        
        # Evening suggestions
        elif 17 <= current_hour < 21:
            return "Evening! Want me to play some relaxing music or find a movie?"
        
        # Night suggestions
        elif 21 <= current_hour or current_hour < 6:
            return "It's getting late. Need anything before you rest?"
        
        return None
    
    def process_conversation(self, user_input: str) -> Dict:
        """
        Main method to process user input and generate intelligent response
        
        Returns: {
            'context': {...},
            'response': str,
            'action_needed': bool,
            'action_type': str,
            'action_params': {...}
        }
        """
        # Understand context
        context = self.understand_context(user_input)
        
        # Update user mood
        self.user_mood = context['emotion']
        
        # Determine if action is needed
        action_needed = context['intent'] != 'chat'
        
        # Generate response
        response = self.generate_natural_response(context)
        
        # Prepare action parameters
        action_params = {}
        if action_needed:
            action_params = context['entities']
        
        # Update last task
        if action_needed:
            self.last_task = {
                'intent': context['intent'],
                'entities': context['entities'],
                'timestamp': datetime.now().isoformat()
            }
        
        # Add to history
        self.add_to_history(user_input, response)
        
        return {
            'context': context,
            'response': response,
            'action_needed': action_needed,
            'action_type': context['intent'],
            'action_params': action_params,
            'emotion': context['emotion']
        }
    
    def handle_clarification(self, user_input: str) -> str:
        """
        Handle clarification questions
        """
        text_lower = user_input.lower()
        
        # Yes/No responses
        if any(word in text_lower for word in ['yes', 'haan', 'ha', 'yeah', 'sure', 'ok']):
            if self.last_task:
                return f"Great! Continuing with {self.last_task['intent']}..."
            return "Okay! What would you like me to do?"
        
        if any(word in text_lower for word in ['no', 'nahi', 'nope', 'cancel']):
            return "No problem! Let me know if you need anything else."
        
        return "I didn't quite get that. Could you please clarify?"
    
    def get_personality_response(self, situation: str) -> str:
        """
        Add personality to responses
        """
        personalities = {
            'greeting': [
                "Hello! I'm JARVIS, your personal assistant. How can I help you today?",
                "Hi there! Ready to assist you!",
                "Namaste! Kaise madad kar sakta hoon?",
                "Hey! What can I do for you?"
            ],
            'thanks': [
                "You're welcome! Happy to help! 😊",
                "Anytime! That's what I'm here for!",
                "Khushi hui madad karke!",
                "My pleasure!"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Alvida! Phir milenge!",
                "Bye! Call me anytime you need help!"
            ],
            'error': [
                "Oops! Something went wrong. Let me try again.",
                "Sorry about that. I'll fix it right away.",
                "Maaf kijiye, ek baar aur try karta hoon.",
                "My bad! Let me correct that."
            ]
        }
        
        import random
        return random.choice(personalities.get(situation, ["I'm here to help!"]))


# Global instance
personal_assistant = PersonalAssistant()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced AI Agent for JARVIS
✅ Smart intent detection
✅ Context-aware responses
✅ Multi-language support (Hindi + English)
✅ Conversation memory
✅ Action execution
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests


class EnhancedAIAgent:
    """Enhanced AI Agent with smart intent detection"""
    
    def __init__(self, engine, ollama_url="http://localhost:11434"):
        self.engine = engine
        self.ollama_url = ollama_url
        self.model = "llama3.2"
        
        # Conversation context
        self.conversation_history = []
        self.context = {}
        
        # Intent patterns (Hindi + English)
        self.intent_patterns = {
            'youtube': [
                r'(youtube|यूट्यूब).*(खोल|open|play|चला)',
                r'(video|वीडियो|song|गाना).*(play|चला|सुना)',
                r'(music|संगीत).*(play|चला)',
            ],
            'browser': [
                r'(browser|ब्राउज़र).*(खोल|open)',
                r'(chrome|firefox|edge).*(खोल|open)',
                r'(internet|इंटरनेट).*(खोल|open)',
            ],
            'movie': [
                r'(movie|फिल्म|मूवी).*(play|चला|देख|search|खोज)',
                r'(vlc).*(open|खोल)',
            ],
            'search': [
                r'(search|खोज|ढूंढ).*(google|गूगल)',
                r'(find|खोज).*(information|जानकारी)',
                r'(what is|क्या है)',
                r'(who is|कौन है)',
                r'(how to|कैसे)',
            ],
            'system': [
                r'(shutdown|बंद कर).*(computer|pc|system)',
                r'(restart|रीस्टार्ट).*(computer|pc|system)',
                r'(sleep|स्लीप).*(computer|pc|system)',
                r'(volume|आवाज़).*(up|down|बढ़ा|घटा)',
            ],
            'file': [
                r'(file|फाइल).*(open|खोल|create|बना|delete|मिटा)',
                r'(folder|फोल्डर).*(open|खोल|create|बना)',
            ],
            'time': [
                r'(time|समय|टाइम).*(क्या|what|बता)',
                r'(date|तारीख|डेट).*(क्या|what|बता)',
            ],
            'weather': [
                r'(weather|मौसम).*(कैसा|how|क्या)',
                r'(temperature|तापमान)',
            ],
            'email': [
                r'(email|ईमेल|mail).*(send|भेज|write|लिख)',
            ],
            'screenshot': [
                r'(screenshot|स्क्रीनशॉट).*(ले|take|capture)',
            ],
            'general': []  # Fallback
        }
        
        # Action executors
        self.action_executors = {}
        self._register_action_executors()
    
    def _register_action_executors(self):
        """Register action executors for different intents"""
        self.action_executors = {
            'youtube': self._execute_youtube,
            'browser': self._execute_browser,
            'movie': self._execute_movie,
            'search': self._execute_search,
            'system': self._execute_system,
            'file': self._execute_file,
            'time': self._execute_time,
            'weather': self._execute_weather,
            'email': self._execute_email,
            'screenshot': self._execute_screenshot,
            'general': self._execute_general,
        }
    
    def detect_intent(self, query: str) -> Tuple[str, float]:
        """
        Detect intent from query
        Returns: (intent, confidence)
        """
        query_lower = query.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent, 0.9
        
        # Fallback to general
        return 'general', 0.5
    
    def extract_entities(self, query: str, intent: str) -> Dict:
        """Extract entities from query based on intent"""
        entities = {}
        
        if intent == 'youtube':
            # Extract search query
            match = re.search(r'(play|चला|सुना)\s+(.+)', query, re.IGNORECASE)
            if match:
                entities['query'] = match.group(2).strip()
        
        elif intent == 'search':
            # Extract search query
            match = re.search(r'(search|खोज|ढूंढ)\s+(.+)', query, re.IGNORECASE)
            if match:
                entities['query'] = match.group(2).strip()
            else:
                # For "what is", "who is" questions
                entities['query'] = query
        
        elif intent == 'movie':
            # Extract movie name
            match = re.search(r'(movie|फिल्म|मूवी)\s+(.+)', query, re.IGNORECASE)
            if match:
                entities['movie_name'] = match.group(2).strip()
        
        elif intent == 'system':
            # Extract system action
            if re.search(r'shutdown|बंद', query, re.IGNORECASE):
                entities['action'] = 'shutdown'
            elif re.search(r'restart|रीस्टार्ट', query, re.IGNORECASE):
                entities['action'] = 'restart'
            elif re.search(r'sleep|स्लीप', query, re.IGNORECASE):
                entities['action'] = 'sleep'
            elif re.search(r'volume.*up|आवाज़.*बढ़ा', query, re.IGNORECASE):
                entities['action'] = 'volume_up'
            elif re.search(r'volume.*down|आवाज़.*घटा', query, re.IGNORECASE):
                entities['action'] = 'volume_down'
        
        return entities
    
    def get_ai_response(self, query: str, context: Optional[Dict] = None) -> str:
        """Get AI response from Ollama"""
        try:
            # Build prompt with context
            prompt = self._build_prompt(query, context)
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return "Sorry, I couldn't process that."
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _build_prompt(self, query: str, context: Optional[Dict] = None) -> str:
        """Build prompt with context"""
        prompt_parts = [
            "You are JARVIS, a helpful AI assistant.",
            "You can help with various tasks like opening apps, searching, playing music, etc.",
            ""
        ]
        
        # Add conversation history (last 3 exchanges)
        if self.conversation_history:
            prompt_parts.append("Recent conversation:")
            for entry in self.conversation_history[-6:]:  # Last 3 exchanges
                role = entry['role'].capitalize()
                content = entry['content']
                prompt_parts.append(f"{role}: {content}")
            prompt_parts.append("")
        
        # Add context
        if context:
            prompt_parts.append(f"Context: {json.dumps(context)}")
            prompt_parts.append("")
        
        # Add current query
        prompt_parts.append(f"User: {query}")
        prompt_parts.append("JARVIS:")
        
        return "\n".join(prompt_parts)
    
    def process_query(self, query: str) -> str:
        """
        Process user query
        Returns: Response string
        """
        try:
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': query,
                'timestamp': datetime.now().isoformat()
            })
            
            # Detect intent
            intent, confidence = self.detect_intent(query)
            
            # Extract entities
            entities = self.extract_entities(query, intent)
            
            # Update context
            self.context.update({
                'last_intent': intent,
                'last_entities': entities,
                'last_query': query,
            })
            
            # Execute action
            executor = self.action_executors.get(intent, self._execute_general)
            response = executor(query, entities)
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 20 exchanges
            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]
            
            return response
        
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"
    
    # Action executors
    def _execute_youtube(self, query: str, entities: Dict) -> str:
        """Execute YouTube action"""
        try:
            search_query = entities.get('query', '')
            
            if self.engine and hasattr(self.engine, 'registry'):
                # Use YouTube skill from registry
                tools = self.engine.registry.list_tools()
                youtube_tools = [t for t in tools if 'youtube' in t.lower()]
                
                if youtube_tools:
                    result = self.engine.execute_tool(youtube_tools[0], {'query': search_query})
                    return f"🎵 Opening YouTube: {search_query}\n\n{result}"
            
            # Fallback
            import webbrowser
            if search_query:
                url = f"https://www.youtube.com/results?search_query={search_query}"
            else:
                url = "https://www.youtube.com"
            webbrowser.open(url)
            
            return f"🎵 Opening YouTube{': ' + search_query if search_query else ''}!"
        
        except Exception as e:
            return f"❌ YouTube error: {str(e)}"
    
    def _execute_browser(self, query: str, entities: Dict) -> str:
        """Execute browser action"""
        try:
            import webbrowser
            webbrowser.open("https://www.google.com")
            return "🌐 Opening browser!"
        except Exception as e:
            return f"❌ Browser error: {str(e)}"
    
    def _execute_movie(self, query: str, entities: Dict) -> str:
        """Execute movie action"""
        try:
            movie_name = entities.get('movie_name', '')
            
            if self.engine and hasattr(self.engine, 'registry'):
                # Use movie skill from registry
                tools = self.engine.registry.list_tools()
                movie_tools = [t for t in tools if 'movie' in t.lower()]
                
                if movie_tools:
                    result = self.engine.execute_tool(movie_tools[0], {'query': movie_name})
                    return f"🎬 {result}"
            
            return f"🎬 Searching for movie: {movie_name}"
        
        except Exception as e:
            return f"❌ Movie error: {str(e)}"
    
    def _execute_search(self, query: str, entities: Dict) -> str:
        """Execute search action"""
        try:
            search_query = entities.get('query', query)
            
            # Get AI response for informational queries
            if any(keyword in query.lower() for keyword in ['what', 'who', 'how', 'क्या', 'कौन', 'कैसे']):
                ai_response = self.get_ai_response(search_query, self.context)
                return f"🔍 {ai_response}"
            
            # Otherwise open browser search
            import webbrowser
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            
            return f"🔍 Searching for: {search_query}"
        
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def _execute_system(self, query: str, entities: Dict) -> str:
        """Execute system action"""
        try:
            action = entities.get('action', '')
            
            if self.engine and hasattr(self.engine, 'registry'):
                # Use system skill from registry
                tools = self.engine.registry.list_tools()
                system_tools = [t for t in tools if 'system' in t.lower()]
                
                if system_tools:
                    result = self.engine.execute_tool(system_tools[0], {'action': action})
                    return f"⚙️ {result}"
            
            return f"⚙️ System action: {action}"
        
        except Exception as e:
            return f"❌ System error: {str(e)}"
    
    def _execute_file(self, query: str, entities: Dict) -> str:
        """Execute file action"""
        try:
            if self.engine and hasattr(self.engine, 'registry'):
                # Use file skill from registry
                tools = self.engine.registry.list_tools()
                file_tools = [t for t in tools if 'file' in t.lower()]
                
                if file_tools:
                    result = self.engine.execute_tool(file_tools[0], entities)
                    return f"📁 {result}"
            
            return "📁 File operation requested"
        
        except Exception as e:
            return f"❌ File error: {str(e)}"
    
    def _execute_time(self, query: str, entities: Dict) -> str:
        """Execute time action"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%B %d, %Y")
        
        return f"🕐 Current time: {time_str}\n📅 Date: {date_str}"
    
    def _execute_weather(self, query: str, entities: Dict) -> str:
        """Execute weather action"""
        try:
            if self.engine and hasattr(self.engine, 'registry'):
                # Use weather skill from registry
                tools = self.engine.registry.list_tools()
                weather_tools = [t for t in tools if 'weather' in t.lower()]
                
                if weather_tools:
                    result = self.engine.execute_tool(weather_tools[0], entities)
                    return f"🌤️ {result}"
            
            return "🌤️ Weather information requested"
        
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
    
    def _execute_email(self, query: str, entities: Dict) -> str:
        """Execute email action"""
        try:
            if self.engine and hasattr(self.engine, 'registry'):
                # Use email skill from registry
                tools = self.engine.registry.list_tools()
                email_tools = [t for t in tools if 'email' in t.lower()]
                
                if email_tools:
                    result = self.engine.execute_tool(email_tools[0], entities)
                    return f"📧 {result}"
            
            return "📧 Email operation requested"
        
        except Exception as e:
            return f"❌ Email error: {str(e)}"
    
    def _execute_screenshot(self, query: str, entities: Dict) -> str:
        """Execute screenshot action"""
        try:
            if self.engine and hasattr(self.engine, 'registry'):
                # Use screenshot skill from registry
                tools = self.engine.registry.list_tools()
                screenshot_tools = [t for t in tools if 'screenshot' in t.lower()]
                
                if screenshot_tools:
                    result = self.engine.execute_tool(screenshot_tools[0], entities)
                    return f"📸 {result}"
            
            return "📸 Screenshot taken!"
        
        except Exception as e:
            return f"❌ Screenshot error: {str(e)}"
    
    def _execute_general(self, query: str, entities: Dict) -> str:
        """Execute general conversation"""
        try:
            # Get AI response
            response = self.get_ai_response(query, self.context)
            return response
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        self.context.clear()
    
    def get_stats(self) -> Dict:
        """Get agent statistics"""
        return {
            'total_queries': len([e for e in self.conversation_history if e['role'] == 'user']),
            'conversation_length': len(self.conversation_history),
            'last_intent': self.context.get('last_intent', 'none'),
        }

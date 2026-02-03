import os
import json
import time
from ollama import Client
from typing import List, Dict, Any
from core.registry import SkillRegistry
from core.self_healing import self_healing
from core.personal_assistant import personal_assistant

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        """Initialize JARVIS engine with Ollama (local LLM), personal assistant, and self-healing capabilities"""
        self.registry = registry
        self.assistant = personal_assistant
        
        # Initialize Ollama client with error handling
        try:
            # Get Ollama host from environment or use default
            ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            
            self.client = Client(host=ollama_host)
            
            # Test connection and pull model if needed
            try:
                models = self.client.list()
                print(f"✅ Connected to Ollama at {ollama_host}")
                print(f"📦 Available models: {len(models.get('models', []))}")
            except Exception as e:
                print(f"⚠️  Ollama connection issue: {e}")
                print(f"💡 Make sure Ollama is running: ollama serve")
                raise
            
        except Exception as e:
            print(f"❌ Failed to initialize Ollama client: {e}")
            print(f"💡 Install Ollama: curl -fsSL https://ollama.com/install.sh | sh")
            print(f"💡 Start Ollama: ollama serve")
            if self_healing.auto_fix_error(e, "Ollama client initialization"):
                # Retry after fix
                self.client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
            else:
                raise
        
        # Use local model - llama3.2 is fast and efficient
        self.model = os.environ.get("OLLAMA_MODEL", "llama3.2")
        
        # Ensure model is available
        self._ensure_model_available()
        
        # Enhanced system prompt with personality
        self.system_prompt = """You are JARVIS, a highly intelligent and empathetic personal AI assistant - like a real human assistant.

PERSONALITY TRAITS:
- Friendly, helpful, and conversational
- Understand emotions and respond empathetically
- Remember context from previous conversations
- Proactive in offering suggestions
- Natural and human-like in responses
- Speak in the user's language (English/Hindi/Hinglish)

IMPORTANT INSTRUCTIONS:

1. YouTube Commands:
   - "youtube kholo" → use play_youtube with empty query (will auto-play trending music)
   - "youtube kholo aur music play karo" → use play_youtube with empty query
   - "youtube kholo aur gaana bajao" → use play_youtube with empty query
   - "play X on youtube" → use play_youtube with query="X"
   - When play_youtube is called with empty query, it automatically plays a trending song

2. Website Commands:
   - "open google" → use open_website with url "https://google.com"
   - "search X on google" → use google_search tool
   - "open website X" → use open_website with url

3. Music Commands:
   - "gaana bajao" or "music play karo" → use play_music or play_youtube (both work)
   - "play X song" → use play_youtube with query="X"
   - Both play_youtube and play_music can auto-select trending songs

4. Movie Download Commands:
   - "download movie X from website Y" → use download_and_play_movie
   - Example: "vegamovies se Inception download karo" → download_and_play_movie(movie_name="Inception", website_url="https://vegamovies.attorney/")
   - Automatically downloads and plays in VLC

5. Conversation Rules:
   - Detect user's emotion (happy, sad, frustrated, excited) and respond appropriately
   - Remember previous tasks and context
   - Handle follow-up questions naturally
   - Be proactive - suggest related actions
   - Confirm actions with natural language, not robotic responses
   - Use emojis when appropriate to add warmth
   - If user says "thanks", respond warmly
   - If user is frustrated, be understanding and helpful

6. Response Style:
   - Keep responses concise but warm
   - Use natural language, not technical jargon
   - Match the user's language and tone
   - Add personality - be friendly, not robotic
   - Example: Instead of "Task completed", say "Done! Anything else I can help with?"

Available tools will be provided in the function calling format."""
        
        self.conversation_history = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]
        self.max_iterations = 5

    def _ensure_model_available(self):
        """Ensure the model is pulled and available"""
        try:
            models = self.client.list()
            model_names = [m.get('name', '') for m in models.get('models', [])]
            
            if not any(self.model in name for name in model_names):
                print(f"📥 Pulling model {self.model}... (this may take a few minutes)")
                self.client.pull(self.model)
                print(f"✅ Model {self.model} ready!")
            else:
                print(f"✅ Using model: {self.model}")
        except Exception as e:
            print(f"⚠️  Model check failed: {e}")
            print(f"💡 Manually pull model: ollama pull {self.model}")

    def process_query(self, user_query: str) -> str:
        """
        Process user query with personal assistant intelligence
        """
        # First, let personal assistant analyze the query
        analysis = self.assistant.process_conversation(user_query)
        
        # Handle special cases
        if self._is_greeting(user_query):
            response = self.assistant.get_personality_response('greeting')
            self.assistant.add_to_history(user_query, response)
            return response
        
        if self._is_thanks(user_query):
            response = self.assistant.get_personality_response('thanks')
            self.assistant.add_to_history(user_query, response)
            return response
        
        if self._is_goodbye(user_query):
            response = self.assistant.get_personality_response('goodbye')
            self.assistant.add_to_history(user_query, response)
            return response
        
        # If it's a simple yes/no clarification
        if self._is_clarification(user_query):
            response = self.assistant.handle_clarification(user_query)
            self.assistant.add_to_history(user_query, response)
            return response
        
        # If action is needed, execute with LLM
        if analysis['action_needed']:
            # Add empathetic acknowledgment
            print(f"\n{analysis['response']}\n")
            
            # Execute the actual task
            result = self.run_conversation(user_query)
            
            # Add natural follow-up
            emotion = analysis['emotion']
            if emotion == "happy":
                result += "\n\n😊 Glad I could help! Anything else?"
            elif emotion == "frustrated":
                result += "\n\nI hope this helps! Let me know if you need anything else."
            else:
                result += "\n\nDone! What else can I do for you?"
            
            return result
        
        # For pure conversation, use LLM
        return self.run_conversation(user_query)
    
    def _is_greeting(self, text: str) -> bool:
        """Check if text is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'namaste', 'namaskar', 'good morning', 
                     'good afternoon', 'good evening', 'jarvis']
        return any(g in text.lower() for g in greetings) and len(text.split()) <= 3
    
    def _is_thanks(self, text: str) -> bool:
        """Check if text is a thank you"""
        thanks = ['thanks', 'thank you', 'shukriya', 'dhanyavaad', 'appreciate']
        return any(t in text.lower() for t in thanks)
    
    def _is_goodbye(self, text: str) -> bool:
        """Check if text is a goodbye"""
        goodbyes = ['bye', 'goodbye', 'see you', 'alvida', 'tata', 'exit', 'quit']
        return any(g in text.lower() for g in goodbyes)
    
    def _is_clarification(self, text: str) -> bool:
        """Check if text is a yes/no clarification"""
        clarifications = ['yes', 'no', 'haan', 'nahi', 'yeah', 'nope', 'ok', 'okay']
        return text.lower().strip() in clarifications

    def run_conversation(self, user_query: str) -> str:
        """
        Run a conversation with self-healing error handling.
        Automatically recovers from errors and retries.
        """
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                return self._execute_conversation(user_query)
            except AttributeError as e:
                # Special handling for AttributeError - these are code issues
                error_msg = str(e)
                
                if "get_all_tools" in error_msg or "SkillRegistry" in error_msg:
                    print(f"\n🔧 Code update detected! Restarting required...")
                    print(f"   Issue: {error_msg}")
                    print(f"\n✅ Fix applied! Please restart JARVIS:")
                    print(f"   python main.py\n")
                    return "System update hua hai. Please restart JARVIS: python main.py"
                
                # Log but don't show to user
                self_healing.log_error(e, f"AttributeError in conversation: {user_query}")
                retry_count += 1
                
                if retry_count < max_retries:
                    print(f"🔄 Retrying... ({retry_count}/{max_retries})")
                    time.sleep(1)
                else:
                    return self._fallback_simple_conversation(user_query)
                    
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️  Conversation error: {error_msg}")
                
                # Try to auto-fix
                if self_healing.auto_fix_error(e, f"Conversation: {user_query}"):
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"🔄 Retrying... ({retry_count}/{max_retries})")
                        time.sleep(1)
                    else:
                        print(f"❌ Maximum retries reached.")
                        return "Sorry, couldn't process your request. Please try again."
                else:
                    return self._fallback_simple_conversation(user_query)
        
        return "Sorry, couldn't process your request. Please try again."

    def _fallback_simple_conversation(self, user_query: str) -> str:
        """Fallback to simple conversation without tools when errors occur"""
        try:
            print("🔄 Using simple conversation mode (no tools)...")
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are JARVIS, a helpful and friendly AI assistant. Answer the user's question directly and warmly."
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
            )
            return response['message']['content'] or "I'm here to help! What do you need?"
        except Exception as e:
            print(f"⚠️  Simple conversation also failed: {e}")
            return "Sorry, I couldn't process that request. Please try again."

    def _execute_conversation(self, user_query: str) -> str:
        """Internal method to execute conversation logic"""
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })

        # Get all available tools with error handling
        try:
            tools = self.registry.get_all_tools()
        except AttributeError as e:
            # Fallback to alternative method
            try:
                tools = self.registry.get_tools_schema()
            except:
                print(f"⚠️  Registry method missing. Using empty tools.")
                tools = []
        
        # Validate tools format
        if tools:
            tools = self._validate_tools_format(tools)
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            try:
                # Call LLM with error handling
                response = self._call_llm_with_retry(tools)
                
                # Process response - Ollama format is different from Groq
                assistant_message = response.get('message', {})
                
                # Handle tool calls in Ollama format
                tool_calls = assistant_message.get('tool_calls', None)
                
                # Build assistant message dict
                assistant_msg = {
                    "role": "assistant",
                    "content": assistant_message.get('content', "")
                }
                
                # Only add tool_calls if they exist
                if tool_calls:
                    assistant_msg["tool_calls"] = tool_calls
                
                self.conversation_history.append(assistant_msg)

                # Check if done
                if not tool_calls:
                    return assistant_message.get('content', "Done! Anything else?")

                # Execute tool calls with error handling
                self._execute_tool_calls_with_healing(tool_calls)
                
            except Exception as e:
                print(f"⚠️  Iteration {iteration} error: {e}")
                if not self_healing.auto_fix_error(e, f"LLM iteration {iteration}"):
                    raise

        return "Request processed! What else can I help with?"

    def _validate_tools_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and fix tools format to prevent errors"""
        validated_tools = []
        for tool in tools:
            if isinstance(tool, dict) and 'type' in tool and 'function' in tool:
                validated_tools.append(tool)
        return validated_tools

    def _call_llm_with_retry(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Call LLM with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=tools if tools else None
                )
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"🔄 LLM call failed, retrying... ({attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    raise

    def _execute_tool_calls_with_healing(self, tool_calls: List[Dict[str, Any]]):
        """Execute tool calls with self-healing"""
        for tool_call in tool_calls:
            try:
                function_name = tool_call['function']['name']
                
                # Handle both dict and JSON string arguments from Ollama
                arguments = tool_call['function']['arguments']
                if isinstance(arguments, str):
                    function_args = json.loads(arguments)
                elif isinstance(arguments, dict):
                    function_args = arguments
                else:
                    function_args = {}
                
                # Execute function
                result = self.registry.execute_skill(function_name, function_args)
                
                # Add result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(result) if result else "Success"
                })
                
            except Exception as e:
                error_msg = f"Error executing {function_name}: {str(e)}"
                print(f"⚠️  {error_msg}")
                
                # Try to auto-fix
                if self_healing.auto_fix_error(e, f"Tool execution: {function_name}"):
                    # Retry
                    try:
                        result = self.registry.execute_skill(function_name, function_args)
                        self.conversation_history.append({
                            "role": "tool",
                            "content": json.dumps(result) if result else "Success"
                        })
                    except:
                        self.conversation_history.append({
                            "role": "tool",
                            "content": f"Error: {error_msg}"
                        })
                else:
                    self.conversation_history.append({
                        "role": "tool",
                        "content": f"Error: {error_msg}"
                    })

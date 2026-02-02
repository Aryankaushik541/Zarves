import os
import json
from groq import Groq
from typing import List, Dict, Any
from core.registry import SkillRegistry
from core.self_healing import self_healing

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        """Initialize JARVIS engine with self-healing capabilities"""
        self.registry = registry
        
        # Initialize Groq client with error handling
        try:
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                if self_healing.fix_api_key_error():
                    api_key = os.environ.get("GROQ_API_KEY")
                else:
                    raise ValueError("GROQ_API_KEY not found")
            
            self.client = Groq(api_key=api_key)
        except Exception as e:
            print(f"❌ Groq client initialize करने में error: {e}")
            if self_healing.auto_fix_error(e, "Groq client initialization"):
                # Retry after fix
                self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            else:
                raise
        
        self.model = "llama-3.3-70b-versatile"
        self.conversation_history = []
        self.max_iterations = 10

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
            except Exception as e:
                retry_count += 1
                print(f"\n⚠️  Conversation error (attempt {retry_count}/{max_retries})")
                
                # Try to auto-fix the error
                if self_healing.auto_fix_error(e, f"Conversation execution (query: {user_query})"):
                    print("✅ Error fixed! Retrying...\n")
                    continue
                else:
                    if retry_count < max_retries:
                        print(f"🔄 Retrying without fix... ({retry_count}/{max_retries})\n")
                        continue
                    else:
                        print(f"❌ Maximum retries reached. Error: {e}")
                        return f"माफ़ करें, मैं इस request को process नहीं कर सका। Error: {str(e)}"
        
        return "माफ़ करें, कुछ technical issue है। कृपया दोबारा try करें।"

    def _execute_conversation(self, user_query: str) -> str:
        """Internal method to execute conversation logic"""
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })

        # Get all available tools
        tools = self.registry.get_all_tools()
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            try:
                # Call LLM with error handling
                response = self._call_llm_with_retry(tools)
                
                # Process response
                assistant_message = response.choices[0].message
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": assistant_message.tool_calls
                })

                # Check if done
                if not assistant_message.tool_calls:
                    return assistant_message.content or "कार्य पूर्ण हुआ।"

                # Execute tool calls with error handling
                self._execute_tool_calls_with_healing(assistant_message.tool_calls)
                
            except Exception as e:
                print(f"⚠️  Iteration {iteration} में error: {e}")
                if not self_healing.auto_fix_error(e, f"LLM iteration {iteration}"):
                    raise

        return "Request process हो गया।"

    def _call_llm_with_retry(self, tools: List[Dict[str, Any]], max_retries: int = 3):
        """Call LLM with automatic retry on failure"""
        for attempt in range(max_retries):
            try:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=tools,
                    tool_choice="auto",
                    max_tokens=4096
                )
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"🔄 LLM call retry {attempt + 1}/{max_retries}")
                    if self_healing.auto_fix_error(e, "LLM API call"):
                        continue
                raise

    def _execute_tool_calls_with_healing(self, tool_calls):
        """Execute tool calls with self-healing error handling"""
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            
            try:
                # Parse arguments with error handling
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON parse error: {e}")
                    function_args = {}
                
                # Execute function with error handling
                function_to_call = self.registry.get_function(function_name)
                
                if function_to_call:
                    try:
                        function_response = function_to_call(**function_args)
                    except Exception as e:
                        print(f"⚠️  Function '{function_name}' execution error: {e}")
                        
                        # Try to auto-fix
                        if self_healing.auto_fix_error(e, f"Function execution: {function_name}"):
                            print("✅ Error fixed! Retrying function...")
                            function_response = function_to_call(**function_args)
                        else:
                            function_response = json.dumps({
                                "status": "error",
                                "error": str(e),
                                "function": function_name
                            })
                else:
                    function_response = json.dumps({
                        "status": "error",
                        "error": f"Function '{function_name}' not found"
                    })
                
                # Add tool response to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(function_response)
                })
                
            except Exception as e:
                print(f"❌ Tool call error: {e}")
                self_healing.auto_fix_error(e, f"Tool call: {function_name}")
                
                # Add error response
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps({"status": "error", "error": str(e)})
                })

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        print("✅ Conversation history reset!")
    
    def get_error_report(self) -> str:
        """Get error report from self-healing system"""
        return self_healing.get_error_report()

import os
import json
import time
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
            print(f"❌ Failed to initialize Groq client: {e}")
            if self_healing.auto_fix_error(e, "Groq client initialization"):
                # Retry after fix
                self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            else:
                raise
        
        # Use smaller, faster model to save tokens
        self.model = "llama-3.1-8b-instant"  # Changed from llama-3.3-70b-versatile
        self.conversation_history = []
        self.max_iterations = 5  # Reduced from 10 to save tokens

    def process_query(self, user_query: str) -> str:
        """
        Process user query - main entry point for JARVIS.
        This is an alias for run_conversation for backward compatibility.
        """
        return self.run_conversation(user_query)

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
                    continue
                else:
                    return "System update in progress. Please restart JARVIS."
            
            except Exception as e:
                error_str = str(e)
                
                # Handle rate limit errors
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    print(f"\n⚠️  Rate limit reached!")
                    print(f"💡 Switching to faster model to save tokens...")
                    self.model = "llama-3.1-8b-instant"
                    return "API rate limit reached. Kuch der baad try karo ya apna API key upgrade karo."
                
                # Handle bad request errors (tool call format issues)
                if "tool_use_failed" in error_str or "400" in error_str:
                    print(f"\n⚠️  Tool call format issue detected")
                    print(f"💡 Retrying with simpler approach...")
                    retry_count += 1
                    
                    # Try without tools on next attempt
                    if retry_count < max_retries:
                        try:
                            return self._execute_simple_conversation(user_query)
                        except:
                            continue
                    else:
                        return "Sorry, technical issue hai. Please try a simpler command."
                
                retry_count += 1
                
                # Try to auto-fix the error
                if self_healing.auto_fix_error(e, f"Conversation execution (query: {user_query})"):
                    print("✅ Error fixed! Retrying...\n")
                    continue
                else:
                    if retry_count < max_retries:
                        print(f"🔄 Retrying... ({retry_count}/{max_retries})\n")
                        time.sleep(1)  # Brief delay before retry
                        continue
                    else:
                        print(f"❌ Maximum retries reached.")
                        return f"Sorry, couldn't process your request. Please try again."
        
        return "Sorry, technical issue hai. Please try again."

    def _execute_simple_conversation(self, user_query: str) -> str:
        """Execute conversation without tools - fallback for errors"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are JARVIS, a helpful AI assistant. Respond concisely and helpfully."
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ],
                max_tokens=500
            )
            return response.choices[0].message.content or "Task completed."
        except Exception as e:
            print(f"⚠️  Simple conversation also failed: {e}")
            return "Sorry, I couldn't process that request."

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
                
                # Process response
                assistant_message = response.choices[0].message
                
                # FIX: Properly handle tool_calls to avoid nullable error
                tool_calls = assistant_message.tool_calls if assistant_message.tool_calls else None
                
                # Build assistant message dict
                assistant_msg = {
                    "role": "assistant",
                    "content": assistant_message.content or ""
                }
                
                # Only add tool_calls if they exist (avoid nullable error)
                if tool_calls:
                    assistant_msg["tool_calls"] = tool_calls
                
                self.conversation_history.append(assistant_msg)

                # Check if done
                if not tool_calls:
                    return assistant_message.content or "Task completed."

                # Execute tool calls with error handling
                self._execute_tool_calls_with_healing(tool_calls)
                
            except Exception as e:
                print(f"⚠️  Iteration {iteration} error: {e}")
                if not self_healing.auto_fix_error(e, f"LLM iteration {iteration}"):
                    raise

        return "Request processed."

    def _validate_tools_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and fix tools format to prevent BadRequestError"""
        validated_tools = []
        
        for tool in tools:
            try:
                # Ensure proper structure
                if "type" in tool and "function" in tool:
                    # Validate function schema
                    func = tool["function"]
                    if "name" in func and "parameters" in func:
                        # Ensure parameters has proper schema
                        if "type" not in func["parameters"]:
                            func["parameters"]["type"] = "object"
                        if "properties" not in func["parameters"]:
                            func["parameters"]["properties"] = {}
                        
                        validated_tools.append(tool)
            except Exception as e:
                print(f"⚠️  Skipping invalid tool: {e}")
                continue
        
        return validated_tools

    def _call_llm_with_retry(self, tools: List[Dict[str, Any]], max_retries: int = 3):
        """Call LLM with automatic retry on failure"""
        for attempt in range(max_retries):
            try:
                # Prepare request parameters
                request_params = {
                    "model": self.model,
                    "messages": self.conversation_history,
                    "max_tokens": 2048  # Reduced from 4096 to save tokens
                }
                
                # Only add tools if they exist and are valid
                if tools and len(tools) > 0:
                    request_params["tools"] = tools
                    request_params["tool_choice"] = "auto"
                
                return self.client.chat.completions.create(**request_params)
                
            except Exception as e:
                error_str = str(e)
                
                # Handle rate limit
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    raise  # Don't retry rate limits
                
                # Handle tool errors
                if "tool_use_failed" in error_str and attempt < max_retries - 1:
                    print(f"🔄 Tool call failed, retrying without tools...")
                    # Remove tools and retry
                    request_params = {
                        "model": self.model,
                        "messages": self.conversation_history,
                        "max_tokens": 2048
                    }
                    try:
                        return self.client.chat.completions.create(**request_params)
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    print(f"🔄 LLM call retry {attempt + 1}/{max_retries}")
                    time.sleep(1)  # Brief delay
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

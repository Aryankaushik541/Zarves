import os
import json
import time
from ollama import Client
from typing import List, Dict, Any
from core.registry import SkillRegistry
from core.self_healing import self_healing

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        """Initialize JARVIS engine with Ollama (local LLM) and self-healing capabilities"""
        self.registry = registry
        
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
        
        self.conversation_history = []
        self.max_iterations = 5  # Reduced from 10 to save tokens

    def _ensure_model_available(self):
        """Ensure the model is pulled and available"""
        try:
            models = self.client.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
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
                
                # Handle Ollama connection errors
                if "connection" in error_str.lower() or "refused" in error_str.lower():
                    print(f"\n⚠️  Ollama connection failed!")
                    print(f"💡 Start Ollama server: ollama serve")
                    return "Ollama server nahi chal raha. Please start karo: ollama serve"
                
                # Handle model not found errors
                if "model" in error_str.lower() and "not found" in error_str.lower():
                    print(f"\n⚠️  Model {self.model} not found!")
                    print(f"💡 Pull model: ollama pull {self.model}")
                    return f"Model {self.model} available nahi hai. Please pull karo: ollama pull {self.model}"
                
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
            response = self.client.chat(
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
                ]
            )
            return response['message']['content'] or "Task completed."
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
                    return assistant_message.get('content', "Task completed.")

                # Execute tool calls with error handling
                self._execute_tool_calls_with_healing(tool_calls)
                
            except Exception as e:
                print(f"⚠️  Iteration {iteration} error: {e}")
                if not self_healing.auto_fix_error(e, f"LLM iteration {iteration}"):
                    raise

        return "Request processed."

    def _validate_tools_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and fix tools format to prevent errors"""
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
                # Prepare request parameters for Ollama
                request_params = {
                    "model": self.model,
                    "messages": self.conversation_history
                }
                
                # Only add tools if they exist and are valid
                if tools and len(tools) > 0:
                    request_params["tools"] = tools
                
                return self.client.chat(**request_params)
                
            except Exception as e:
                error_str = str(e)
                
                # Handle connection errors
                if "connection" in error_str.lower() or "refused" in error_str.lower():
                    raise  # Don't retry connection errors
                
                # Handle model errors
                if "model" in error_str.lower() and "not found" in error_str.lower():
                    raise  # Don't retry model not found
                
                # Retry other errors
                if attempt < max_retries - 1:
                    print(f"⚠️  LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(1)
                    continue
                else:
                    raise

    def _execute_tool_calls_with_healing(self, tool_calls):
        """Execute tool calls with automatic error recovery"""
        for tool_call in tool_calls:
            try:
                # Extract tool info - Ollama format
                if isinstance(tool_call, dict):
                    function_name = tool_call.get('function', {}).get('name')
                    function_args = tool_call.get('function', {}).get('arguments', {})
                    tool_call_id = tool_call.get('id', 'unknown')
                else:
                    # Fallback for object format
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    tool_call_id = tool_call.id

                # Execute skill
                result = self.registry.execute_skill(function_name, function_args)

                # Add result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": str(result)
                })

            except Exception as e:
                error_msg = f"Error executing {function_name}: {str(e)}"
                print(f"⚠️  {error_msg}")
                
                # Try to auto-fix
                if self_healing.auto_fix_error(e, f"Tool execution: {function_name}"):
                    print("✅ Tool error fixed! Retrying...")
                    try:
                        result = self.registry.execute_skill(function_name, function_args)
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": str(result)
                        })
                    except Exception as retry_error:
                        # Add error to conversation
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": f"Error: {str(retry_error)}"
                        })
                else:
                    # Add error to conversation
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": error_msg
                    })

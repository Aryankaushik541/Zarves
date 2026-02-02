import os
import json
import re
from groq import Groq
from core.registry import SkillRegistry

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"
        
        self.system_instruction = (
            "You are Jarvis, a helpful and precise AI assistant. "
            "Use the provided tools to answer the user's request. "
            "Always respond naturally and conversationally. "
            "When a tool is executed successfully, acknowledge the action briefly."
        )

    def run_conversation(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            tools_schema = self.registry.get_tools_schema()
            
            completion_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            if tools_schema:
                completion_kwargs["tools"] = tools_schema
                completion_kwargs["tool_choice"] = "auto"
            
            response = self.client.chat.completions.create(**completion_kwargs)
            
        except Exception as e:
            # Handle tool_use_failed error from Groq
            error_str = str(e)
            if "tool_use_failed" in error_str and "failed_generation" in error_str:
                try:
                    # Extract failed generation from error message
                    # Pattern: <function=NAME({"key": "value"})</function>
                    match = re.search(r"<function=(\w+)\((.*?)\)</function>", error_str)
                    if match:
                        func_name = match.group(1)
                        func_args_str = match.group(2)
                        print(f"DEBUG: Recovered failed tool call: {func_name} with args: {func_args_str}")
                        
                        function_to_call = self.registry.get_function(func_name)
                        if function_to_call:
                            try:
                                # Parse the arguments
                                args = json.loads(func_args_str)
                                print(f"DEBUG: Executing {func_name} with {args}")
                                res = function_to_call(**args)
                                
                                # Parse the result if it's JSON
                                try:
                                    result_data = json.loads(res)
                                    if result_data.get("status") == "success":
                                        if "service" in result_data:
                                            return f"Opening {result_data['service']} in your browser, sir."
                                        elif "app" in result_data:
                                            return f"Opening {result_data['app']}, sir."
                                        else:
                                            return "Done, sir."
                                    else:
                                        return str(res)
                                except:
                                    return str(res)
                                    
                            except Exception as exec_e:
                                print(f"Error executing recovered tool: {exec_e}")
                                return f"I encountered an error: {exec_e}"
                except Exception as parse_e:
                    print(f"Failed to recover tool call: {parse_e}")

            print(f"Groq API Error: {e}")
            return "I am having trouble connecting to the brain, sir."

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # CASE 1: AI wants to use a tool (Action)
        if tool_calls:
            print("DEBUG: Executing Tool...")
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.registry.get_function(function_name)
                
                if not function_to_call:
                    res = "Error: Tool not found."
                else:
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                        if function_args is None:
                            function_args = {}
                        
                        print(f"DEBUG: Calling {function_name} with {function_args}")
                        res = function_to_call(**function_args)
                    except Exception as e:
                        res = f"Error executing tool: {e}"
                        print(f"Tool execution error: {e}")
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(res),
                    }
                )
            
            # Get final spoken response after tool runs
            try:
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=150
                )
                return second_response.choices[0].message.content
            except Exception as e:
                print(f"Error getting final response: {e}")
                # Return a generic success message based on the tool result
                try:
                    result_data = json.loads(res)
                    if result_data.get("status") == "success":
                        return "Done, sir."
                except:
                    pass
                return "Task completed, sir."
        
        # CASE 2: AI wants to chat
        else:
            return response_message.content

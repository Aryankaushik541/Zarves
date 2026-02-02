import os
import json
import re
import webbrowser
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
        
        # Web services mapping
        self.web_services = {
            "youtube": "https://www.youtube.com",
            "gmail": "https://mail.google.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "reddit": "https://www.reddit.com",
            "github": "https://www.github.com",
            "linkedin": "https://www.linkedin.com",
            "netflix": "https://www.netflix.com",
            "spotify": "https://open.spotify.com",
            "amazon": "https://www.amazon.com",
            "whatsapp": "https://web.whatsapp.com",
            "discord": "https://discord.com",
            "slack": "https://slack.com",
        }

    def handle_direct_command(self, query: str) -> tuple[bool, str]:
        """
        Handle direct commands without AI processing for reliability.
        Returns (handled: bool, response: str)
        """
        query_lower = query.lower().strip()
        
        # Handle "open X" commands
        if query_lower.startswith("open "):
            target = query_lower.replace("open ", "").strip()
            
            # Check if it's a web service
            for service, url in self.web_services.items():
                if service in target:
                    try:
                        webbrowser.open(url)
                        return True, f"Opening {service.title()}, sir."
                    except Exception as e:
                        return True, f"Error opening {service}: {e}"
            
            # Try to open as macOS app
            try:
                os.system(f"open -a '{target.title()}'")
                return True, f"Opening {target.title()}, sir."
            except Exception as e:
                return True, f"I couldn't open {target}, sir."
        
        # Handle "search X" commands
        if query_lower.startswith("search ") or "search for" in query_lower:
            search_term = query_lower.replace("search for", "").replace("search", "").strip()
            try:
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                return True, f"Searching for {search_term}, sir."
            except Exception as e:
                return True, f"Error searching: {e}"
        
        # Handle volume commands
        volume_match = re.search(r"volume (\d+)", query_lower)
        if volume_match or "set volume" in query_lower:
            try:
                level = int(volume_match.group(1)) if volume_match else 50
                os.system(f"osascript -e 'set volume output volume {level}'")
                return True, f"Volume set to {level}, sir."
            except Exception as e:
                return True, f"Error setting volume: {e}"
        
        return False, ""

    def run_conversation(self, user_prompt: str) -> str:
        # First try direct command handling
        handled, response = self.handle_direct_command(user_prompt)
        if handled:
            return response
        
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
                                            return f"Opening {result_data['service']}, sir."
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

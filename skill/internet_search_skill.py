"""
Internet Search Skill - Real-time web data collection
Connects JARVIS to the internet for live information
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any

class InternetSearchSkill:
    """Real-time internet search and data collection"""
    
    def __init__(self):
        self.name = "internet_search_skill"
        self.description = "Search the internet for real-time information"
        
    def get_tools(self):
        """Return tool definitions for LLM"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the internet for real-time information, news, facts, or any current data. Use this for questions about current events, latest information, or anything that requires up-to-date knowledge.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query (e.g., 'latest news', 'weather today', 'Bitcoin price')"
                            },
                            "depth": {
                                "type": "string",
                                "enum": ["quick", "standard", "deep"],
                                "description": "Search depth: 'quick' for simple facts, 'standard' for balanced research, 'deep' for comprehensive analysis",
                                "default": "standard"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_webpage_content",
                    "description": "Fetch and extract content from a specific webpage URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL of the webpage to fetch"
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_youtube",
                    "description": "Search YouTube for videos on any topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "What to search for on YouTube"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Number of results to return (default: 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def search_web(self, query: str, depth: str = "standard") -> str:
        """
        Search the web using DuckDuckGo (no API key needed)
        Returns real-time search results
        """
        try:
            # Use DuckDuckGo Instant Answer API (free, no key needed)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Extract relevant information
            results = []
            
            # Abstract (main answer)
            if data.get("Abstract"):
                results.append(f"📌 {data['Abstract']}")
            
            # Related topics
            if data.get("RelatedTopics"):
                results.append("\n🔍 Related Information:")
                for i, topic in enumerate(data["RelatedTopics"][:5], 1):
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append(f"{i}. {topic['Text']}")
            
            # Answer (if available)
            if data.get("Answer"):
                results.append(f"\n✅ Answer: {data['Answer']}")
            
            if results:
                return "\n".join(results)
            else:
                # Fallback: Try Google search scraping
                return self._fallback_google_search(query)
                
        except Exception as e:
            return f"❌ Search failed: {str(e)}\n💡 Try: 'open google and search {query}'"
    
    def _fallback_google_search(self, query: str) -> str:
        """Fallback to basic Google search scraping"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            url = f"https://www.google.com/search?q={query}"
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract featured snippet
            featured = soup.find('div', class_='BNeawe')
            if featured:
                return f"📌 {featured.get_text()}"
            
            # Extract search results
            results = []
            for g in soup.find_all('div', class_='g')[:3]:
                title = g.find('h3')
                snippet = g.find('div', class_='VwiC3b')
                if title and snippet:
                    results.append(f"• {title.get_text()}\n  {snippet.get_text()}")
            
            if results:
                return "🔍 Search Results:\n" + "\n\n".join(results)
            else:
                return f"💡 Please open Google manually: 'open google and search {query}'"
                
        except Exception as e:
            return f"💡 Please use: 'open google and search {query}'"
    
    def get_webpage_content(self, url: str) -> str:
        """Fetch and extract text content from a webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit length
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            return f"📄 Content from {url}:\n\n{text}"
            
        except Exception as e:
            return f"❌ Failed to fetch webpage: {str(e)}"
    
    def search_youtube(self, query: str, max_results: int = 5) -> str:
        """Search YouTube videos (using web scraping)"""
        try:
            import urllib.parse
            
            # Encode query
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # Extract video IDs from response
            import re
            video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
            
            if video_ids:
                results = [f"🎥 Found {len(video_ids[:max_results])} videos for '{query}':\n"]
                for i, vid_id in enumerate(video_ids[:max_results], 1):
                    video_url = f"https://www.youtube.com/watch?v={vid_id}"
                    results.append(f"{i}. {video_url}")
                
                return "\n".join(results)
            else:
                return f"💡 Opening YouTube search for: {query}"
                
        except Exception as e:
            return f"💡 Opening YouTube to search: {query}"
    
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Execute the requested function"""
        if function_name == "search_web":
            return self.search_web(
                query=arguments.get("query", ""),
                depth=arguments.get("depth", "standard")
            )
        elif function_name == "get_webpage_content":
            return self.get_webpage_content(url=arguments.get("url", ""))
        elif function_name == "search_youtube":
            return self.search_youtube(
                query=arguments.get("query", ""),
                max_results=arguments.get("max_results", 5)
            )
        else:
            return f"Unknown function: {function_name}"

# Create skill instance
skill = InternetSearchSkill()

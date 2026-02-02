import webbrowser
import json
import sys
import random
from typing import List, Dict, Any, Callable
from core.skill import Skill

class MusicSkill(Skill):
    """
    Music playback skill optimized for Hindi songs and Indian music
    Supports natural language commands like "play music", "gaana bajao", etc.
    """
    
    # Popular Hindi songs for random playback
    POPULAR_HINDI_SONGS = [
        "Tum Hi Ho Aashiqui 2",
        "Kesariya Brahmastra",
        "Apna Bana Le Bhediya",
        "Chaleya Jawan",
        "Maan Meri Jaan King",
        "Kahani Suno 2.0",
        "Satranga Animal",
        "Arjan Vailly Animal",
        "Hua Main Animal",
        "O Maahi Dunki",
        "Tauba Tauba Bad Newz",
        "Pehle Bhi Main Vishal Mishra",
        "Tere Vaaste Zara Hatke Zara Bachke",
        "Ve Kamleya Rocky Aur Rani",
        "What Jhumka Arijit Singh",
        "Tum Kya Mile Pritam",
        "Heeriye Jasleen Royal",
        "Besharam Rang Pathaan",
        "Jhoome Jo Pathaan",
        "Naina Arijit Singh",
    ]
    
    @property
    def name(self) -> str:
        return "music_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "play_music",
                    "description": "Play music on YouTube. Supports Hindi songs, English songs, or any music request. Use this for commands like 'play music', 'gaana bajao', 'song sunao', etc.",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "query": {
                                "type": "string",
                                "description": "Song name, artist, or music type. If empty or 'random', plays a popular Hindi song. Examples: 'Kesariya', 'Arijit Singh songs', 'romantic songs', 'latest Hindi songs'"
                            },
                            "language": {
                                "type": "string",
                                "description": "Language preference: 'hindi', 'english', 'punjabi', 'tamil', etc. Default is 'hindi'",
                                "default": "hindi"
                            }
                        }, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_hindi_song",
                    "description": "Play a specific Hindi song or a random popular Hindi song",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "song_name": {
                                "type": "string",
                                "description": "Hindi song name or artist. Leave empty for random popular song"
                            }
                        }, 
                        "required": [] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "play_playlist",
                    "description": "Play a music playlist or mix on YouTube",
                    "parameters": { 
                        "type": "object", 
                        "properties": { 
                            "playlist_type": {
                                "type": "string",
                                "description": "Type of playlist: 'romantic', 'party', 'sad', 'workout', 'bollywood hits', 'latest', etc."
                            },
                            "language": {
                                "type": "string",
                                "description": "Language: 'hindi', 'english', 'punjabi', etc.",
                                "default": "hindi"
                            }
                        }, 
                        "required": ["playlist_type"] 
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "play_music": self.play_music,
            "play_hindi_song": self.play_hindi_song,
            "play_playlist": self.play_playlist
        }

    def play_music(self, query="", language="hindi"):
        """
        Play music on YouTube with smart defaults
        """
        try:
            # If no query, play random popular Hindi song
            if not query or query.lower() in ["random", "kuch bhi", "anything", "surprise me"]:
                song = random.choice(self.POPULAR_HINDI_SONGS)
                print(f"🎵 Playing random Hindi song: {song}")
                return self._play_on_youtube(song)
            
            # Add language context if specified
            if language and language.lower() != "hindi":
                search_query = f"{query} {language} song"
            else:
                search_query = f"{query} hindi song"
            
            print(f"🎵 Playing: {search_query}")
            return self._play_on_youtube(search_query)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def play_hindi_song(self, song_name=""):
        """
        Play a Hindi song or random popular song
        """
        try:
            if not song_name:
                song = random.choice(self.POPULAR_HINDI_SONGS)
                print(f"🎵 Playing random Hindi song: {song}")
            else:
                song = f"{song_name} hindi song"
                print(f"🎵 Playing: {song}")
            
            return self._play_on_youtube(song)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def play_playlist(self, playlist_type, language="hindi"):
        """
        Play a music playlist/mix
        """
        try:
            search_query = f"{playlist_type} {language} songs playlist"
            print(f"🎵 Playing playlist: {search_query}")
            return self._play_on_youtube(search_query)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def _play_on_youtube(self, query):
        """
        Internal method to play on YouTube with fallback support
        """
        try:
            # Try pywhatkit first (better auto-play)
            import pywhatkit as kit
            import time
            
            print(f"🔍 Searching YouTube: {query}")
            
            # Platform-specific handling
            if sys.platform == "win32":  # Windows
                kit.playonyt(query, open_web=True)
                time.sleep(2)
            elif sys.platform == "darwin":  # macOS
                kit.playonyt(query, open_web=True)
                time.sleep(2)
            else:  # Linux
                kit.playonyt(query, open_web=True)
                time.sleep(2)
            
            return json.dumps({
                "status": "success", 
                "action": "play_music", 
                "query": query,
                "platform": sys.platform
            })
            
        except ImportError:
            # Fallback to webbrowser
            print("⚠️  pywhatkit not found, using browser fallback...")
            try:
                search_query = query.replace(' ', '+')
                url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open(url)
                return json.dumps({
                    "status": "success", 
                    "action": "play_music_fallback", 
                    "query": query,
                    "note": "Install pywhatkit for better playback: pip install pywhatkit"
                })
            except Exception as e:
                return json.dumps({"status": "error", "error": str(e)})
                
        except Exception as e:
            print(f"❌ YouTube Error: {e}")
            # Final fallback
            try:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)
                return json.dumps({
                    "status": "partial_success", 
                    "action": "youtube_search", 
                    "query": query,
                    "error": str(e)
                })
            except Exception as e2:
                return json.dumps({"status": "error", "error": str(e2)})

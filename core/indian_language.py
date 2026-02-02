"""
Indian Language Support for JARVIS
Understands natural Indian English, Hinglish, and common Hindi phrases
Koi bhi admi bole, JARVIS samajh jayega!
"""

import re
from typing import Dict, List, Tuple, Optional

class IndianLanguageProcessor:
    """
    Process and understand Indian language patterns
    Supports: Hinglish, Indian English, Hindi commands
    """
    
    def __init__(self):
        # Common Indian English patterns
        self.indian_patterns = {
            # Greetings
            'namaste': 'hello',
            'namaskar': 'hello',
            'ram ram': 'hello',
            'jai hind': 'hello',
            'sat sri akal': 'hello',
            
            # Polite words
            'ji': '',  # Remove honorific
            'bhai': '',
            'yaar': '',
            'boss': '',
            'dost': 'friend',
            
            # Common verbs
            'karo': 'do',
            'kar do': 'do',
            'kar dena': 'do',
            'karna hai': 'do',
            'karna': 'do',
            'kijiye': 'do',
            'kijiyega': 'do',
            
            'kholo': 'open',
            'khol do': 'open',
            'khol dena': 'open',
            'kholna hai': 'open',
            
            'band karo': 'close',
            'band kar do': 'close',
            'band karna': 'close',
            
            'chalu karo': 'start',
            'chalu kar do': 'start',
            'shuru karo': 'start',
            'shuru kar do': 'start',
            
            'bajao': 'play',
            'baja do': 'play',
            'chalao': 'play',
            'chala do': 'play',
            
            'roko': 'stop',
            'rok do': 'stop',
            'band karo': 'stop',
            
            'dhundo': 'search',
            'dhundho': 'search',
            'khojo': 'search',
            'dekho': 'search',
            'dekh lo': 'search',
            
            'batao': 'tell',
            'bata do': 'tell',
            'batana': 'tell',
            
            'dikhao': 'show',
            'dikha do': 'show',
            
            'bhejo': 'send',
            'bhej do': 'send',
            
            'likho': 'write',
            'likh do': 'write',
            
            'padho': 'read',
            'padh do': 'read',
            
            # Common nouns
            'gaana': 'song',
            'gana': 'song',
            'sangeet': 'music',
            'music': 'music',
            
            'video': 'video',
            'film': 'movie',
            'picture': 'movie',
            
            'photo': 'photo',
            'tasveer': 'photo',
            'pic': 'photo',
            
            'email': 'email',
            'mail': 'email',
            
            'message': 'message',
            'msg': 'message',
            'sandesh': 'message',
            
            # Apps and websites
            'youtube': 'youtube',
            'youtub': 'youtube',
            'utube': 'youtube',
            
            'google': 'google',
            'gugal': 'google',
            
            'chrome': 'chrome',
            'browser': 'browser',
            
            'whatsapp': 'whatsapp',
            'watsapp': 'whatsapp',
            
            # Time related
            'abhi': 'now',
            'turant': 'now',
            'jaldi': 'quickly',
            'jaldi se': 'quickly',
            
            'baad me': 'later',
            'bad mein': 'later',
            
            # Questions
            'kya': 'what',
            'kya hai': 'what is',
            'kaun': 'who',
            'kaun hai': 'who is',
            'kab': 'when',
            'kahan': 'where',
            'kaise': 'how',
            'kyun': 'why',
            'kyu': 'why',
            'kitna': 'how much',
            'kitne': 'how many',
            
            # Common phrases
            'mujhe chahiye': 'i want',
            'mujhe chaiye': 'i want',
            'chahiye': 'want',
            'chaiye': 'want',
            
            'ho gaya': 'done',
            'ho gya': 'done',
            'ban gaya': 'done',
            
            'theek hai': 'okay',
            'thik hai': 'okay',
            'accha': 'okay',
            'acha': 'okay',
            'haan': 'yes',
            'ha': 'yes',
            'nahi': 'no',
            'nai': 'no',
            
            # Directions
            'upar': 'up',
            'neeche': 'down',
            'aage': 'forward',
            'peeche': 'back',
            'bahar': 'out',
            'andar': 'in',
        }
        
        # Common Indian English sentence patterns
        self.sentence_patterns = [
            # "X karo" -> "do X"
            (r'(.+?)\s+kar[o|na|do|dena|diya]', r'do \1'),
            
            # "mujhe X chahiye" -> "i want X"
            (r'mujhe\s+(.+?)\s+cha[hiye|iye]', r'i want \1'),
            
            # "X dikha do" -> "show X"
            (r'(.+?)\s+dikha[o|do]', r'show \1'),
            
            # "X bata do" -> "tell X"
            (r'(.+?)\s+bata[o|do|na]', r'tell \1'),
            
            # "X khol do" -> "open X"
            (r'(.+?)\s+khol[o|do|na]', r'open \1'),
            
            # "X band kar do" -> "close X"
            (r'(.+?)\s+band\s+kar[o|do]', r'close \1'),
            
            # "X chala do" -> "play X"
            (r'(.+?)\s+chala[o|do]', r'play \1'),
            
            # "X dhundho" -> "search X"
            (r'(.+?)\s+dhund[ho|o]', r'search \1'),
        ]
        
        # Common app name variations
        self.app_variations = {
            'youtub': 'youtube',
            'utube': 'youtube',
            'u tube': 'youtube',
            'you tube': 'youtube',
            
            'gugal': 'google',
            'googal': 'google',
            
            'watsapp': 'whatsapp',
            'watsap': 'whatsapp',
            'whatsap': 'whatsapp',
            
            'krom': 'chrome',
            'crome': 'chrome',
            
            'notepad': 'notepad',
            'not pad': 'notepad',
            
            'calculator': 'calculator',
            'calc': 'calculator',
            'kalkulator': 'calculator',
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize Indian language text to standard English
        Handles Hinglish, Indian English, and common variations
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Apply sentence patterns first (more context-aware)
        for pattern, replacement in self.sentence_patterns:
            text = re.sub(pattern, replacement, text)
        
        # Replace individual words
        words = text.split()
        normalized_words = []
        
        for word in words:
            # Check if word is in patterns dictionary
            if word in self.indian_patterns:
                replacement = self.indian_patterns[word]
                if replacement:  # Only add if not empty string
                    normalized_words.append(replacement)
            # Check app variations
            elif word in self.app_variations:
                normalized_words.append(self.app_variations[word])
            else:
                normalized_words.append(word)
        
        # Join and clean up
        normalized = ' '.join(normalized_words)
        
        # Remove duplicate words
        normalized = self._remove_duplicates(normalized)
        
        # Clean up extra spaces again
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def _remove_duplicates(self, text: str) -> str:
        """Remove duplicate consecutive words"""
        words = text.split()
        result = []
        prev = None
        
        for word in words:
            if word != prev:
                result.append(word)
            prev = word
        
        return ' '.join(result)
    
    def extract_intent(self, text: str) -> Tuple[str, str]:
        """
        Extract intent (action) and entity (object) from text
        Returns: (action, entity)
        
        Examples:
        "youtube kholo" -> ("open", "youtube")
        "gaana bajao" -> ("play", "song")
        "google pe dhundho" -> ("search", "google")
        """
        normalized = self.normalize_text(text)
        
        # Common action words
        actions = {
            'open': ['open', 'launch', 'start', 'run'],
            'close': ['close', 'exit', 'quit', 'stop'],
            'play': ['play', 'start'],
            'search': ['search', 'find', 'look', 'google'],
            'show': ['show', 'display'],
            'tell': ['tell', 'say'],
            'send': ['send'],
            'write': ['write'],
            'read': ['read'],
        }
        
        # Find action
        action = None
        for key, variations in actions.items():
            for variation in variations:
                if variation in normalized:
                    action = key
                    break
            if action:
                break
        
        # Extract entity (remove action words)
        entity = normalized
        if action:
            for variations in actions.values():
                for variation in variations:
                    entity = entity.replace(variation, '').strip()
        
        return (action or 'unknown', entity or normalized)
    
    def is_question(self, text: str) -> bool:
        """Check if text is a question"""
        question_words = ['kya', 'kaun', 'kab', 'kahan', 'kaise', 'kyun', 'kyu', 
                         'what', 'who', 'when', 'where', 'how', 'why', 'which']
        
        text_lower = text.lower()
        return any(word in text_lower for word in question_words) or text.endswith('?')
    
    def get_examples(self) -> List[str]:
        """Get example commands in Indian language"""
        return [
            # Basic commands
            "YouTube kholo",
            "Google Chrome chalu karo",
            "Notepad band karo",
            
            # Music/Video
            "Gaana bajao",
            "Video dikha do",
            "Music chala do",
            
            # Search
            "Google pe dhundho",
            "YouTube pe search karo",
            
            # Questions
            "Aaj ka mausam kaisa hai?",
            "Time kya hua hai?",
            "Ye kya hai?",
            
            # Hinglish mix
            "Mujhe ek email bhejni hai",
            "Calculator khol do yaar",
            "Jaldi se YouTube chala do",
            
            # Natural speech
            "Bhai, thoda volume badha do",
            "Boss, screenshot le lo",
            "Yaar, ye file band kar do",
        ]


# Global instance
indian_language = IndianLanguageProcessor()


def normalize_indian_text(text: str) -> str:
    """
    Convenience function to normalize Indian language text
    Usage: normalized = normalize_indian_text("youtube kholo")
    """
    return indian_language.normalize_text(text)


def extract_intent_from_indian_text(text: str) -> Tuple[str, str]:
    """
    Convenience function to extract intent from Indian language text
    Usage: action, entity = extract_intent_from_indian_text("gaana bajao")
    """
    return indian_language.extract_intent(text)


def is_indian_question(text: str) -> bool:
    """
    Check if text is a question in Indian language
    Usage: if is_indian_question("time kya hua?"): ...
    """
    return indian_language.is_question(text)


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("Indian Language Processor - Test Examples")
    print("="*60)
    
    test_phrases = [
        "youtube kholo",
        "gaana bajao",
        "google pe dhundho",
        "mujhe email bhejni hai",
        "calculator chalu karo",
        "time kya hua hai?",
        "volume badha do yaar",
        "chrome band kar do",
        "notepad dikha do",
        "jaldi se screenshot le lo",
    ]
    
    for phrase in test_phrases:
        normalized = normalize_indian_text(phrase)
        action, entity = extract_intent_from_indian_text(phrase)
        is_q = is_indian_question(phrase)
        
        print(f"\nOriginal: {phrase}")
        print(f"Normalized: {normalized}")
        print(f"Intent: Action='{action}', Entity='{entity}'")
        print(f"Is Question: {is_q}")
    
    print("\n" + "="*60)
    print("Example Commands:")
    print("="*60)
    for example in indian_language.get_examples():
        print(f"  • {example}")

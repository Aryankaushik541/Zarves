# 🎵 YouTube Auto-Music Feature

## Overview
Ab JARVIS automatically trending music play kar sakta hai jab aap YouTube kholne ko bolo!

## ✨ New Feature
Jab aap "YouTube kholo" ya "YouTube kholo aur music play karo" bolte ho, JARVIS automatically:
1. 🔍 Latest trending Hindi songs fetch karta hai
2. 🎲 Random trending song select karta hai
3. ▶️ YouTube pe automatically play karta hai

## 🎯 Usage Examples

### Example 1: Open YouTube with Auto-Music
```
YOU: Jarvis, YouTube kholo

JARVIS: 
🎵 No specific song requested, playing trending music...
🔍 Fetching trending songs...
🎵 Found trending: Tauba Tauba Bad Newz
🎵 Selected: Tauba Tauba Bad Newz
🎵 YouTube पर खोज रहा हूँ: Tauba Tauba Bad Newz
✅ YouTube opened and playing!
```

### Example 2: YouTube with Music Request
```
YOU: Jarvis, YouTube kholo aur music play karo

JARVIS:
🎵 Auto-selecting trending song...
🎵 Playing: Satranga Animal
✅ Done!
```

### Example 3: YouTube with Specific Song
```
YOU: Jarvis, YouTube pe Kesariya bajao

JARVIS:
🎵 Playing: Kesariya
✅ Playing on YouTube!
```

### Example 4: Just Music
```
YOU: Jarvis, gaana bajao

JARVIS:
🎵 Auto-selected: Maan Meri Jaan King
✅ Playing!
```

## 🎼 Trending Songs Pool
JARVIS automatically fetches from:
- Latest 2024 trending Hindi songs
- Popular Bollywood hits
- Viral music videos

**Fallback Songs** (if internet fails):
- Tauba Tauba (Bad Newz)
- Satranga (Animal)
- Arjan Vailly (Animal)
- Maan Meri Jaan (King)
- Kesariya (Brahmastra)
- Chaleya (Jawan)
- Apna Bana Le (Bhediya)
- O Maahi (Dunki)
- Pehle Bhi Main (Vishal Mishra)
- Heeriye (Jasleen Royal)
- And many more...

## 🔧 How It Works

### Smart Detection
JARVIS detects these commands as "auto-music":
- "YouTube kholo"
- "YouTube kholo aur music play karo"
- "YouTube kholo aur gaana bajao"
- "play music"
- "gaana bajao"
- "song sunao"

### Trending Fetch Process
1. **Live Fetch**: Tries to get latest trending from YouTube
2. **Parse Results**: Filters out playlists, mixes, channels
3. **Random Selection**: Picks a random trending song
4. **Fallback**: Uses popular songs list if fetch fails

### Auto-Play Logic
```python
# Empty query or music keywords → Auto-select trending
if query == "" or query in ["music", "song", "gaana"]:
    query = get_trending_song()
    
# Play on YouTube
play_youtube(query)
```

## 📋 Commands Reference

| Command | Action |
|---------|--------|
| `YouTube kholo` | Opens YouTube + plays trending song |
| `YouTube kholo aur music play karo` | Same as above |
| `YouTube kholo aur gaana bajao` | Same as above |
| `play music` | Plays trending song |
| `gaana bajao` | Plays trending song |
| `play [song name]` | Plays specific song |
| `[song name] bajao` | Plays specific song |

## 🎨 Customization

### Change Language Preference
Edit `web_ops.py`:
```python
# Change from Hindi to English
search_query = "trending english songs 2024"

# Or Punjabi
search_query = "trending punjabi songs 2024"
```

### Add More Fallback Songs
Edit `web_ops.py`:
```python
trending_songs = [
    "Your Song 1",
    "Your Song 2",
    "Your Song 3",
    # Add more...
]
```

### Adjust Trending Fetch
```python
# Fetch more songs for variety
titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)[:20]  # Get 20 instead of 10
```

## 🛠️ Troubleshooting

### Issue: "Same song plays every time"
**Solution**: 
- Check internet connection (for live trending fetch)
- Restart JARVIS to refresh trending cache
- Clear browser cache

### Issue: "No music plays"
**Solution**:
```bash
# Install pywhatkit
pip install pywhatkit

# Or use browser fallback (automatic)
```

### Issue: "Wrong language songs"
**Solution**: Edit trending search query in `web_ops.py`

## 🚀 Advanced Features

### Multi-Language Support
```python
# In web_ops.py, modify _get_trending_song()
def _get_trending_song(self, language="hindi"):
    search_query = f"trending {language} songs 2024"
    # Rest of the code...
```

### Mood-Based Selection
```python
# Add mood parameter
def _get_trending_song(self, mood="happy"):
    search_query = f"trending {mood} hindi songs 2024"
    # Rest of the code...
```

### Time-Based Selection
```python
import datetime

hour = datetime.datetime.now().hour
if 6 <= hour < 12:
    search_query = "morning songs hindi"
elif 12 <= hour < 17:
    search_query = "afternoon party songs"
else:
    search_query = "evening romantic songs"
```

## 💡 Pro Tips

1. **Better Variety**: Restart JARVIS daily for fresh trending songs
2. **Specific Requests**: Say exact song name for precise results
3. **Playlist Mode**: Say "play romantic songs playlist" for continuous music
4. **Quality**: Use good internet for better trending fetch

## 🎯 Future Enhancements
- [ ] User preference learning (remember favorite genres)
- [ ] Mood detection from voice tone
- [ ] Time-based auto-selection
- [ ] Multi-language support
- [ ] Spotify integration
- [ ] Offline music library

## 📝 Notes
- Trending songs update automatically from YouTube
- Requires internet for live trending fetch
- Falls back to popular songs if offline
- Works on all platforms (Windows, macOS, Linux)

---
**Made with ❤️ by JARVIS AI**

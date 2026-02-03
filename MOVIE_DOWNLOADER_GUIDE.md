# 🎬 JARVIS Movie Downloader & Player Guide

## Overview
JARVIS ab movies download kar sakta hai aur automatically VLC player mein play kar sakta hai!

## ✨ Features
- 🔍 **Automatic Movie Search** - Website pe movie search karta hai
- ⬇️ **Smart Download** - Movie automatically download karta hai
- 🎥 **Auto-Play in VLC** - Download hone ke baad VLC mein khud se play karta hai
- 📊 **Progress Tracking** - Download progress dikhata hai
- 🎯 **Quality Selection** - 480p, 720p, 1080p choose kar sakte ho

## 📋 Requirements

### 1. Install Required Python Packages
```bash
pip install selenium beautifulsoup4 requests webdriver-manager
```

### 2. Install ChromeDriver
```bash
pip install webdriver-manager
```

### 3. Install VLC Player
- **Windows**: https://www.videolan.org/vlc/download-windows.html
- **macOS**: https://www.videolan.org/vlc/download-macosx.html
- **Linux**: `sudo apt install vlc`

## 🎯 Usage Examples

### Example 1: Basic Movie Download
```
YOU: Jarvis, Inception movie download karo vegamovies se

JARVIS: 
🎬 Movie Downloader & Player
============================================================
Movie: Inception
Website: https://vegamovies.attorney/
Quality: 720p
============================================================

🔍 Searching for 'Inception' on https://vegamovies.attorney/...
✅ Found: Inception (2010) 720p BluRay
🔗 URL: https://vegamovies.attorney/inception-2010/
✅ Download link found!
⬇️  Downloading movie...
📍 Save location: ~/Downloads/JARVIS_Movies/Inception_720p.mp4
⬇️  Progress: 100.0%
✅ Download complete!
🎥 Opening in VLC player...

Movie 'Inception' downloaded and playing in VLC!
```

### Example 2: Specify Quality
```
YOU: Jarvis, Avatar movie 1080p quality mein download karo

JARVIS: [Downloads Avatar in 1080p quality]
```

### Example 3: Different Website
```
YOU: Jarvis, https://example-movies.com se Interstellar download karo

JARVIS: [Downloads from specified website]
```

### Example 4: Play Already Downloaded Movie
```
YOU: Jarvis, ~/Downloads/JARVIS_Movies/Inception_720p.mp4 play karo

JARVIS: 🎥 Playing: Inception_720p.mp4
```

## 🗂️ Download Location
All movies are saved to:
```
~/Downloads/JARVIS_Movies/
```

## ⚙️ How It Works

1. **Search Phase**
   - JARVIS website pe movie search karta hai
   - Selenium WebDriver use karta hai (anti-detection ke saath)
   - Movie page ka URL find karta hai

2. **Link Extraction**
   - Movie page se download link extract karta hai
   - Quality preference ke according link select karta hai
   - Google Drive, direct links, etc. support karta hai

3. **Download Phase**
   - Movie file download karta hai with progress tracking
   - `~/Downloads/JARVIS_Movies/` folder mein save karta hai
   - File size aur progress display karta hai

4. **Auto-Play**
   - VLC player automatically launch karta hai
   - Downloaded movie play karta hai

## 🛠️ Troubleshooting

### Issue: "VLC player not found"
**Solution**: VLC install karo:
- Windows: https://www.videolan.org/vlc/
- macOS: `brew install --cask vlc`
- Linux: `sudo apt install vlc`

### Issue: "ChromeDriver not found"
**Solution**: 
```bash
pip install webdriver-manager
```

### Issue: "Movie not found on website"
**Solution**: 
- Movie name correctly spell karo
- Different website try karo
- Manual search karke exact movie name use karo

### Issue: "Download link not found"
**Solution**:
- Website structure change ho sakta hai
- Manual download karo movie page se
- Different quality try karo

## 🔒 Legal Disclaimer
**IMPORTANT**: 
- Sirf legal aur authorized content download karo
- Copyright laws follow karo
- Piracy illegal hai
- Yeh tool educational purposes ke liye hai

## 🎨 Supported Websites
- vegamovies.attorney
- Any website with similar structure
- Custom websites (may need code adjustments)

## 📝 Advanced Usage

### Custom Website Support
Agar aapko different website se download karna hai:

```python
# In skill/movie_downloader.py
# Modify _search_movie_on_website() and _extract_download_link()
# according to target website structure
```

### Quality Options
- `480p` - Low quality, small file size
- `720p` - HD quality (default)
- `1080p` - Full HD quality, large file size

## 🚀 Future Enhancements
- [ ] Multiple download sources
- [ ] Subtitle download
- [ ] Batch download
- [ ] Resume interrupted downloads
- [ ] Torrent support
- [ ] Streaming option

## 💡 Tips
1. **Fast Downloads**: Use good internet connection
2. **Storage**: Ensure enough disk space
3. **VLC Shortcuts**: Learn VLC keyboard shortcuts for better experience
4. **Quality vs Size**: 720p is best balance between quality and file size

## 🤝 Contributing
Agar improvements suggest karna hai ya bugs report karna hai, GitHub issues use karo!

---
**Made with ❤️ by JARVIS AI**

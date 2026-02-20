# 🚀 ZARVES - Quick Start Guide (Hindi)

## 📥 Step 1: Download Karo

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves
```

---

## 📦 Step 2: Install Karo

```bash
pip install -r requirements.txt
```

**Agar error aaye to:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 🎤 Step 3: Run Karo

```bash
python zarves_advanced.py
```

---

## 🗣️ Step 4: Bolo!

Jab Zarves taiyar ho jaye, tab yeh commands bol sakte ho:

### 🌐 Websites Kholne Ke Liye
```
"Zarves open Google"
"Open YouTube"
"Open Facebook"
"Open Instagram"
"Open Gmail"
```

### 🔍 Search Karne Ke Liye
```
"Search for Python tutorials"
"YouTube search funny videos"
"Find best restaurants"
```

### ⏰ Information Ke Liye
```
"What's the time?"
"What's the date?"
"How are you?"
```

### 💻 System Control
```
"Close browser"
"Exit" (Zarves band karne ke liye)
```

---

## ⚙️ Settings (Optional)

### Voice Speed Adjust Karna
File kholo: `zarves_advanced.py`

Line 120 pe:
```python
self.engine.setProperty('rate', 180)  # 150 = slow, 200 = fast
```

### Volume Adjust Karna
Line 121 pe:
```python
self.engine.setProperty('volume', 0.9)  # 0.5 = low, 1.0 = max
```

---

## 🐛 Common Problems

### Problem 1: Microphone kaam nahi kar raha
**Solution:**
- Windows: Settings → Privacy → Microphone → Allow
- Check microphone connection
- Dusra microphone try karo

### Problem 2: Browser nahi khul raha
**Solution:**
```bash
pip install selenium webdriver-manager
```

Chrome install karo: https://www.google.com/chrome/

### Problem 3: Voice samajh nahi aa rahi
**Solution:**
- Thoda loud bolo
- Background noise kam karo
- Microphone ke paas bolo
- Hindi ya English clearly bolo

### Problem 4: "Module not found" error
**Solution:**
```bash
pip install pyttsx3 SpeechRecognition pyaudio
```

**Windows pe pyaudio error:**
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 📝 Example Session

```
🚀 Initializing Zarves AI Agent...
✅ Zarves is ready!
🗣️ Zarves: Zarves taiyar hai! Aap mujhe kuch bhi bol sakte hain.

🎤 Listening...
👤 You (Hindi): Zarves open Google
🗣️ Zarves: Browser khol raha hoon
[Chrome opens with google.com]

🎤 Listening...
👤 You (English): Search for Python tutorials
🗣️ Zarves: Python tutorials search kar raha hoon
[Google search results appear]

🎤 Listening...
👤 You: What's the time?
🗣️ Zarves: Abhi time hai 03:45 PM

🎤 Listening...
👤 You: Exit
🗣️ Zarves: Zarves band ho raha hai. Alvida!
👋 Zarves stopped.
```

---

## 🎯 Pro Tips

1. **Clear bolo** - Zarves better samjhega
2. **"Zarves" bolke start karo** - Better recognition
3. **Ek command ek baar** - Multiple commands ek saath mat bolo
4. **Wait karo** - Command execute hone do
5. **Practice karo** - Zarves seekhta rahega

---

## 🔥 Advanced Usage

### Custom Commands Add Karna

File kholo: `zarves_advanced.py`

Line 50 pe apna command add karo:
```python
"open netflix": {"action": "open_browser", "url": "https://www.netflix.com"},
"open amazon": {"action": "open_browser", "url": "https://www.amazon.in"},
```

### Naye Skills Add Karna

`skill/` folder me naya file banao:
```python
# skill/my_custom_skill.py

class MyCustomSkill:
    def do_something(self):
        print("Custom skill working!")
```

---

## 📚 Next Steps

1. ✅ Basic commands try karo
2. ✅ README.md padho (detailed info)
3. ✅ Code explore karo
4. ✅ Apne commands add karo
5. ✅ Share karo aur star do! ⭐

---

## 🆘 Help Chahiye?

- **GitHub Issues**: https://github.com/Aryankaushik541/Zarves/issues
- **Code dekho**: `zarves_advanced.py` file kholo
- **Examples dekho**: README.md me bahut examples hain

---

## 🎉 Enjoy Zarves!

**Yaad rakho:**
- Zarves **offline** kaam karta hai
- **Koi API key** nahi chahiye
- **Free** hai aur **open source** hai
- Aap **modify** kar sakte ho

**Happy Coding! 🚀**

# 🏧 Zarves - Aadhar ATM Auto Withdrawal (Voice + AI Screen Detect)

Zarves अब **Aadhar ATM automation** के लिए focused है। `main.py` चलाते ही GUI खुलता है और:

- ✅ **Aadhar number manual typing नहीं** — user बोलेगा, app सुनकर लेगा  
- ✅ **Amount भी voice से** पूछेगा: *"kitna paisa chahiye?"*  
- ✅ **AI screen detect** (OCR + Ollama optional) करके Aadhar/Amount fields भर देगा  
- ✅ Submit → Fingerprint prompt detect → balance पढ़ेगा → **Print receipt** करेगा

---

## 🚀 Quick Start

```bash
git clone https://github.com/Aryankaushik541/Zarves.git
cd Zarves

# Install dependencies
pip install -r requirements.txt

# Run GUI (voice-first)
python main.py
```

---

## ✅ जरूरी Dependencies

**Python packages:**
- `pyautogui`
- `pytesseract`
- `opencv-python`
- `Pillow`
- `SpeechRecognition`
- `pyaudio`
- `ollama` (optional, for better AI label detection)

```bash
pip install pyautogui pytesseract opencv-python Pillow SpeechRecognition pyaudio ollama
```

**Tesseract OCR install (required):**
- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki  
- **Linux:** `sudo apt-get install tesseract-ocr`  
- **Mac:** `brew install tesseract`

---

## 🤖 Ollama (Optional AI Detection)

Ollama local AI से screen labels बेहतर detect होंगे।

```bash
ollama serve
ollama pull llama3.2
```

अगर Ollama नहीं है, तो system OCR heuristic se काम करेगा।

---

## 🧭 How It Works (Flow)

1. GUI खुलते ही app बोलेगा: **"Aadhar number bolo"**
2. User बोलेगा → system Aadhar capture करेगा  
3. App पूछेगा: **"Kitna paisa chahiye?"**
4. Amount capture होते ही automation शुरू  
5. Screen detect करके Aadhar field भरता है  
6. Amount field भरता है  
7. Submit click  
8. Fingerprint screen detect → user ko बोलता है  
9. Balance पढ़ता है  
10. Print button click करके receipt generate करता है  

---

## 🧩 Project Structure

```
Zarves/
├── main.py                 # Main entry (voice GUI)
├── launch_aadhar_atm.py     # GUI + voice logic
├── skill/
│   └── aadhar_atm_skill.py  # OCR + AI automation
└── core/
    └── voice.py             # Voice prompts
```

---

## ⚠️ Notes

- Automation के दौरान mouse corner में ले जाएं तो PyAutoGUI failsafe stop कर देता है।
- OCR quality screen clarity पर depend करती है।
- कुछ ATM screens पर labels अलग हो सकते हैं — Ollama मदद करता है।

---

## ✅ Run

```bash
python main.py
```

बस इतना ही!

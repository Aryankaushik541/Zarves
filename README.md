# 🏧 Aadhar ATM Auto Withdrawal (GUI + Voice)

Yeh project Aadhar ATM screen ko OCR se read karke **auto-fill**, **amount entry**, **submit**, **print**, aur **receipt generate** karne ke liye bana hai. `main.py` run karte hi GUI open hoti hai aur voice input bhi available hai.

---

## ✅ Run (Single Command)

```bash
python main.py
```

---

## 📦 Dependencies

```bash
pip install -r requirements.txt
```

**OCR ke liye Tesseract install karna zaroori hai:**

- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki  
- **Linux:** `sudo apt-get install tesseract-ocr`  
- **Mac:** `brew install tesseract`

---

## 🎤 Voice Flow (Aadhar + Amount)

GUI me **“🎤 Aadhar + Amount बोलकर भरो”** button hai:

1. System **Aadhar number** sunega (12 digits).
2. Phir **kitna paisa chahiye** poochega aur amount sunega.
3. Fields auto-fill ho jayengi.

---

## 🧠 Auto Screen Detection

Automation step-by-step:

1. **Aadhar field detect** karke number fill
2. **Amount field detect** karke amount fill
3. **Submit** button click
4. **Fingerprint/Morpho** prompt ka wait
5. Screen se **balance** aur **withdrawal amount** read
6. **Print** button click karke receipt generate

---

## 📝 Notes

- Screen par text clearly visible hona chahiye (OCR accuracy ke liye).
- Fingerprint scan ke baad balance auto-read hota hai.
- Agar OCR miss kare to agent fallback position use karta hai.

---

## 📂 Key Files

- `main.py` → single entry point
- `launch_aadhar_atm.py` → GUI + voice input
- `skill/aadhar_atm_skill.py` → OCR + automation logic

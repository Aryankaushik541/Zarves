# 🔄 Migration Guide: Groq → Ollama

## Why Migrate?

### **Before (Groq)**
❌ API key required  
❌ Rate limits (14,400 tokens/min)  
❌ Cloud dependency  
❌ Data sent to external servers  
❌ Internet required  

### **After (Ollama)**
✅ No API key needed  
✅ No rate limits  
✅ Runs locally  
✅ 100% private  
✅ Works offline (after model download)  

---

## Quick Migration (5 Minutes)

### **Step 1: Install Ollama**

```bash
# Windows
https://ollama.com/download/windows

# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### **Step 2: Start Ollama & Pull Model**

```bash
# Terminal 1: Start server
ollama serve

# Terminal 2: Pull model (one-time, ~2GB)
ollama pull llama3.2
```

### **Step 3: Update JARVIS**

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
```

### **Step 4: Remove Old Config (Optional)**

```bash
# Remove GROQ_API_KEY from .env file
# Or just delete .env and use defaults
```

### **Step 5: Run JARVIS**

```bash
python main.py
```

**Expected Output:**
```
✅ Connected to Ollama at http://localhost:11434
📦 Available models: 1
✅ Using model: llama3.2
🎤 JARVIS is listening...
```

---

## What Changed?

### **Code Changes**

| File | Change |
|------|--------|
| `core/engine.py` | Replaced `from groq import Groq` with `from ollama import Client` |
| `requirements.txt` | Replaced `groq` with `ollama` |
| `.env.template` | Replaced `GROQ_API_KEY` with `OLLAMA_HOST` and `OLLAMA_MODEL` |

### **Configuration Changes**

**Old (.env):**
```bash
GROQ_API_KEY=your_groq_api_key_here
```

**New (.env) - Optional:**
```bash
# These are defaults, no need to set unless customizing
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## Troubleshooting

### **Issue: "Connection refused"**

```bash
❌ Error: Connection refused to http://localhost:11434

✅ Solution:
# Make sure Ollama is running
ollama serve
```

### **Issue: "Model not found"**

```bash
❌ Error: Model llama3.2 not found

✅ Solution:
# Pull the model
ollama pull llama3.2

# Verify
ollama list
```

### **Issue: "Import error: ollama"**

```bash
❌ ModuleNotFoundError: No module named 'ollama'

✅ Solution:
pip install ollama
```

---

## Performance Comparison

### **Response Time**

| Hardware | Groq (Cloud) | Ollama (Local) |
|----------|--------------|----------------|
| i5, 16GB RAM | ~1-2 sec | ~2-3 sec |
| i7, 32GB RAM, RTX 3060 | ~1-2 sec | ~1-2 sec |

### **Cost**

| Feature | Groq | Ollama |
|---------|------|--------|
| Monthly Cost | $0 (free tier) | $0 |
| Rate Limits | 14,400 tokens/min | Unlimited |
| API Key | Required | Not needed |

---

## Advanced Configuration

### **Use Different Model**

```bash
# Pull different model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral
```

### **Remote Ollama Server**

```bash
# Run Ollama on powerful server
# Server: ollama serve

# Client .env:
OLLAMA_HOST=http://192.168.1.100:11434
```

### **Multiple Models**

```bash
# Pull multiple models
ollama pull llama3.2
ollama pull mistral
ollama pull codellama

# Switch by updating .env
OLLAMA_MODEL=codellama  # For coding tasks
```

---

## Rollback (If Needed)

If you want to go back to Groq:

```bash
# 1. Checkout previous version
git checkout <commit-before-ollama>

# 2. Reinstall dependencies
pip install -r requirements.txt

# 3. Add GROQ_API_KEY to .env
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run JARVIS
python main.py
```

---

## Benefits Summary

✅ **No API Key** - One less thing to manage  
✅ **No Rate Limits** - Use as much as you want  
✅ **Privacy** - Data never leaves your computer  
✅ **Offline** - Works without internet  
✅ **Free Forever** - No subscription, no costs  
✅ **Multiple Models** - Easy to switch  
✅ **Self-Hosted** - Full control  

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull model
3. ✅ Update JARVIS
4. ✅ Test commands
5. 📖 Read [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for advanced features

---

**Questions?** Open an issue on GitHub!

**Enjoy your FREE, unlimited AI assistant!** 🚀

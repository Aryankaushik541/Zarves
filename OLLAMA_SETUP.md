# 🚀 Ollama Setup Guide - Local LLM for JARVIS

JARVIS ab **Ollama** use karta hai - ek **completely free, local LLM server** jo aapke apne computer par chalta hai!

## 🎯 Why Ollama?

✅ **Completely FREE** - No API keys, no rate limits, no costs  
✅ **100% Private** - Data aapke computer par hi rahta hai  
✅ **Unlimited Usage** - Jitna chahe use karo, koi limit nahi  
✅ **Fast** - Local execution means faster responses  
✅ **Offline** - Internet ke bina bhi kaam karta hai  
✅ **Multiple Models** - Llama, Mistral, CodeLlama, aur bahut kuch  

---

## 📦 Installation

### **Windows**

```bash
# Download and install from official website
https://ollama.com/download/windows

# Or use winget
winget install Ollama.Ollama
```

### **Mac**

```bash
# Download from official website
https://ollama.com/download/mac

# Or use Homebrew
brew install ollama
```

### **Linux**

```bash
# One-line install
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 🚀 Quick Start

### **1. Start Ollama Server**

```bash
# Terminal/Command Prompt mein run karo
ollama serve
```

**Output:**
```
Ollama server running on http://localhost:11434
```

> **Note:** Yeh terminal window open rakhna hai jab tak JARVIS use kar rahe ho!

### **2. Pull a Model**

```bash
# Recommended: Llama 3.2 (Fast & Efficient)
ollama pull llama3.2

# Or other models:
ollama pull llama3.1      # Larger, more powerful
ollama pull mistral       # Alternative model
ollama pull codellama     # For coding tasks
```

**Model Download Sizes:**
- `llama3.2` - ~2GB (Recommended)
- `llama3.1` - ~4.7GB (More powerful)
- `mistral` - ~4.1GB (Alternative)
- `codellama` - ~3.8GB (Code-focused)

### **3. Verify Installation**

```bash
# List installed models
ollama list

# Test a model
ollama run llama3.2
>>> Hello!
```

---

## ⚙️ JARVIS Configuration

### **1. Update Dependencies**

```bash
# Install Ollama Python library
pip install ollama

# Or update all dependencies
pip install -r requirements.txt
```

### **2. Configure Environment (Optional)**

Create/update `.env` file:

```bash
# Default configuration (works out of the box)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Custom configuration (if needed)
# OLLAMA_HOST=http://192.168.1.100:11434  # Remote Ollama server
# OLLAMA_MODEL=mistral                     # Different model
```

> **Note:** Agar `.env` file nahi banate, toh default settings use hongi!

### **3. Run JARVIS**

```bash
python main.py
```

**Expected Output:**
```
✅ Connected to Ollama at http://localhost:11434
📦 Available models: 3
✅ Using model: llama3.2
🎤 JARVIS is listening...
```

---

## 🎯 Available Models

### **Recommended Models**

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `llama3.2` | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | **Best for JARVIS** - Fast & efficient |
| `llama3.1` | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | More powerful, slower |
| `mistral` | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐ | Alternative, good quality |
| `codellama` | 3.8GB | ⚡⚡ | ⭐⭐⭐⭐ | Best for coding tasks |

### **Pull Multiple Models**

```bash
# Pull all recommended models
ollama pull llama3.2
ollama pull llama3.1
ollama pull mistral
ollama pull codellama
```

### **Switch Models**

Update `.env` file:
```bash
OLLAMA_MODEL=mistral  # Change to any installed model
```

---

## 🔧 Advanced Configuration

### **Custom Ollama Host**

Agar Ollama kisi aur machine par chal raha hai:

```bash
# .env file mein
OLLAMA_HOST=http://192.168.1.100:11434
```

### **GPU Acceleration**

Ollama automatically GPU use karta hai agar available ho:

```bash
# Check GPU usage
nvidia-smi  # For NVIDIA GPUs

# Ollama will show:
✅ CUDA available: 12.1
✅ GPU: NVIDIA GeForce RTX 3060
```

### **Model Parameters**

Custom model parameters (advanced):

```python
# In core/engine.py, modify _call_llm_with_retry:
response = self.client.chat(
    model=self.model,
    messages=self.conversation_history,
    options={
        'temperature': 0.7,      # Creativity (0-1)
        'top_p': 0.9,           # Diversity
        'num_predict': 2048,    # Max tokens
    }
)
```

---

## 🐛 Troubleshooting

### **Issue: "Connection refused"**

```bash
❌ Error: Connection refused to http://localhost:11434

Solution:
1. Start Ollama server: ollama serve
2. Check if running: curl http://localhost:11434
3. Restart JARVIS
```

### **Issue: "Model not found"**

```bash
❌ Error: Model llama3.2 not found

Solution:
1. Pull model: ollama pull llama3.2
2. Verify: ollama list
3. Restart JARVIS
```

### **Issue: "Out of memory"**

```bash
❌ Error: Out of memory

Solution:
1. Use smaller model: ollama pull llama3.2
2. Close other applications
3. Update .env: OLLAMA_MODEL=llama3.2
```

### **Issue: Slow responses**

```bash
⚠️  Responses are slow

Solution:
1. Use faster model: llama3.2
2. Enable GPU acceleration (if available)
3. Reduce max_tokens in engine.py
```

---

## 📊 Performance Comparison

### **Groq (Cloud) vs Ollama (Local)**

| Feature | Groq | Ollama |
|---------|------|--------|
| **Cost** | Free tier limited | Completely FREE |
| **Privacy** | Data sent to cloud | 100% local |
| **Speed** | Very fast | Fast (depends on hardware) |
| **Rate Limits** | Yes (14,400 tokens/min) | No limits |
| **Internet** | Required | Optional |
| **Setup** | API key needed | Local installation |

### **Model Performance**

**Hardware:** Intel i5, 16GB RAM, No GPU

| Model | Response Time | Quality |
|-------|---------------|---------|
| `llama3.2` | ~2-3 seconds | ⭐⭐⭐ |
| `llama3.1` | ~5-7 seconds | ⭐⭐⭐⭐ |
| `mistral` | ~4-6 seconds | ⭐⭐⭐⭐ |

**Hardware:** Intel i7, 32GB RAM, RTX 3060

| Model | Response Time | Quality |
|-------|---------------|---------|
| `llama3.2` | ~1-2 seconds | ⭐⭐⭐ |
| `llama3.1` | ~2-3 seconds | ⭐⭐⭐⭐ |
| `mistral` | ~2-3 seconds | ⭐⭐⭐⭐ |

---

## 🎯 Best Practices

### **1. Keep Ollama Running**

```bash
# Start Ollama in background (Linux/Mac)
ollama serve &

# Windows: Run in separate terminal
start ollama serve
```

### **2. Regular Model Updates**

```bash
# Update models periodically
ollama pull llama3.2
```

### **3. Monitor Resource Usage**

```bash
# Check memory usage
ollama ps

# Check running models
ollama list
```

### **4. Clean Up Old Models**

```bash
# Remove unused models
ollama rm old-model-name

# Free up space
ollama prune
```

---

## 🚀 Migration from Groq

### **What Changed?**

✅ **No API Key needed** - Remove `GROQ_API_KEY` from `.env`  
✅ **Local execution** - Start `ollama serve` before running JARVIS  
✅ **Model names** - Use `llama3.2` instead of `llama-3.1-8b-instant`  
✅ **Unlimited usage** - No rate limits!  

### **Migration Steps**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull model
ollama pull llama3.2

# 3. Start server
ollama serve

# 4. Update dependencies
pip install ollama

# 5. Run JARVIS
python main.py
```

---

## 📚 Resources

- **Ollama Website:** https://ollama.com
- **Ollama GitHub:** https://github.com/ollama/ollama
- **Model Library:** https://ollama.com/library
- **Python Library:** https://github.com/ollama/ollama-python
- **Documentation:** https://github.com/ollama/ollama/tree/main/docs

---

## 💡 Tips

1. **Start Ollama automatically on boot:**
   - Windows: Add to Startup folder
   - Linux/Mac: Create systemd service

2. **Use multiple models:**
   - Pull different models for different tasks
   - Switch via `.env` file

3. **Optimize for your hardware:**
   - Low RAM? Use `llama3.2`
   - High RAM + GPU? Use `llama3.1`

4. **Remote access:**
   - Run Ollama on powerful server
   - Access from multiple devices

---

## 🎉 Enjoy Unlimited, Free AI!

Ab JARVIS completely free aur unlimited hai! No API keys, no rate limits, no costs! 🚀

**Questions?** Open an issue on GitHub!

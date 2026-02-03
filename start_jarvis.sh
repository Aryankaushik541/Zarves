#!/bin/bash

# JARVIS Startup Script
# Automatically checks and starts Ollama, then launches JARVIS

echo "🤖 JARVIS Startup Script"
echo "========================"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found!"
    echo ""
    echo "📥 Installing Ollama..."
    echo ""
    
    # Detect OS and install
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Detected macOS"
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Detected Linux"
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "⚠️  Please install Ollama manually:"
        echo "   https://ollama.com/download"
        exit 1
    fi
fi

echo "✅ Ollama found!"
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    
    # Wait for Ollama to start
    echo "⏳ Waiting for Ollama to start..."
    for i in {1..10}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama server started!"
            break
        fi
        sleep 1
    done
else
    echo "✅ Ollama server already running!"
fi

echo ""

# Check if model is available
echo "📦 Checking for llama3.2 model..."
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 Pulling llama3.2 model (this may take a few minutes)..."
    ollama pull llama3.2
    echo "✅ Model downloaded!"
else
    echo "✅ Model already available!"
fi

echo ""
echo "🎯 Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Launching JARVIS..."
echo "========================"
echo ""

# Launch JARVIS
python main.py

# Cleanup on exit
if [ ! -z "$OLLAMA_PID" ]; then
    echo ""
    echo "🛑 Stopping Ollama server..."
    kill $OLLAMA_PID 2>/dev/null
fi

@echo off
REM JARVIS Startup Script for Windows
REM Automatically checks and starts Ollama, then launches JARVIS

echo.
echo ========================================
echo    JARVIS Startup Script (Windows)
echo ========================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama not found!
    echo.
    echo Please install Ollama:
    echo 1. Download from: https://ollama.com/download/windows
    echo 2. Run the installer
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo [OK] Ollama found!
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Starting Ollama server...
    start /B ollama serve
    
    REM Wait for Ollama to start
    echo [INFO] Waiting for Ollama to start...
    timeout /t 5 /nobreak >nul
    echo [OK] Ollama server started!
) else (
    echo [OK] Ollama server already running!
)

echo.

REM Check if model is available
echo [INFO] Checking for llama3.2 model...
ollama list | findstr "llama3.2" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Pulling llama3.2 model (this may take a few minutes)...
    ollama pull llama3.2
    echo [OK] Model downloaded!
) else (
    echo [OK] Model already available!
)

echo.
echo [INFO] Installing Python dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo    Launching JARVIS...
echo ========================================
echo.

REM Launch JARVIS
python main.py

echo.
echo [INFO] JARVIS closed.
pause

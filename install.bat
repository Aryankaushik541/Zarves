@echo off
echo ========================================
echo    ZARVES AI AGENT - Auto Installer
echo ========================================
echo.

echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version
echo Python found!
echo.

echo [2/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/5] Installing core dependencies...
pip install pyttsx3 SpeechRecognition selenium webdriver-manager psutil pyautogui requests beautifulsoup4 lxml python-dotenv
echo.

echo [4/5] Installing Windows-specific packages...
pip install pywin32 comtypes pygetwindow wmi
echo.

echo [5/5] Installing optional packages...
echo Installing PyAudio (may fail - that's okay)...
pip install pipwin
pipwin install pyaudio
if errorlevel 1 (
    echo.
    echo WARNING: PyAudio installation failed.
    echo Voice recognition will still work but may be less accurate.
    echo You can install it manually later if needed.
    echo.
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To run Zarves, type one of these:
echo     python main.py
echo     python zarves_pro.py
echo     python zarves_advanced.py
echo.
echo For help, read README.md
echo.
echo NOTE: Make sure you have a working microphone!
echo.
pause

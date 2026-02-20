@echo off
echo ========================================
echo    ZARVES AI AGENT - Auto Installer
echo ========================================
echo.

echo [1/6] Checking Python...
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

echo [2/6] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Pip not found! Installing pip...
    echo.
    
    echo Downloading get-pip.py...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    
    if exist get-pip.py (
        echo Installing pip...
        python get-pip.py
        del get-pip.py
        echo Pip installed successfully!
    ) else (
        echo Failed to download get-pip.py
        echo Trying alternative method...
        python -m ensurepip --default-pip
    )
    echo.
)

echo Verifying pip...
python -m pip --version
if errorlevel 1 (
    echo ERROR: Pip installation failed!
    echo Please install pip manually:
    echo 1. Download: https://bootstrap.pypa.io/get-pip.py
    echo 2. Run: python get-pip.py
    pause
    exit /b 1
)
echo Pip is working!
echo.

echo [3/6] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [4/6] Installing core dependencies...
python -m pip install pyttsx3 SpeechRecognition selenium webdriver-manager psutil pyautogui requests beautifulsoup4 lxml python-dotenv
echo.

echo [5/6] Installing Windows-specific packages...
python -m pip install pywin32 comtypes pygetwindow wmi
echo.

echo [6/6] Installing optional packages...
echo Installing PyAudio (may fail - that's okay)...
python -m pip install pipwin >nul 2>&1
pipwin install pyaudio >nul 2>&1
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

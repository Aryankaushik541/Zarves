@echo off
REM JARVIS Dependency Auto-Installer for Windows
REM Automatically installs all required dependencies

echo.
echo ========================================
echo    JARVIS Dependency Installer
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found
    set PYTHON_CMD=python
    set PIP_CMD=pip
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Python3 found
        set PYTHON_CMD=python3
        set PIP_CMD=pip3
    ) else (
        echo [ERROR] Python not found!
        echo.
        echo Please install Python 3.8+ from:
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
)

REM Show Python version
for /f "tokens=*" %%i in ('%PYTHON_CMD% --version') do set PYTHON_VERSION=%%i
echo    Version: %PYTHON_VERSION%
echo.

REM Upgrade pip
echo [2/5] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip
echo.

REM Install requirements
echo [3/5] Installing Python dependencies...
echo    This may take a few minutes...
echo.

if exist requirements.txt (
    %PIP_CMD% install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] All dependencies installed successfully!
    ) else (
        echo [WARNING] Some dependencies failed to install
        echo.
        echo Try manual installation:
        echo    %PIP_CMD% install selenium beautifulsoup4 requests webdriver-manager pywhatkit
    )
) else (
    echo [WARNING] requirements.txt not found
    echo Installing core dependencies manually...
    %PIP_CMD% install ollama selenium beautifulsoup4 requests webdriver-manager pywhatkit
)
echo.

REM Check Ollama
echo [4/5] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama found
    
    REM Check for model
    echo    Checking for llama3.2 model...
    ollama list | findstr "llama3.2" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] llama3.2 model found
    ) else (
        echo [INFO] Pulling llama3.2 model...
        echo    This may take a few minutes...
        ollama pull llama3.2
    )
) else (
    echo [WARNING] Ollama not found
    echo.
    echo Please install Ollama from:
    echo https://ollama.com/download/windows
    echo.
    echo After installation, run:
    echo    ollama pull llama3.2
)
echo.

REM Check VLC
echo [5/5] Checking VLC Player (optional)...
where vlc >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] VLC found
) else (
    echo [INFO] VLC not found (optional for movie playback)
    echo.
    echo Install VLC from:
    echo https://www.videolan.org/vlc/download-windows.html
)
echo.

REM Test imports
echo ========================================
echo    Testing Python Packages
echo ========================================
echo.

%PYTHON_CMD% -c "import ollama; print('[OK] Ollama')" 2>nul || echo [MISSING] Ollama
%PYTHON_CMD% -c "import selenium; print('[OK] Selenium')" 2>nul || echo [MISSING] Selenium
%PYTHON_CMD% -c "import bs4; print('[OK] BeautifulSoup4')" 2>nul || echo [MISSING] BeautifulSoup4
%PYTHON_CMD% -c "import requests; print('[OK] Requests')" 2>nul || echo [MISSING] Requests
%PYTHON_CMD% -c "import pywhatkit; print('[OK] PyWhatKit')" 2>nul || echo [MISSING] PyWhatKit

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Start JARVIS:
echo    %PYTHON_CMD% main.py
echo.
echo Read guides:
echo    - README.md
echo    - INSTALLATION.md
echo    - MOVIE_DOWNLOADER_GUIDE.md
echo    - YOUTUBE_AUTO_MUSIC_GUIDE.md
echo.
echo ========================================
echo.

pause

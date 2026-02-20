@echo off
echo ========================================
echo    ZARVES AI AGENT - Auto Installer
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/4] Installing dependencies...
pip install -r requirements.txt
echo.

echo [4/4] Installing additional packages...
pip install selenium webdriver-manager
echo.

echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To run Zarves, type:
echo     python zarves_advanced.py
echo.
echo For help, read QUICK_START.md
echo.
pause

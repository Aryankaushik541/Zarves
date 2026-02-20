@echo off
echo ========================================
echo    FIX PIP - Zarves Installation
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)
echo.

echo [2/3] Downloading get-pip.py...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
if errorlevel 1 (
    echo ERROR: Failed to download get-pip.py
    echo Please check your internet connection
    pause
    exit /b 1
)
echo.

echo [3/3] Installing pip...
python get-pip.py
if errorlevel 1 (
    echo ERROR: Failed to install pip
    echo Trying alternative method...
    python -m ensurepip --upgrade
)
echo.

echo Cleaning up...
del get-pip.py
echo.

echo ========================================
echo    Pip Installation Complete!
echo ========================================
echo.

echo Verifying pip...
python -m pip --version
echo.

echo Now you can run:
echo     install.bat
echo Or:
echo     python -m pip install -r requirements.txt
echo.
pause

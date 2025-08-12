@echo off
REM Terminal Command Menu - Setup Script for Windows
REM This script sets up the virtual environment and installs the package

echo 🚀 Setting up Terminal Command Menu...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is required but not installed.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install the package in development mode
echo 📥 Installing Terminal Command Menu...
pip install -e .

echo.
echo 🎉 Setup complete!
echo.
echo To use Terminal Command Menu:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python -m terminal_menu.main
echo.
echo To deactivate the virtual environment later: deactivate
echo.
echo 📚 For more information, see README.md
pause
